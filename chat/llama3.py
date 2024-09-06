import os
from together import Together
from typing import Optional

class Llama3Client:
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Llama3Client with an optional API key.

        Args:
            api_key (Optional[str]): The API key for Together API. Defaults to environment variable 'TOGETHER_API_KEY'.
        """
        self.api_key = api_key or os.environ.get("TOGETHER_API_KEY")
        self.client = Together(api_key=self.api_key)

    def get_response(self, prompt: str, stream: bool = False) -> Optional[str]:
        """
        Generate a response using the Llama-3 model.

        Args:
            prompt (str): The prompt to send to the model.
            stream (bool): Whether to stream the output. Defaults to False.

        Returns:
            Optional[str]: The model's response if streaming is disabled, otherwise None.
        """
        if stream:
            # Streaming mode
            stream_response = self.client.chat.completions.create(
                model="meta-llama/Llama-3-70b-chat-hf",
                messages=[{"role": "user", "content": prompt}],
                stream=True
            )

            # Print streaming response
            for chunk in stream_response:
                content = chunk.choices[0].delta.content or ""
                print(content, end="", flush=True)
        else:
            # Non-streaming mode
            response = self.client.chat.completions.create(
                model="meta-llama/Llama-3-70b-chat-hf",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content

def llama3(prompt: str, api_key: Optional[str] = None, stream: bool = False) -> Optional[str]:
    """
    Convenience function to generate a response using the Llama-3 model.

    Args:
        prompt (str): The prompt to send to the model.
        api_key (Optional[str]): The API key for Together API. Defaults to None.
        stream (bool): Whether to stream the output. Defaults to False.

    Returns:
        Optional[str]: The model's response if streaming is disabled, otherwise None.
    """
    client = Llama3Client(api_key)
    return client.get_response(prompt, stream)
