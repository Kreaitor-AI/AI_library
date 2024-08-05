import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
from langchain import PromptTemplate
from langchain_openai import ChatOpenAI
import yaml
import pkg_resources
import time

class LiveWebToolkit:
    def __init__(self, api_key, prompts_file=None, max_retries=3):
        self.api_key = api_key
        self.llm = ChatOpenAI(openai_api_key=api_key, model="gpt-3.5-turbo")
        if prompts_file is None:
            prompts_file = pkg_resources.resource_filename(__name__, 'prompts.yaml')
        with open(prompts_file, 'r') as file:
            self.prompts = yaml.safe_load(file)
        self.max_retries = max_retries

    def refine_search_query(self, query):
        template = self.prompts['refine_search_query']
        prompt = PromptTemplate(template=template, input_variables=["query"])
        result = prompt | self.llm
        refined_query = result.invoke({"query": query}).content.strip()
        return refined_query

    def perform_google_search(self, query, num_results):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        search_url = f"https://www.google.com/search?q={query}&num={num_results}"
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        results = []
        for item in soup.find_all('div', class_='tF2Cxc'):
            title = item.find('h3').text if item.find('h3') else 'No title'
            link = item.find('a')['href'] if item.find('a') else 'No link'
            snippet = item.find('span', class_='aCOpRe').text if item.find('span', 'aCOpRe') else 'No snippet'
            results.append((title, link, snippet))
        return results

    def fetch_web_content(self, url):
        for attempt in range(self.max_retries):
            try:
                response = requests.get(url)
                response.raise_for_status()
                if response.status_code == 403:
                    return None
                soup = BeautifulSoup(response.content, 'html.parser')
                paragraphs = soup.find_all('p')
                content = "\n".join([para.get_text() for para in paragraphs])
                if content:
                    return content
            except HTTPError:
                if response.status_code == 403:
                    return None
            except Exception:
                pass
            time.sleep(2 ** attempt)
        return None

    def process_web_content_with_llm(self, contents):
        template = self.prompts['summarize_content']
        prompt = PromptTemplate(template=template, input_variables=["content"])
        processed_summaries = []
        max_chunk_length = 16000  # Adjusted chunk length to avoid token limits
        content_chunks = [contents[i:i + max_chunk_length] for i in range(0, len(contents), max_chunk_length)]
        for chunk in content_chunks:
            result = prompt | self.llm
            summary = result.invoke({"content": chunk}).content
            processed_summaries.append(summary)
        return " ".join(processed_summaries)

    def execute_toolkit(self, initial_query, num_results):
        for attempt in range(self.max_retries):
            refined_query = self.refine_search_query(initial_query)
            search_results = self.perform_google_search(refined_query, num_results)
            if not search_results:
                time.sleep(2 ** attempt)
                continue

            fetched_content = []
            for _, link, _ in search_results:
                content = self.fetch_web_content(link)
                if content:
                    fetched_content.append(content)

            if fetched_content:
                final_summary = self.process_web_content_with_llm(" ".join(fetched_content))
                if final_summary.strip():
                    return final_summary
            time.sleep(2 ** attempt)
        return "Failed to get a valid response after multiple attempts."

def web_summary(api_key, initial_query, num_results, prompts_file=None):
    toolkit = LiveWebToolkit(api_key, prompts_file)
    return toolkit.execute_toolkit(initial_query, num_results)
