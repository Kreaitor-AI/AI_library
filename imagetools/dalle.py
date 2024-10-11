from openai import OpenAI
from typing import Optional

class DalleImageGenerator:
    """
    A class to interface with OpenAI's API for generating images using DALL-E.
    Parameters:
        - api_key (str): The API key needed to authenticate with the OpenAI API.
    Processing Logic:
        - The class stores the API client as an instance variable.
        - Throws ValueError if the API response does not contain the expected image data.
    """
    def __init__(self, api_key: str):
        """
        Initialize the DalleImageGenerator with an API key.

        Args:
            api_key (str): The API key for the OpenAI API.
        """
        self.client = OpenAI(api_key=api_key)

    def generate_image(self, prompt: str, size: str = "1024x1024") -> str:
        """
        Generate an image using the DALL-E model.

        Args:
            prompt (str): The prompt to generate the image from.
            size (str): The size of the generated image. Defaults to "1024x1024".

        Returns:
            str: The URL of the generated image.
        
        Raises:
            ValueError: If the API response does not contain image data.
        """
        response = self.client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size=size,
            quality="standard",
            n=1,
        )

        if not response.data or not response.data[0].url:
            raise ValueError("Failed to generate image: No data returned by the API.")

        return response.data[0].url

def dalle(api_key: str, prompt: str, size: str = "1024x1024") -> str:
    """
    Convenience function to generate an image using DALL-E.

    Args:
        api_key (str): The API key for the OpenAI API.
        prompt (str): The prompt to generate the image from.
        size (str): The size of the generated image. Defaults to "1024x1024".

    Returns:
        str: The URL of the generated image.
    """
    generator = DalleImageGenerator(api_key)
    return generator.generate_image(prompt, size)
