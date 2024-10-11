import requests
from bs4 import BeautifulSoup
from langchain import PromptTemplate
from langchain_openai import ChatOpenAI
import yaml
import pkg_resources
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Tuple, Optional

class LiveWebToolkit:
    """
    Centralizes various web-related tasks like query refinement, web searching, summarization, and content fetching.
    Parameters:
        - api_key (str): The API key required to authenticate requests to the external live services.
        - prompts_file (Optional[str]): The path to a YAML file containing predefined prompts. Default is None.
    Processing Logic:
        - Initializes a ChatOpenAI instance using the provided API key and a specific model for processing.
        - Loads prompts from a YAML file, which is used for constructing inputs for the large language model.
        - All web content extraction functions handle potential request failures and return appropriate outputs.
        - Utilizes concurrent requests to optimize content fetching performance when dealing with multiple URLs.
    """
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
        """Performs a Google search and retrieves search results.
        Parameters:
            - query (str): The search query string.
            - num_results (int, optional): The number of search results to return. Defaults to 10.
        Returns:
            - List[Tuple[str, str, str]]: A list of tuples containing the search result title, URL, and description.
        Processing Logic:
            - A User-Agent header is set to mimic a browser request.
            - The Google search URL is constructed with the query and the number of results specified.
            - A GET request is sent to the Google search URL with a timeout of 10 seconds.
            - If the request fails, an empty list is returned. Otherwise, the response is parsed to extract search results."""
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
        """Parse search results from a Google search results page.
        Parameters:
            - soup (BeautifulSoup): Parsed HTML content of the search results page.
        Returns:
            - List[Tuple[str, str, str]]: A list of tuples, each containing the title, link, and snippet of a search result.
        Processing Logic:
            - The function iterates over each search result container found in the parsed HTML.
            - It ensures that if an element is missing (title, link, or snippet), a placeholder string is provided."""
        results = []
        for item in soup.find_all('div', class_='tF2Cxc'):
            title = item.find('h3').text if item.find('h3') else 'No title'
            link = item.find('a')['href'] if item.find('a') else 'No link'
            snippet = item.find('span', class_='aCOpRe').text if item.find('span', 'aCOpRe') else 'No snippet'
            results.append((title, link, snippet))
        return results

    def fetch_web_content(self, url: str) -> Optional[str]:
        """Fetches and returns web content as a concatenated string of all paragraph tags.
        Parameters:
            - url (str): The URL of the web page to fetch content from.
        Returns:
            - Optional[str]: A string containing all the text within paragraph tags of the web page, or None if an error occurs or access is forbidden.
        Processing Logic:
            - The function uses `requests.get` to perform an HTTP GET request to fetch the webpage.
            - It checks for a 403 status code to handle forbidden access explicitly.
            - Utilizes BeautifulSoup to parse the HTML content and extract text from paragraph tags."""
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

    def process_web_content_with_llm(self, contents: str, query: str) -> str:
        """Summarize web content based on a provided query using a large language model (LLM).
        Parameters:
            - contents (str): The web content to be summarized.
            - query (str): The query that guides the summarization process.
        Returns:
            - str: A comprehensive summary of the web content based on the provided query.
        Processing Logic:
            - Splits the input content into chunks that do not exceed the maximum token length the LLM can handle.
            - Passes each content chunk individually to the LLM along with the query for processing.
            - Accumulates and concatenates the summaries generated from each chunk to form a comprehensive final summary."""
        template = """Summarize the following content accurately and comprehensively based on the query. Ensure that no key points are omitted, and all important details are included. The summary should reflect the full scope of the content:
        Query: {query}
        Content: {content}
        """

        prompt = PromptTemplate(template=template, input_variables=["content", "query"])
        llm_chain = prompt | self.llm

        processed_summaries = []
        max_chunk_length = 16000  # Max tokens for the model
        content_chunks = [contents[i:i + max_chunk_length] for i in range(0, len(contents), max_chunk_length)]

        for chunk in content_chunks:
            result = llm_chain.invoke({"content": chunk, "query": query}).content.strip()
            processed_summaries.append(result)

        return " ".join(processed_summaries)

    def execute_toolkit(self, initial_query: str, num_results: int) -> str:
        """Executes a sequence of actions to refine and process a search query and return a final summary.
        Parameters:
            - initial_query (str): The initial search query provided by the user.
            - num_results (int): The number of search results to be retrieved.
        Returns:
            - str: The summarized content of the search results or an error message.
        Processing Logic:
            - The function refines the search query to improve search results.
            - It performs a Google search and fetches content concurrently from the result links.
            - If the content is retrieved, it processes the web content and provides a final summary.
            - Returns an error message if no content is fetched or no summary is generated."""
        refined_query = self.refine_search_query(initial_query)
        search_results = self.perform_google_search(refined_query, num_results)
        if not search_results:
            return "No search results found."

        fetched_content = self.fetch_content_concurrently([link for _, link, _ in search_results])

        if fetched_content:
            final_summary = self.process_web_content_with_llm(" ".join(fetched_content), refined_query)
            if final_summary.strip():
                return final_summary
        return "Failed to get a valid response."

    def fetch_content_concurrently(self, urls: List[str], max_workers: int = 5) -> List[str]:
        """Fetch web content for multiple URLs concurrently.
        Parameters:
            - urls (List[str]): A list of URLs from which to fetch content.
            - max_workers (int): The maximum number of worker threads to use, default is 5.
        Returns:
            - List[str]: A list of content from the given URLs.
        Processing Logic:
            - Utilizes a ThreadPoolExecutor to handle concurrent requests.
            - Submits fetch_web_content jobs for each URL into the pool.
            - Appends successful fetch results to the fetched_content list."""
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

def web_summary(api_key: str, initial_query: str, num_results: int, prompts_file: Optional[str] = None) -> str:
    toolkit = LiveWebToolkit(api_key, prompts_file)
    return toolkit.execute_toolkit(initial_query, num_results)
