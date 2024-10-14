import os
import fal_client

class ImageUpscalerError(Exception):
    """Custom exception for image upscaling errors."""

class ImageUpscaler:
    """
    Represents an object that can upscale images using the FAL API.
    Parameters:
        - fal_key (str): The API key used to authenticate with the FAL service.
    """

    def __init__(self, fal_key: str):
        os.environ["FAL_KEY"] = fal_key

    def upscale_image(self, image_bytes: bytes) -> str:
        """
        Upscale an image.

        Args:
            image_bytes (bytes): The bytes of the image to upscale.

        Returns:
            str: The URL of the upscaled image.

        Raises:
            ImageUpscalerError: If the upscaling fails or no image is returned.
        """
        # Upload the image
        image_url = fal_client.upload_file(image_bytes)

        # Submit a request to upscale the image
        handler = fal_client.submit(
            "fal-ai/clarity-upscaler",
            arguments={"image_url": image_url}
        )
        result = handler.get()

        if 'image' in result and result['image']['url']:
            return result['image']['url']
        raise ImageUpscalerError("Image upscaling failed or no image returned.")

def upscale_image(fal_key: str, image_bytes: bytes) -> str:
    """
    Convenience function to upscale an image.

    Args:
        fal_key (str): The API key for FAL.
        image_bytes (bytes): The bytes of the image to upscale.

    Returns:
        str: The URL of the upscaled image.

    Raises:
        ImageUpscalerError: If the upscaling fails or no image is returned.
    """
    upscaler = ImageUpscaler(fal_key)
    return upscaler.upscale_image(image_bytes)
