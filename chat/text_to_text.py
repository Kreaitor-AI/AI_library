from typing import Optional, Union, Generator, Callable
from .gpt3_5 import gpt3_5
from .gpt4omini import gpt4omini
from .llama3 import llama3

class TextToTextProcessor:
    def __init__(self, model: str, api_key: str):
        self.model = model
        self.api_key = api_key

    def _handle_streaming_response(self, stream_response: Union[str, Generator[str, None, None]]) -> str:
        # Collect the entire streamed response
        if isinstance(stream_response, Generator):
            response = ''.join(chunk for chunk in stream_response)
        else:
            response = stream_response
        return response

    def process(self, prompt: str, stream: bool = False) -> Union[str, Generator[str, None, None]]:
        if self.model == "gpt-3.5-turbo":
            return gpt3_5(prompt, api_key=self.api_key, stream=stream)
        elif self.model == "gpt-4o-mini":
            return gpt4omini(prompt, api_key=self.api_key, stream=stream)
        elif self.model == "llama3":
            response = llama3(prompt, api_key=self.api_key, stream=stream)
            if stream:
                return self._handle_streaming_response(response)
            return response
        else:
            raise ValueError(f"Unsupported model: {self.model}")

    def concat(self, next_model: str, next_api_key: str, next_prompt: str, stream: bool = False) -> Union[str, Generator[str, None, None]]:
        next_processor = TextToTextProcessor(next_model, next_api_key)
        return next_processor.process(next_prompt, stream)

def text_to_text(model: str, api_key: str) -> TextToTextProcessor:
    return TextToTextProcessor(model, api_key)
