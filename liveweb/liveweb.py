import requests
from bs4 import BeautifulSoup
from langchain import PromptTemplate
from langchain_openai import ChatOpenAI
import yaml
import pkg_resources
from concurrent.futures import ThreadPoolExecutor, as_completed

class LiveWebToolkit:
    def __init__(self, api_key, prompts_file=None):
        self.api_key = api_key
        self.llm = ChatOpenAI(openai_api_key=api_key, model="gpt-3.5-turbo")
        if prompts_file is None:
            prompts_file = pkg_resources.resource_filename(__name__, 'prompts.yaml')
        with open(prompts_file, 'r') as file:
            self.prompts = yaml.safe_load(file)

    def refine_search_query(self, query):
        template = self.prompts.get('refine_search_query', "Refine the following query to make it more precise and suitable for a Google search: {query}")
        prompt = PromptTemplate(template=template, input_variables=["query"])
        result = prompt | self.llm
        return result.invoke({"query": query}).content.strip()

    def perform_google_search(self, query, num_results=10):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        search_url = f"https://www.google.com/search?q={query}&num={num_results}"
        try:
            response = requests.get(search_url, headers=headers, timeout=10)  # 10 seconds timeout
            response.raise_for_status()
        except Exception:
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        results = []
        for item in soup.find_all('div', class_='tF2Cxc'):
            title = item.find('h3').text if item.find('h3') else 'No title'
            link = item.find('a')['href'] if item.find('a') else 'No link'
            snippet = item.find('span', class_='aCOpRe').text if item.find('span', 'aCOpRe') else 'No snippet'
            results.append((title, link, snippet))
        return results

    def fetch_web_content(self, url):
        try:
            response = requests.get(url, timeout=10)  # 10 seconds timeout
            response.raise_for_status()
            if response.status_code == 403:
                return None
            soup = BeautifulSoup(response.content, 'html.parser')
            paragraphs = soup.find_all('p')
            content = "\n".join([para.get_text() for para in paragraphs])
            return content
        except Exception:
            return None

    def process_web_content_with_llm(self, contents):
        template = self.prompts.get('summarize_content', "Summarize the following content accurately and comprehensively: {content}")
        prompt = PromptTemplate(template=template, input_variables=["content"])
        result = prompt | self.llm
        return result.invoke({"content": contents}).content.strip()

    def execute_toolkit(self, initial_query, num_results):
        refined_query = self.refine_search_query(initial_query)
        search_results = self.perform_google_search(refined_query, num_results)
        if not search_results:
            return "No search results found."

        urls = [link for _, link, _ in search_results]
        fetched_content = []

        # Using ThreadPoolExecutor to fetch content concurrently
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_url = {executor.submit(self.fetch_web_content, url): url for url in urls}
            for future in as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    content = future.result()
                    if content:
                        fetched_content.append(content)
                except Exception:
                    continue

        if fetched_content:
            final_summary = self.process_web_content_with_llm(" ".join(fetched_content))
            if final_summary.strip():
                return final_summary
        return "Failed to get a valid response."

def web_summary(api_key, initial_query, num_results, prompts_file=None):
    toolkit = LiveWebToolkit(api_key, prompts_file)
    return toolkit.execute_toolkit(initial_query, num_results)
