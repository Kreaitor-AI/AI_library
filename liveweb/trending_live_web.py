def execute_toolkit(self, initial_query: str, num_results: int) -> str:
    refined_query = self.refine_search_query(initial_query)
    search_results = self.perform_google_search(refined_query, num_results)
    if not search_results:
        return "No search results found."

    fetched_content = self.fetch_content_concurrently([link for _, link, _ in search_results])

    if fetched_content:
        # Removed the extra argument 'refined_query'
        final_summary = self.process_web_content_with_llm(" ".join(fetched_content))
        if final_summary.strip():
            return final_summary
    return "Failed to get a valid response."
This change should resolve the TypeError and the method process_web_content_with_llm will now be called with the correct number of arguments.






You said:
give me full code
ChatGPT said:
ChatGPT
Here is the full corrected code with the changes applied:

python
Copy code
import requests
from bs4 import BeautifulSoup
from langchain import PromptTemplate
from langchain_openai import ChatOpenAI
import yaml
import pkg_resources
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Tuple, Optional

class LiveWebToolkit:
    def __init__(self, api_key: str, prompts_file: Optional[str] = None):
        self.api_key = api_key
        self.llm = ChatOpenAI(openai_api_key=api_key, model="gpt-3.5-turbo")
        self.prompts = self.load_prompts(prompts_file)

    def load_prompts(self, prompts_file: Optional[str]) -> dict:
        if prompts_file is None:
            prompts_file = pkg_resources.resource_filename(__name__, 'prompts.yaml')
        with open(prompts_file, 'r') as file:
            return yaml.safe_load(file)

    def refine_search_query(self, query: str) -> str:
        template = self.prompts['refine_search_query']
        prompt = PromptTemplate(template=template, input_variables=["query"])
        result = prompt | self.llm
        return result.invoke({"query": query}).content.strip()

    def perform_google_search(self, query: str, num_results: int = 10) -> List[Tuple[str, str, str]]:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            )
        }
        search_url = f"https://www.google.com/search?q={query}&num={num_results}"
        try:
            response = requests.get(search_url, headers=headers, timeout=10)
            response.raise_for_status()
        except requests.RequestException:
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        return self.parse_google_results(soup)

    def parse_google_results(self, soup: BeautifulSoup) -> List[Tuple[str, str, str]]:
        results = []
        for item in soup.find_all('div', class_='tF2Cxc'):
            title = item.find('h3').text if item.find('h3') else 'No title'
            link = item.find('a')['href'] if item.find('a') else 'No link'
            snippet = item.find('span', class_='aCOpRe').text if item.find('span', 'aCOpRe') else 'No snippet'
            results.append((title, link, snippet))
        return results

    def fetch_web_content(self, url: str) -> Optional[str]:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            if response.status_code == 403:
                return None
            soup = BeautifulSoup(response.content, 'html.parser')
            paragraphs = soup.find_all('p')
            return "\n".join(para.get_text() for para in paragraphs)
        except (requests.RequestException, Exception):
            return None

    def process_web_content_with_llm(self, contents: str) -> str:
        template = """Summarize the following content accurately and comprehensively based on the query. Ensure that no key points are omitted, and all important details are included. The summary should reflect the full scope of the content:
        Content: {content}
        """

        prompt = PromptTemplate(template=template, input_variables=["content"])
        llm_chain = prompt | self.llm

        processed_summaries = []
        max_chunk_length = 16000  # Max tokens for the model
        content_chunks = [contents[i:i + max_chunk_length] for i in range(0, len(contents), max_chunk_length)]

        for chunk in content_chunks:
            result = llm_chain.invoke({"content": chunk}).content.strip()
            processed_summaries.append(result)

        return " ".join(processed_summaries)

    def execute_toolkit(self, initial_query: str, num_results: int) -> str:
        refined_query = self.refine_search_query(initial_query)
        search_results = self.perform_google_search(refined_query, num_results)
        if not search_results:
            return "No search results found."

        fetched_content = self.fetch_content_concurrently([link for _, link, _ in search_results])

        if fetched_content:
            # Removed the extra argument 'refined_query'
            final_summary = self.process_web_content_with_llm(" ".join(fetched_content))
            if final_summary.strip():
                return final_summary
        return "Failed to get a valid response."

    def fetch_content_concurrently(self, urls: List[str], max_workers: int = 5) -> List[str]:
        fetched_content = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_url = {executor.submit(self.fetch_web_content, url): url for url in urls}
            for future in as_completed(future_to_url):
                try:
                    content = future.result()
                    if content:
                        fetched_content.append(content)
                except Exception:
                    continue
        return fetched_content

def trending_web_summary(api_key: str, initial_query: str, num_results: int, prompts_file: Optional[str] = None) -> str:
    toolkit = LiveWebToolkit(api_key, prompts_file)
    return toolkit.execute_toolkit(initial_query, num_results)
