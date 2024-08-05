import requests
from bs4 import BeautifulSoup
from langchain import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableLambda

class WebToolkit:
    def __init__(self, api_key, prompts_file=None):
        self.api_key = api_key
        self.llm = ChatOpenAI(openai_api_key=api_key, model="gpt-3.5-turbo")
        self.prompts_file = prompts_file
        self.prompts = self.load_prompts(prompts_file)
        
        self.refine_query_runnable = RunnableLambda(func=lambda inputs: self.refine_query(inputs))
        self.google_search_runnable = RunnableLambda(func=lambda inputs: self.google_search(inputs[0], inputs[1]))
        self.fetch_content_runnable = RunnableLambda(func=lambda url: self.fetch_content(url))
        self.process_content_runnable = RunnableLambda(func=lambda contents: self.process_scraped_content_with_llm(contents))

    def load_prompts(self, prompts_file):
        if prompts_file is None:
            raise ValueError("Prompts file must be provided")
        import yaml
        with open(prompts_file, 'r') as file:
            return yaml.safe_load(file)

    def refine_query(self, initial_query):
        template = self.prompts['refine_search_query']
        prompt = PromptTemplate(template=template, input_variables=["query"])
        llm_chain = prompt | self.llm
        result = llm_chain.invoke({"query": initial_query})
        return result.content.strip()

    def google_search(self, query, num_results=10):
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
        template = self.prompts['summarize_content']
        prompt = PromptTemplate(template=template, input_variables=["content"])
        llm_chain = prompt | self.llm

        processed_summaries = []
        max_chunk_length = 16000
        content_chunks = [contents[i:i + max_chunk_length] for i in range(0, len(contents), max_chunk_length)]
        results = llm_chain.batch([{"content": chunk} for chunk in content_chunks], config={"max_concurrency": 10})

        for result in results:
            processed_summaries.append(result.content)

        final_summary = " ".join(processed_summaries)
        return final_summary

    def web_summary(self, initial_query, num_results):
        refined_query = self.refine_query_runnable.invoke(initial_query)
        search_results = self.google_search_runnable.invoke([refined_query, num_results])
        fetched_contents = [self.fetch_content_runnable.invoke(link) for _, link, _ in search_results]
        final_summary = self.process_content_runnable.invoke(fetched_contents)
        return final_summary
