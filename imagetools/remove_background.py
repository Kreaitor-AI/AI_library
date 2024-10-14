import os
import fal_client

class BackgroundRemovalError(Exception):
    """Custom exception for background removal errors."""

class BackgroundRemover:
    """
    Represents an object that can remove backgrounds from images using the FAL API.
    Parameters:
        - fal_key (str): The API key used to authenticate with the FAL service.
    """

    def __init__(self, fal_key: str):
        os.environ["FAL_KEY"] = fal_key

    def remove_background(self, image_bytes: bytes) -> str:
        """
        Remove the background from an image.

        Args:
            image_bytes (bytes): The bytes of the image to process.

        Returns:
            str: The URL of the processed image with the background removed.

        Raises:
            BackgroundRemovalError: If the background removal fails or no image is returned.
        """
        # Upload the image
        image_url = fal_client.upload_file(image_bytes)

        # Submit a request to remove the background
        handler = fal_client.submit(
            "fal-ai/birefnet",
            arguments={"image_url": image_url}
        )
        result = handler.get()

        if 'image' in result and result['image']['url']:
            return result['image']['url']
        raise BackgroundRemovalError("Background removal failed or no image returned.")

def remove_background(fal_key: str, image_bytes: bytes) -> str:
    """
    Convenience function to remove background from an image.

    Args:
        fal_key (str): The API key for FAL.
        image_bytes (bytes): The bytes of the image to process.

    Returns:
        str: The URL of the processed image with the background removed.

    Raises:
        BackgroundRemovalError: If the background removal fails or no image is returned.
    """
    remover = BackgroundRemover(fal_key)
    return remover.remove_background(image_bytes)
