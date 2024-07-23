from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

class GPT4ominiClient:
    def __init__(self, api_key=None):
        self.api_key = api_key

    def chat_completion(self, prompt, stream=False):
        template = "{prompt}"
        prompt_template = PromptTemplate(template=template, input_variables=["prompt"])
        
        callbacks = [StreamingStdOutCallbackHandler()] if stream else None
        
        llm = ChatOpenAI(
            openai_api_key=self.api_key, 
            model="gpt-4omini",
            streaming=stream,
            callbacks=callbacks
        )
        
        chain = prompt_template | llm
        
        result = chain.invoke({"prompt": prompt})
        
        if not stream:
            return result.content.strip()

def gpt4omini(prompt, api_key=None, stream=False):
    client = GPT4ominiClient(api_key)
    return client.chat_completion(prompt, stream)
