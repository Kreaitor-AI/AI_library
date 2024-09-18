import os
import asyncio
from together import Together
from typing import Optional

class Llama3Client:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("TOGETHER_API_KEY")
        if not self.api_key:
            raise ValueError("API key is required for Together API.")
        self.client = Together(api_key=self.api_key)

    async def get_response(self, prompt: str, stream: bool = False, language: Optional[str] = "English") -> Optional[str]:
        if language and language != "English":
            prompt = f"Please respond in {language}: {prompt}"

        if stream:
            try:
                stream_response = await self.client.chat.completions.create(
                    model="meta-llama/Llama-3-70b-chat-hf",
                    messages=[{"role": "user", "content": prompt}],
                    stream=True
                )
                collected_response = []
                async for chunk in stream_response:
                    content = chunk.choices[0].delta.content or ""
                    collected_response.append(content)
                return ''.join(collected_response)
            except Exception:
                return None
        else:
            try:
                response = await self.client.chat.completions.create(
                    model="meta-llama/Llama-3-70b-chat-hf",
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.choices[0].message.content
            except Exception:
                return None

async def llama3(prompt: str, api_key: Optional[str] = None, stream: bool = False, language: Optional[str] = "English") -> Optional[str]:
    client = Llama3Client(api_key)
    return await client.get_response(prompt, stream, language)
