import requests
from bs4 import BeautifulSoup
from langchain import PromptTemplate
from langchain_openai import ChatOpenAI
import yaml
import pkg_resources

class LiveWebToolkit:
    def __init__(self, api_key, prompts_file=None):
        self.api_key = api_key
        self.llm = ChatOpenAI(openai_api_key=api_key, model="gpt-4o-mini")
        if prompts_file is None:
            # Use the default prompts file within the package
            prompts_file = pkg_resources.resource_filename(__name__, 'prompts.yaml')
        # Load prompts from the YAML file
        with open(prompts_file, 'r') as file:
            self.prompts = yaml.safe_load(file)

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
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            paragraphs = soup.find_all('p')
            content = "\n".join([para.get_text() for para in paragraphs])
            return content
        except Exception as e:
            return str(e)

    def process_web_content_with_llm(self, contents):
        template = self.prompts['summarize_content']
        prompt = PromptTemplate(template=template, input_variables=["content"])
        processed_summaries = []
        max_chunk_length = 40000
        content_chunks = [contents[i:i + max_chunk_length] for i in range(0, len(contents), max_chunk_length)]
        for chunk in content_chunks:
            result = prompt | self.llm
            summary = result.invoke({"content": chunk}).content
            processed_summaries.append(summary)
        final_summary = " ".join(processed_summaries)
        return final_summary

    def execute_toolkit(self, initial_query, num_results):
        refined_query = self.refine_search_query(initial_query)
        search_results = self.perform_google_search(refined_query, num_results)
        fetched_content = []
        for title, link, snippet in search_results:
            content = self.fetch_web_content(link)
            fetched_content.append(content)
        final_summary = self.process_web_content_with_llm(" ".join(fetched_content))
        return final_summary

def web_summary(api_key, initial_query, num_results, prompts_file=None):
    toolkit = LiveWebToolkit(api_key, prompts_file)
    return toolkit.execute_toolkit(initial_query, num_results)
