import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
from langchain import PromptTemplate
from langchain_openai import ChatOpenAI
import yaml
import pkg_resources

class LiveWebToolkit:
    def __init__(self, api_key, prompts_file=None):
        self.api_key = api_key
        self.llm = ChatOpenAI(openai_api_key=api_key, model="gpt-3.5-turbo")
        if prompts_file is None:
            prompts_file = pkg_resources.resource_filename(__name__, 'prompts.yaml')
        with open(prompts_file, 'r') as file:
            self.prompts = yaml.safe_load(file)
    
    def refine_query(self, initial_query):
        template = self.prompts["refine_search_query"]
        prompt = PromptTemplate(template=template, input_variables=["query"])
        llm_chain = prompt | self.llm

        result = llm_chain.invoke({"query": initial_query})

        return result.content.strip()

    def google_search(self, query, num_results=3):
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
            results.append((snippet, link))

        return results

    def fetch_content(self, url):
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            paragraphs = soup.find_all('p')
            content = "\n".join([para.get_text() for para in paragraphs])
            return content
        except Exception as e:
            return str(e)

    def process_scraped_content_with_llm(self, contents):
        template = self.prompts["summarize_content"]
        prompt = PromptTemplate(template=template, input_variables=["content"])
        llm_chain = prompt | self.llm

        processed_summaries = []

        max_chunk_length = 16000
        content_chunks = []
        for content in contents:
            chunks = [content[i:i + max_chunk_length] for i in range(0, len(content), max_chunk_length)]
            content_chunks.extend(chunks)
        results = llm_chain.batch([{"content": chunk} for chunk in content_chunks], config={"max_concurrency": 10})

        for result in results:
            processed_summaries.append(result.content)

        final_summary = " ".join(processed_summaries)

        return final_summary

    def execute_toolkit(self, initial_query, num_results):
        refined_query = self.refine_query(initial_query)
        search_results = self.google_search(refined_query, num_results)
        contents = [self.fetch_content(link) for _, link in search_results]
        summary = self.process_scraped_content_with_llm(contents)
        return summary

def web_summary(api_key, initial_query, num_results, prompts_file=None):
    toolkit = LiveWebToolkit(api_key, prompts_file)
    return toolkit.execute_toolkit(initial_query, num_results)
