from .gpt3_5 import gpt3_5
from .llama3 import llama3
from .gpt4omini import gpt4omini

MODEL_MAP = {
    "gpt_3_5": gpt3_5,
    "gpt_4omini": gpt4omini,
    "llama3": llama3,
}

class TextToText:
    def __init__(self, model, api_key=None, prompt=None, stream=False):
        self.model = model
        self.api_key = api_key
        self.prompt = prompt
        self.stream = stream

    def process(self, prompt):
        return MODEL_MAP[self.model](prompt, api_key=self.api_key, stream=self.stream)

    def concat(self, next_model, prompt):
        first_output = self.process(self.prompt)
        next_model_instance = TextToText(next_model, api_key=self.api_key, prompt=first_output, stream=self.stream)
        return next_model_instance.process(prompt)

def text_to_text(model, api_key=None, prompt=None, stream=False):
    return TextToText(model, api_key, prompt, stream)
