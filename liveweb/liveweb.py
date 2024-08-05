import aiohttp
import asyncio
from bs4 import BeautifulSoup
from langchain import PromptTemplate
from langchain_openai import ChatOpenAI
import yaml
import pkg_resources

try:
    import nest_asyncio
    nest_asyncio.apply()
except ImportError:
    pass  # nest_asyncio is not required in non-Jupyter environments

class LiveWebToolkit:
    def __init__(self, api_key, prompts_file=None):
        self.api_key = api_key
        self.llm = ChatOpenAI(openai_api_key=api_key, model="gpt-4o-mini")
        if prompts_file is None:
            prompts_file = pkg_resources.resource_filename(__name__, 'prompts.yaml')
        with open(prompts_file, 'r') as file:
            self.prompts = yaml.safe_load(file)

    def refine_search_query(self, query):
        template = self.prompts['refine_search_query']
        prompt = PromptTemplate(template=template, input_variables=["query"])
        result = prompt | self.llm
        return result.invoke({"query": query}).content.strip()

    async def perform_google_search(self, query, num_results=10):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        search_url = f"https://www.google.com/search?q={query}&num={num_results}"
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(search_url, headers=headers, timeout=20) as response:
                    if response.status != 200:
                        return []
                    text = await response.text()
            except Exception:
                return []

        soup = BeautifulSoup(text, "html.parser")
        results = []
        for item in soup.find_all('div', class_='tF2Cxc'):
            try:
                title = item.find('h3').text if item.find('h3') else 'No title'
                link = item.find('a')['href'] if item.find('a') else 'No link'
                snippet = item.find('span', class_='aCOpRe').text if item.find('span', 'aCOpRe') else 'No snippet'
                results.append((title, link, snippet))
            except Exception:
                continue
        return results

    async def fetch_web_content(self, url, session):
        try:
            async with session.get(url, timeout=10) as response:
                if response.status == 403 or response.status != 200:
                    return None  # Skip URLs with 403 status or any non-200 status
                text = await response.text()
                soup = BeautifulSoup(text, 'html.parser')
                paragraphs = soup.find_all('p')
                content = "\n".join([para.get_text() for para in paragraphs])
                return content
        except Exception:
            return None

    async def fetch_all_content(self, urls):
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch_web_content(url, session) for url in urls]
            return await asyncio.gather(*tasks)

    def process_web_content_with_llm(self, contents):
        template = self.prompts['summarize_content']
        prompt = PromptTemplate(template=template, input_variables=["content"])
        result = prompt | self.llm
        return result.invoke({"content": contents}).content.strip()

    async def execute_toolkit(self, initial_query, num_results):
        refined_query = self.refine_search_query(initial_query)
        search_results = await self.perform_google_search(refined_query, num_results)
        if not search_results:
            return "No search results found."

        urls = [link for _, link, _ in search_results]
        fetched_content = await self.fetch_all_content(urls)
        fetched_content = [content for content in fetched_content if content]

        if fetched_content:
            final_summary = self.process_web_content_with_llm(" ".join(fetched_content))
            if final_summary.strip():
                return final_summary
        return "Failed to get a valid response."

def web_summary(api_key, initial_query, num_results, prompts_file=None):
    toolkit = LiveWebToolkit(api_key, prompts_file)
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(toolkit.execute_toolkit(initial_query, num_results))
