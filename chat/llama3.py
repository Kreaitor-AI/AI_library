# text_to_text.py
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from together import Together
from llama3 import llama3 as llama3_client

class TextToTextProcessor:
    def __init__(self, model: str, api_key: str, prompt: str = None):
        self.model = model
        self.api_key = api_key
        self.prompt = prompt

        if model in ["gpt-3.5-turbo", "gpt-4o-mini"]:
            self.llm = ChatOpenAI(openai_api_key=api_key, model=model)
        elif model == "llama3":
            self.client = llama3_client
        else:
            raise ValueError("Unsupported model.")

    def process(self, prompt: str) -> str:
        self.prompt = prompt
        if hasattr(self, 'llm'):
            template = "{prompt}"
            prompt_template = PromptTemplate(template=template, input_variables=["prompt"])
            chain = prompt_template | self.llm
            result = chain.invoke({"prompt": self.prompt})
            return result.content.strip()
        elif hasattr(self, 'client'):
            return self.client(self.prompt, api_key=self.api_key)
        else:
            raise ValueError("Unsupported model.")

    def concat(self, next_model: str, next_prompt: str) -> str:
        next_processor = TextToTextProcessor(next_model, self.api_key, next_prompt)
        return next_processor.process(next_prompt)

def text_to_text(model: str, api_key: str, prompt: str = None) -> TextToTextProcessor:
    return TextToTextProcessor(model, api_key, prompt)
