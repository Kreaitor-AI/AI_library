import os
import fal_client
from typing import Optional

class ImageGenerationError(Exception):
    """Custom exception for image generation errors."""


class ImageGenerator:
    """
    Represents an object that can generate images using the FAL API.
    Parameters:
        - fal_key (str): The API key used to authenticate with the FAL service.
    Processing Logic:
        - Upon initialization, the FAL API key is stored in an environment variable.
        - The `generate_image` method submits a request to the FAL server and waits for the result.
        - If the result contains images, the URL of the first image is returned.
        - An exception is raised if no images are generated or returned.
    """
    def __init__(self, fal_key: str):
        """
        Initialize the ImageGenerator with the FAL API key.

        Args:
            fal_key (str): The API key for FAL.
        """
        os.environ["FAL_KEY"] = fal_key

    def generate_image(self, prompt: str) -> str:
        """
        Generate an image using the FAL API.

        Args:
            prompt (str): The prompt to generate the image from.

        Returns:
            str: The URL of the generated image.

        Raises:
            ImageGenerationError: If image generation fails or no image is returned.
        """
        handler = fal_client.submit(
            "fal-ai/flux/schnell",
            arguments={"prompt": prompt},
        )
        result = handler.get()

        if result.get('images') and len(result['images']) > 0:
            return result['images'][0]['url']
        raise ImageGenerationError("Image generation failed or no image returned.")

def flux(fal_key: str, prompt: str) -> str:
    """
    Convenience function to generate an image using the FAL API.

    Args:
        fal_key (str): The API key for FAL.
        prompt (str): The prompt to generate the image from.

    Returns:
        str: The URL of the generated image.

    Raises:
        ImageGenerationError: If image generation fails or no image is returned.
    """
    generator = ImageGenerator(fal_key)
    return generator.generate_image(prompt)
