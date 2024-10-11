import asyncio
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.callbacks import AsyncIteratorCallbackHandler, StreamingStdOutCallbackHandler
from typing import Optional, AsyncIterator, Union

class GPT4ominiClient:
    """
    Provides asynchronous interaction with GPT-4o-mini for chat completions.
    Parameters:
        - api_key (Optional[str]): The API key used to authenticate with the OpenAI API.
    Processing Logic:
        - Uses asyncio for managing asynchronous tasks.
        - Employs a PromptTemplate to format input before sending it to the model.
        - Utilizes a callback handling mechanism to stream response tokens.
        - Chains components using the pipe (|) operator to create a processing pipeline.
    """
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the GPT4ominiClient with an optional API key.
        Args:
            api_key (Optional[str]): The API key for OpenAI. Defaults to None.
        """
        self.api_key = api_key

    async def chat_completion_stream(self, prompt: str, language: str = "English") -> AsyncIterator[str]:
        """
        Generate a chat completion using the GPT-4o-mini model with streaming.
        Args:
            prompt (str): The prompt to send to the model.
            language (str): The language for the response. Defaults to "English".
        Returns:
            AsyncIterator[str]: An iterator yielding the tokens as they are received.
        """
        prompt_template = PromptTemplate(
            template="Respond to the following prompt in {language}:\n\n{prompt}",
            input_variables=["prompt", "language"]
        )
        callback = AsyncIteratorCallbackHandler()

        llm = ChatOpenAI(
            openai_api_key=self.api_key,
            model="gpt-4o-mini",
            streaming=True,
            callbacks=[callback]
        )

        chain = prompt_template | llm
        inputs = {"prompt": prompt, "language": language}
        task = asyncio.create_task(chain.ainvoke(inputs))

        async for token in callback.aiter():
            yield token

        await task

    async def chat_completion(self, prompt: str, language: Optional[str] = "English") -> str:
        """
        Generate a chat completion using the GPT-4o-mini model without streaming.
        Args:
            prompt (str): The prompt to send to the model.
            language (Optional[str]): The language for the response. Defaults to "English".
        Returns:
            str: The model's response.
        """
        prompt_template = PromptTemplate(
            template="Please respond entirely in {language}. Here is the prompt: {prompt}",
            input_variables=["prompt", "language"]
        )

        llm = ChatOpenAI(
            openai_api_key=self.api_key,
            model="gpt-4o-mini",
            streaming=False
        )

        chain = prompt_template | llm
        response = await chain.ainvoke({"prompt": prompt, "language": language})
        return response.content.strip()

async def stream_gpt4omini(prompt: str, api_key: Optional[str] = None, language: Optional[str] = "English") -> AsyncIterator[str]:
    """
    Asynchronous function to generate streaming chat completion with GPT-4o-mini.
    Args:
        prompt (str): The prompt to send to the model.
        api_key (Optional[str]): The API key for OpenAI. Defaults to None.
        language (Optional[str]): The language for the response. Defaults to "English".
    Returns:
        AsyncIterator[str]: An iterator yielding the tokens as they are received.
    """
    client = GPT4ominiClient(api_key)
    async for chunk in client.chat_completion_stream(prompt, language):
        yield chunk

async def non_stream_gpt4omini(prompt: str, api_key: Optional[str] = None, language: Optional[str] = "English") -> str:
    """
    Asynchronous function to generate non-streaming chat completion with GPT-4o-mini.
    Args:
        prompt (str): The prompt to send to the model.
        api_key (Optional[str]): The API key for OpenAI. Defaults to None.
        language (Optional[str]): The language for the response. Defaults to "English".
    Returns:
        str: The model's response.
    """
    client = GPT4ominiClient(api_key)
    return await client.chat_completion(prompt, language)
