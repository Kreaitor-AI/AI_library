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
        print(f"Refined Query: {refined_query}")  # Print the refined query
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
            paragraphs = soup.find_all(['p', 'div'])
            content = "\n".join([para.get_text() for para in paragraphs if para.get_text(strip=True)])
            print(f"Fetched content from {url}:\n{content}\n")  # Print the fetched content
            return content
        except Exception as e:
            return f"Error fetching content from {url}: {str(e)}"

    def process_web_content_with_llm(self, contents):
        template = """Summarize the following content accurately and comprehensively. Ensure that no key points are omitted, and all important details are included. The summary should reflect the full scope of the content:
        {content}
        """
        prompt = PromptTemplate(template=template, input_variables=["content"])
        llm_chain = prompt | self.llm

        processed_summaries = []

        max_chunk_length = 55000
        content_chunks = [contents[i:i + max_chunk_length] for i in range(0, len(contents), max_chunk_length)]
        results = llm_chain.batch([{"content": chunk} for chunk in content_chunks], config={"max_concurrency": 10})

        for result in results:
            processed_summaries.append(result.content)

        final_summary = " ".join(processed_summaries)
        print(f"Summary:\n{final_summary}\n")  # Print the summary
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
