import os
import fal_client
from typing import Optional


class BackgroundRemovalError(Exception):
    """Custom exception for background removal errors."""


class BackgroundRemover:
    """
    Represents an object that can remove the background from an image using the FAL API.
    
    Parameters:
        - fal_key (str): The API key used to authenticate with the FAL service.
    
    Processing Logic:
        - Upon initialization, the FAL API key is stored in an environment variable.
        - The `remove_background` method submits a request to the FAL server to remove the background of the image.
        - If the result contains a valid image, the URL of the processed image is returned.
        - An exception is raised if the request fails or no image is returned.
    """
    
    def __init__(self, fal_key: str):
        """
        Initialize the BackgroundRemover with the FAL API key.

        Args:
            fal_key (str): The API key for FAL.
        """
        os.environ["FAL_KEY"] = fal_key

    def remove_background(self, image_url: str, model: str = "General Use (Light)", 
                          operating_resolution: str = "1024x1024", output_format: str = "png") -> str:
        """
        Remove the background from an image using the FAL API.

        Args:
            image_url (str): The URL of the image from which to remove the background.
            model (str): The model to use for background removal (default is "General Use (Light)").
            operating_resolution (str): The resolution to operate on (default is "1024x1024").
            output_format (str): The format of the output image (default is "png").

        Returns:
            str: The URL of the processed image.

        Raises:
            BackgroundRemovalError: If background removal fails or no image is returned.
        """
        try:
            handler = fal_client.submit(
                "fal-ai/birefnet",
                arguments={
                    "image_url": image_url,
                    "model": model,
                    "operating_resolution": operating_resolution,
                    "output_format": output_format
                },
            )
            result = handler.get()

            if result.get('image') and result['image'].get('url'):
                return result['image']['url']
            raise BackgroundRemovalError("Background removal failed or no image returned.")
        except Exception as e:
            raise BackgroundRemovalError(f"Background removal error: {str(e)}")


def remove_background(fal_key: str, image_url: str) -> str:
    """
    Convenience function to remove background from an image using the FAL API.

    Args:
        fal_key (str): The API key for FAL.
        image_url (str): The URL of the image to remove the background from.

    Returns:
        str: The URL of the image with the background removed.

    Raises:
        BackgroundRemovalError: If background removal fails or no image is returned.
    """
    remover = BackgroundRemover(fal_key)
    return remover.remove_background(image_url)
