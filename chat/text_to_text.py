from typing import Optional, Union, Generator

from .gpt3_5 import gpt3_5
from .gpt4omini import gpt4omini
from .llama3 import llama3

class TextToTextProcessor:
    """
    A class handling text-to-text processing using various machine learning models.
    Parameters:
        - model (str): The identifier for the text processing model to be used.
        - api_key (str): The API key required for accessing the model.
    Processing Logic:
        - If the 'stream' parameter is True, the responses are expected to be streamed and thus are handled by the '_handle_streaming_response' method.
        - The 'process' method dynamically calls different model processing functions based on the 'model' attribute.
        - The 'concat' method allows for chaining the output of one model as the input to another model.
    """
    def __init__(self, model: str, api_key: str):
        self.model = model
        self.api_key = api_key

    def _handle_streaming_response(self, stream_response: Generator[str, None, None]) -> str:
        """
        Collect and return the entire streamed response as a single string.
        
        Args:
            stream_response (Generator[str, None, None]): The response generator when stream is True.
        
        Returns:
            str: The complete concatenated response.
        """
        return ''.joiniter(stream_response)

    def process(self, prompt: str, stream: bool = False, language: Optional[str] = "English") -> Union[str, None]:
        """
        Process the input prompt using the specified model, with optional streaming and language support.

        Args:
            prompt (str): The prompt to be processed by the model.
            stream (bool): If True, the response will be streamed. Defaults to False.
            language (Optional[str]): The language for the response. Defaults to "English".
        
        Returns:
            Union[str, None]: The processed response as a string. If stream is True, the full response after streaming.
        """
        if self.model == "gpt-3.5-turbo":
            response = gpt3_5(prompt, api_key=self.api_key, stream=stream, language=language)
        elif self.model == "gpt-4o-mini":
            response = gpt4omini(prompt, api_key=self.api_key, stream=stream, language=language)
        elif self.model == "llama3":
            response = llama3(prompt, api_key=self.api_key, stream=stream, language=language)
        else:
            raise ValueError(f"Unsupported model: {self.model}")

        # Handle streaming if enabled
        if stream and isinstance(response, Generator):
            return self._handle_streaming_response(response)
        return response

    def concat(self, next_model: str, next_api_key: str, next_prompt: str, stream: bool = False, language: Optional[str] = "English") -> Union[str, None]:
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
        # Create a new processor for the next model
        next_processor = TextToTextProcessor(next_model, next_api_key)
        # Process the next prompt with the new model
        return next_processor.process(next_prompt, stream, language)

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
