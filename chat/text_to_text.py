# text_to_text.py
from AI_library.chat.gpt3_5 import gpt3_5
from AI_library.chat.gpt4omini import gpt4omini
from AI_library.chat.llama3 import llama3

class TextToText:
    def __init__(self, model, api_key, api_key_for_model=None):
        self.model = model
        self.api_key = api_key
        self.api_key_for_model = api_key_for_model
    
    def process(self, prompt):
        if self.model in ["gpt_3_5", "gpt_4o_mini"]:
            return self._call_openai_api(prompt)
        elif self.model == "llama3":
            return self._call_together_api(prompt)
        else:
            raise ValueError(f"Model {self.model} is not supported.")
    
    def concat(self, model, prompt):
        if model == "llama3":
            return self._call_together_api(prompt)
        elif model in ["gpt_3_5", "gpt_4o_mini"]:
            return self._call_openai_api(prompt)
        else:
            raise ValueError(f"Model {model} is not supported.")
    
    def _call_openai_api(self, prompt):
        if self.model == "gpt_3_5":
            response = gpt3_5(prompt, api_key=self.api_key)
        elif self.model == "gpt_4o_mini":
            response = gpt4omini(prompt, api_key=self.api_key)
        else:
            raise ValueError(f"Model {self.model} is not supported.")
        return response
    
    def _call_together_api(self, prompt):
        if not self.api_key_for_model:
            raise ValueError("API key for Together model must be provided.")
        response = llama3(prompt, api_key=self.api_key_for_model)
        return response
