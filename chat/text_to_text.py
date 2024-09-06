from typing import Optional, Union, Generator
from .gpt3_5 import gpt3_5
from .gpt4omini import gpt4omini
from .llama3 import llama3

class TextToTextProcessor:
    def __init__(self, model: str, api_key: str):
        """
        Initialize the TextToTextProcessor with a specified model and API key.

        Args:
            model (str): The name of the model to use ("gpt-3.5-turbo", "gpt-4o-mini", or "llama3").
            api_key (str): The API key for authentication with the model.
        """
        self.model = model
        self.api_key = api_key

    def _handle_streaming_response(self, stream_response: Generator[str, None, None]) -> str:
        """
        Collect and concatenate the entire streamed response.

        Args:
            stream_response (Generator[str, None, None]): The generator yielding streamed response chunks.

        Returns:
            str: The concatenated response.
        """
        return ''.join(chunk for chunk in stream_response)

    def process(self, prompt: str, stream: bool = False) -> Union[str, Generator[str, None, None]]:
        """
        Process a prompt using the selected model.

        Args:
            prompt (str): The input prompt to process.
            stream (bool): Whether to stream the response. Defaults to False.

        Returns:
            Union[str, Generator[str, None, None]]: The response from the model, either as a full string or a generator for streaming.
        """
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
        """
        Process a prompt using a different model, chaining the outputs.

        Args:
            next_model (str): The name of the next model to use.
            next_api_key (str): The API key for the next model.
            next_prompt (str): The input prompt to process with the next model.
            stream (bool): Whether to stream the response. Defaults to False.

        Returns:
            Union[str, Generator[str, None, None]]: The response from the next model, either as a full string or a generator for streaming.
        """
        next_processor = TextToTextProcessor(next_model, next_api_key)
        return next_processor.process(next_prompt, stream)

def text_to_text(model: str, api_key: str) -> TextToTextProcessor:
    """
    Create a TextToTextProcessor for the specified model and API key.

    Args:
        model (str): The name of the model to use ("gpt-3.5-turbo", "gpt-4o-mini", or "llama3").
        api_key (str): The API key for authentication with the model.

    Returns:
        TextToTextProcessor: An instance of the TextToTextProcessor class.
    """
    return TextToTextProcessor(model, api_key)
