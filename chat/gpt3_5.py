import asyncio
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from typing import Optional

class GPT3_5TurboClient:
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the GPT3_5TurboClient with an optional API key.

        Args:
            api_key (Optional[str]): The API key for OpenAI. Defaults to None.
        """
        self.api_key = api_key

    async def chat_completion(self, prompt: str, stream: bool = False, language: Optional[str] = "English") -> Optional[str]:
        """
        Generate a chat completion using the GPT-3.5-turbo model asynchronously.

        Args:
            prompt (str): The prompt to send to the model.
            stream (bool): Whether to stream the output. Defaults to False.
            language (Optional[str]): The language for the response. Defaults to "English".

        Returns:
            Optional[str]: The model's response if streaming is disabled, otherwise None.
        """
        prompt_template = PromptTemplate(
            template="Please respond strictly in {language} without using other languages: {prompt}",
            input_variables=["prompt", "language"]
        )
        callbacks = [StreamingStdOutCallbackHandler()] if stream else None

        llm = ChatOpenAI(
            openai_api_key=self.api_key,
            model="gpt-3.5-turbo",
            streaming=stream,
            callbacks=callbacks
        )

        result = prompt_template | llm

        # Asynchronous call to invoke the model
        response = await result.ainvoke({"prompt": prompt, "language": language})

        if not stream:
            return response.content.strip()

async def gpt3_5(prompt: str, api_key: Optional[str] = None, stream: bool = False, language: Optional[str] = "English") -> Optional[str]:
    """
    Asynchronous function to generate chat completion with GPT-3.5-turbo.

    Args:
        prompt (str): The prompt to send to the model.
        api_key (Optional[str]): The API key for OpenAI. Defaults to None.
        stream (bool): Whether to stream the output. Defaults to False.
        language (Optional[str]): The language for the response. Defaults to "English".

    Returns:
        Optional[str]: The model's response if streaming is disabled, otherwise None.
    """
    client = GPT3_5TurboClient(api_key)
    return await client.chat_completion(prompt, stream, language)
