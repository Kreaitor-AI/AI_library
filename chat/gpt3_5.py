from langchain import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableLambda

class GPT3_5TurboClient:
    def __init__(self, api_key=None):
        self.llm = ChatOpenAI(openai_api_key=api_key, model="gpt-3.5-turbo")

    def chat_completion(self, prompt, stream=False):
        template = "{prompt}"
        prompt_template = PromptTemplate(template=template, input_variables=["prompt"])

        if stream:
            # For streaming responses
            llm_chain = prompt_template | RunnableLambda(self.llm.stream)
            for chunk in llm_chain.invoke({"prompt": prompt}):
                print(chunk.content or "", end="", flush=True)
        else:
            # For non-streaming responses
            llm_chain = prompt_template | self.llm
            result = llm_chain.invoke({"prompt": prompt})
            return result.content.strip()

def gpt3_5(prompt, api_key=None, stream=False):
    client = GPT3_5TurboClient(api_key)
    return client.chat_completion(prompt, stream)
