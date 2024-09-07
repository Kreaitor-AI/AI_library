import os
from together import Together
from typing import Optional, List

class Llama3Client:
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Llama3Client with an optional API key.

        Args:
            api_key (Optional[str]): The API key for Together API. Defaults to environment variable 'TOGETHER_API_KEY'.
        """
        self.api_key = api_key or os.environ.get("TOGETHER_API_KEY")
        if not self.api_key:
            raise ValueError("API key is required for Together API.")
        self.client = Together(api_key=self.api_key)

    def get_response(self, prompt: str, stream: bool = False) -> Optional[str]:
        """
        Generate a response using the Llama-3 model.

        Args:
            prompt (str): The prompt to send to the model.
            stream (bool): Whether to stream the output. Defaults to False.

        Returns:
            Optional[str]: The model's response if streaming is disabled, otherwise the collected stream.
        """
        if stream:
            # Streaming mode
            try:
                stream_response = self.client.chat.completions.create(
                    model="meta-llama/Llama-3-70b-chat-hf",
                    messages=[{"role": "user", "content": prompt}],
                    stream=True
                )

                # Collect the stream response chunks
                collected_response = []
                for chunk in stream_response:
                    content = chunk.choices[0].delta.content or ""
                    print(content, end="", flush=True)
                    collected_response.append(content)

                # Return the full collected response
                return ''.join(collected_response)
            except Exception as e:
                print(f"Error occurred during streaming: {e}")
                return None
        else:
            # Non-streaming mode
            try:
                response = self.client.chat.completions.create(
                    model="meta-llama/Llama-3-70b-chat-hf",
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.choices[0].message.content
            except Exception as e:
                print(f"Error occurred during non-streaming response: {e}")
                return None

def llama3(prompt: str, api_key: Optional[str] = None, stream: bool = False) -> Optional[str]:
    """
    Convenience function to generate a response using the Llama-3 model.

    Args:
        prompt (str): The prompt to send to the model.
        api_key (Optional[str]): The API key for Together API. Defaults to None.
        stream (bool): Whether to stream the output. Defaults to False.

    Returns:
        Optional[str]: The model's response if streaming is disabled, or the collected stream if enabled.
    """
    client = Llama3Client(api_key)
    return client.get_response(prompt, stream)
