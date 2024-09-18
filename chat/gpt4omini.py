import asyncio
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from typing import Optional

class GPT4ominiClient:
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the GPT4ominiClient with an optional API key.

        Args:
            api_key (Optional[str]): The API key for OpenAI. Defaults to None.
        """
        self.api_key = api_key

    async def chat_completion(self, prompt: str, stream: bool = False, language: Optional[str] = "English") -> Optional[str]:
        """
        Generate a chat completion using the GPT-4o-mini model asynchronously.

        Args:
            prompt (str): The prompt to send to the model.
            stream (bool): Whether to stream the output. Defaults to False.
            language (Optional[str]): The language for the response. Defaults to "English".

        Returns:
            Optional[str]: The model's response if streaming is disabled, otherwise None.
        """
        # Modified template to include the language parameter
        prompt_template = PromptTemplate(
            template="Please respond entirely in {language}. Here is the prompt: {prompt}",
            input_variables=["prompt", "language"]
        )
        callbacks = [StreamingStdOutCallbackHandler()] if stream else None

        llm = ChatOpenAI(
            openai_api_key=self.api_key,
            model="gpt-4o-mini",
            streaming=stream,
            callbacks=callbacks
        )

        result = prompt_template | llm

        # Asynchronous call to invoke the model
        response = await result.ainvoke({"prompt": prompt, "language": language})

        if not stream:
            return response.content.strip()

async def gpt4omini(prompt: str, api_key: Optional[str] = None, stream: bool = False, language: Optional[str] = "English") -> Optional[str]:
    """
    Asynchronous function to generate chat completion with GPT-4o-mini.

    Args:
        prompt (str): The prompt to send to the model.
        api_key (Optional[str]): The API key for OpenAI. Defaults to None.
        stream (bool): Whether to stream the output. Defaults to False.
        language (Optional[str]): The language for the response. Defaults to "English".

    Returns:
        Optional[str]: The model's response if streaming is disabled, otherwise None.
    """
    client = GPT4ominiClient(api_key)
    return await client.chat_completion(prompt, stream, language)
