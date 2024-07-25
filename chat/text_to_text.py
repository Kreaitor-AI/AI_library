from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from together import Together

class TextToTextProcessor:
    def __init__(self, model, api_key, prompt=None):
        self.model = model
        self.api_key = api_key
        self.prompt = prompt

        if model in ["gpt_3_5", "gpt_4o_mini"]:
            self.llm = ChatOpenAI(openai_api_key=api_key, model=model.replace("_", "-"))
        elif model == "llama3":
            self.client = Together(api_key=api_key)
        else:
            raise ValueError("Unsupported model.")

    def process(self, prompt):
        self.prompt = prompt
        if hasattr(self, 'llm'):
            template = "{prompt}"
            prompt_template = PromptTemplate(template=template, input_variables=["prompt"])
            chain = prompt_template | self.llm
            result = chain.invoke({"prompt": self.prompt})
            return result.content.strip()
        else:
            messages = [{"role": "user", "content": self.prompt}]
            model = "meta-llama/Llama-3-70b-chat-hf"
            response = self.client.chat.completions.create(
                model=model,
                messages=messages
            )
            return response.choices[0].message.content

    def concat(self, next_model, next_prompt):
        next_processor = TextToTextProcessor(next_model, self.api_key, next_prompt)
        return next_processor.process(next_prompt)

def text_to_text(model, api_key, prompt=None):
    return TextToTextProcessor(model, api_key, prompt)
