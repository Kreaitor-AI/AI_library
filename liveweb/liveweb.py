import requests
from bs4 import BeautifulSoup
from langchain import PromptTemplate
from langchain_openai import ChatOpenAI

class LiveWebToolkit:
    def __init__(self, api_key):
        self.api_key = api_key
        self.llm = ChatOpenAI(openai_api_key=api_key, model="gpt-3.5-turbo")

    def refine_search_query(self, query):
        template = """Refine the following query to make it more precise and suitable for a Google search:
        Initial Query: {query}
        Refined Query:"""
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
        template = """Summarize the following content accurately and comprehensively. Ensure that no key points are omitted, and all important details are included. The summary should reflect the full scope of the content:
        {content}
        """
        prompt = PromptTemplate(template=template, input_variables=["content"])
        processed_summaries = []
        max_chunk_length = 16000
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

if __name__ == "__main__":
    api_key = input("Enter your OpenAI API key: ")
    query = input("Enter your initial search query: ")
    num_results = int(input("Enter the number of search results to retrieve: "))
    toolkit = LiveWebToolkit(api_key)
    summary = toolkit.execute_toolkit(query, num_results)
    print(f"Final Summary: {summary}")
