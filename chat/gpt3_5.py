from langchain import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableLambda

class GPT3_5TurboClient:
    def __init__(self, api_key=None):
        self.llm = ChatOpenAI(openai_api_key=api_key, model="gpt-3.5-turbo")

    def chat_completion(self, initial_query, stream=False):
        template = "Refine the following query: {query}"
        prompt = PromptTemplate(template=template, input_variables=["query"])

        if stream:
            # For streaming responses
            llm_chain = prompt | RunnableLambda(self.llm.stream)
            for chunk in llm_chain.invoke({"query": initial_query}):
                print(chunk.content or "", end="", flush=True)
        else:
            # For non-streaming responses
            llm_chain = prompt | self.llm
            result = llm_chain.invoke({"query": initial_query})
            return result.content.strip()

def chat_completion(initial_query, api_key=None, stream=False):
    client = GPT3_5TurboClient(api_key)
    return client.chat_completion(initial_query, stream)
