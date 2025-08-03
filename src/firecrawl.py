import os
from firecrawl import FirecrawlApp, ScrapeOptions
from dotenv import load_dotenv

load_dotenv()

class FirecrawlService:
    def __init__(self):
        api_key = os.getenv('FIRECRAWL_API_KEY')
        if not api_key:
            raise EnvironmentError('FIRECRAWL_API_KEY environment variable not set')
        self.app: FirecrawlApp = FirecrawlApp(api_key)

    def search_company(self, query: str, num_results: int= 5):
        try:
            results = self.app.search(
                query=f"{query} company pricing",
                limit=num_results,
                scrape_options=ScrapeOptions(
                    formats=["markdown"]
                )
            )
            return results
        except Exception as e:
            print(e)
            return []


    def search_pages(self, url: str):
        try:
            results = self.app.scrape_url(
                url,
                format=["markdown"]
            )
            return results
        except Exception as e:
            print(e)
            return None