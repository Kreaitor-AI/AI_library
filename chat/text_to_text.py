from typing import Optional, Union, Generator
from .gpt3_5 import gpt3_5
from .gpt4omini import gpt4omini
from .llama3 import llama3
import asyncio

class TextToTextProcessor:
    def __init__(self, model: str, api_key: str):
        self.model = model
        self.api_key = api_key

    async def _handle_streaming_response(self, stream_response: Generator[str, None, None]) -> str:
        return ''.join(chunk async for chunk in stream_response)

    async def process(self, prompt: str, stream: bool = False, language: Optional[str] = "English") -> Union[str, None]:
        if self.model == "gpt-3.5-turbo":
            response = await gpt3_5(prompt, api_key=self.api_key, stream=stream, language=language)
        elif self.model == "gpt-4o-mini":
            response = await gpt4omini(prompt, api_key=self.api_key, stream=stream, language=language)
        elif self.model == "llama3":
            response = await llama3(prompt, api_key=self.api_key, stream=stream, language=language)
        else:
            raise ValueError(f"Unsupported model: {self.model}")

        if stream and isinstance(response, Generator):
            return await self._handle_streaming_response(response)
        return response

    async def concat(self, next_model: str, next_api_key: str, next_prompt: str, stream: bool = False, language: Optional[str] = "English") -> Union[str, None]:
        next_processor = TextToTextProcessor(next_model, next_api_key)
        return await next_processor.process(next_prompt, stream, language)

def text_to_text(model: str, api_key: str) -> TextToTextProcessor:
    return TextToTextProcessor(model, api_key)
