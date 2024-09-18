from typing import Optional, Union, Generator
from .gpt3_5 import gpt3_5
from .gpt4omini import gpt4omini
from .llama3 import llama3
import asyncio

class TextToTextProcessor:
    def __init__(self, model: str, api_key: str):
        """
        Args:
            model (str): The model to be used (e.g., "gpt-3.5-turbo", "llama3").
            api_key (str): The API key for the chosen model.
        """
        self.model = model
        self.api_key = api_key

    async def _handle_streaming_response(self, stream_response: Generator[str, None, None]) -> str:
        """
        Args:
            stream_response (Generator[str, None, None]): The response generator when stream is True.

        Returns:
            str: The complete concatenated response from the streamed output.
        """
        return ''.join(chunk async for chunk in stream_response)

    async def process(self, prompt: str, stream: bool = False, language: Optional[str] = "English") -> Union[str, None]:
        """
        Process the input prompt using the specified model, with optional streaming and language support.

        Args:
            prompt (str): The prompt to be processed by the model.
            stream (bool): If True, the response will be streamed. Defaults to False.
            language (Optional[str]): The language for the response. Defaults to "English".
        
        Returns:
            Union[str, None]: The processed response as a string, or full response after streaming.
        """
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
        """
        Concatenate another model's response with the current context and generate a response.
        
        Args:
            next_model (str): The next model to use.
            next_api_key (str): API key for the next model.
            next_prompt (str): Prompt for the next model.
            stream (bool): If True, the response will be streamed. Defaults to False.
            language (Optional[str]): The language for the response. Defaults to "English".
        
        Returns:
            Union[str, None]: The processed response from the next model.
        """
        next_processor = TextToTextProcessor(next_model, next_api_key)
        return await next_processor.process(next_prompt, stream, language)

def text_to_text(model: str, api_key: str) -> TextToTextProcessor:
    """
    Factory function to initialize a TextToTextProcessor.
    
    Args:
        model (str): The model to be used (e.g., "gpt-3.5-turbo", "llama3").
        api_key (str): The API key for the chosen model.
    
    Returns:
        TextToTextProcessor: An initialized processor for the given model.
    """
    return TextToTextProcessor(model, api_key)
