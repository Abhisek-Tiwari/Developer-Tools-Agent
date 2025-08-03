from typing import Dict, Any
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from .model import ResearchState, CompanyInfo, CompanyAnalysis
from .firecrawl import FirecrawlService
from .prompt_handling import DeveloperToolsPrompts

class Agent:
    def __init__(self):
        self.model = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
        self.prompts = DeveloperToolsPrompts()
        self.firecrawl = FirecrawlService()
        self.workflow = self._build_workflow()


    def _build_workflow(self):
        graph = StateGraph(ResearchState)
        graph.add_node("extract_tools", self._extract_tools_stage)
        graph.add_node("research", self._research_stage)
        graph.add_node("analyze", self._analyze_stage)
        graph.add_edge("extract_tools", "research")
        graph.add_edge("research", "analyze")
        graph.add_edge("analyze", END)
        return graph.compile()

    def _extract_tools_stage(self, state: ResearchState) -> Dict[str, Any]:
        print(f"Extracting articles for: {state.query}")

        article_query = f"{state.query} tools comparison best alternatives"
        results = self.firecrawl.search_company(article_query, num_results=3)

        content = ""
        for result in results.data:
            url = result.get("url", "")
            scrape = self.firecrawl.search_pages(url)
            if scrape:
                content + scrape.markdown[:1500] + "\n\n"

        messages=[
            SystemMessage(content=self.prompts.TOOL_EXTRACTION_SYSTEM),
            HumanMessage(content=self.prompts.tool_extraction_user(state.query, content)),
        ]

        try:
            response = self.model.invoke(messages)
            tools = [
                name.strip()
                for name in response.content.strip().split("\n")
                if name.strip()
            ]
            print(f"Tools extracted are: {'. '.join(tools[:5])}")
            return {"extracted_tools": tools}
        except Exception as e:
            print(e)
            return {"extracted_tools": []}


    def _analyze_company_content(self, company_name: str, content: str) -> CompanyAnalysis:
        struct_model = self.model.with_structured_output(CompanyAnalysis)

        messages = [
            SystemMessage(content=self.prompts.TOOL_EXTRACTION_SYSTEM),
            HumanMessage(content=self.prompts.tool_extraction_user(company_name, content))
        ]

        try:
            analysis = struct_model.invoke(messages)
            return analysis
        except Exception as e:
            print(e)
            return CompanyAnalysis(
                pricing_model="Unknown",
                is_open_source=None,
                tech_stack=[],
                api_available=None,
                language_support=[],
                integration_capabilities=[]
            )

    def _research_stage(self, state: ResearchState) -> Dict[str, Any]:
        extracted_tools = getattr(state, "extracted_tools", [])

        if not extracted_tools:
            print("No extracted tools found")
            search_results = self.firecrawl.search_company(state.query, num_results=4)
            tool_names = [
                search_result.get("metadata", {}).get("title", "Unknown")
                for search_result in search_results
            ]
        else:
            tool_names = extracted_tools[:4]

        print(f"Researching the tools: {', '.join(tool_names)}")

        companies = []
        for tool_name in tool_names:
            tool_search_results = self.firecrawl.search_company(tool_name+ " official website", num_results=1)

            if tool_search_results:
                result = tool_search_results.data[0]
                url = result.get("url", "")

                company = CompanyInfo(
                    name=tool_name,
                    description=result.get("markdown",""),
                    website=url,
                    tech_stack=[],
                    competitors=[]
                )

                scrape = self.firecrawl.search_pages(url)
                if scrape:
                    content = scrape.markdown
                    analysis = self._analyze_company_content(company.name, content)

                    company.pricing_model = analysis.pricing_model
                    company.is_open_source = analysis.is_open_source
                    company.tech_stack = analysis.tech_stack
                    company.api_available = analysis.api_available
                    company.language_support = analysis.language_support
                    company.integration_capabilities = analysis.integration_capabilities
                    company.description = analysis.description

                companies.append(company)

        return {"companies": companies}


    def _analyze_stage(self, state: ResearchState) -> Dict[str, Any]:
        print("Making recommendations")

        company_data = ", ".join([
            company.json() for company in state.companies
        ])

        messages = [
            SystemMessage(content=self.prompts.RECOMMENDATIONS_SYSTEM),
            HumanMessage(content=self.prompts.recommendations_user(state.query, company_data)),
        ]

        response = self.model.invoke(messages)
        return {"analysis": response.content}

    def run(self, query: str) -> ResearchState:
        initial_state = ResearchState(query=query)
        final_state = self.workflow.invoke(initial_state)
        return ResearchState(**final_state)



