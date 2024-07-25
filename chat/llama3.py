from together import Together
from typing import Optional, Generator

class Llama3Client:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        if not self.api_key:
            raise ValueError("API key must be provided or set as TOGETHER_API_KEY environment variable")
        self.client = Together(api_key=self.api_key)

    def get_response(self, prompt: str, stream: bool = False) -> str | Generator[str, None, None]:
        messages = [{"role": "user", "content": prompt}]
        model = "meta-llama/Llama-3-70b-chat-hf"
        if stream:
            return self._stream_response(model, messages)
        else:
            return self._non_stream_response(model, messages)

    def _stream_response(self, model: str, messages: list) -> Generator[str, None, None]:
        stream_response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            stream=True
        )
        for chunk in stream_response:
            content = chunk.choices[0].delta.content or ""
            yield content

    def _non_stream_response(self, model: str, messages: list) -> str:
        response = self.client.chat.completions.create(
            model=model,
            messages=messages
        )
        return response.choices[0].message.content

def llama3(prompt: str, api_key: Optional[str] = None, stream: bool = False) -> str | Generator[str, None, None]:
    client = Llama3Client(api_key)
    return client.get_response(prompt, stream)
    
