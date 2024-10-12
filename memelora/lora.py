import os
import fal_client

class ImageGenerator:
    """
    A utility class to generate images using a text-to-image API.
    Parameters:
        - fal_key (str): The API key for authenticating requests to the image generation service.
    Processing Logic:
        - Stores the provided API key in an environment variable for subsequent API calls.
    """
    def __init__(self, fal_key):
        # Set the FAL_KEY environment variable with the API key
        os.environ["FAL_KEY"] = fal_key

    def generate_image(self, prompt, lora_path, model_endpoint):
        # Submit the request to the specified model (either LoRA or General)
        """Generate an image based on a text prompt using a specified model endpoint.
        Parameters:
            - prompt (str): The text prompt to guide image generation.
            - lora_path (str): The path to the LoRA parameters.
            - model_endpoint (str): The endpoint URL of the image generation model.
        Returns:
            - str: URL of the generated image.
        Processing Logic:
            - Dynamically selects the model endpoint based on provided `model_endpoint`.
            - Bakes in static parameters such as `num_images`, `image_size`, and `num_inference_steps` while allowing dynamic `prompt` and `lora_path`."""
        handler = fal_client.submit(
            model_endpoint,  # Dynamically choose the endpoint
            arguments={
                "prompt": prompt,  # Use the user-supplied prompt directly
                "loras": [
                    {
                        "path": lora_path
                    }
                ],
                "num_images": 1,
                "image_size": "square_hd",
                "num_inference_steps": 28
            },
        )

        # Get the result from the handler
        result = handler.get()
        if 'images' in result and len(result['images']) > 0:
            return result['images'][0]['url']
        raise Exception("Image generation failed or no image returned.")

# Public function to generate image using the specified model
def lora(fal_key, lora_path, prompt, model_endpoint="fal-ai/flux-lora"):
    """
    Public function to generate an image using either LoRA or General models.
    
    :param fal_key: The FAL API key for authentication.
    :param lora_path: The path to the LoRA model weights (required for all models).
    :param prompt: The user input or description for the image.
    :param model_endpoint: The model endpoint to use ('fal-ai/flux-lora' or 'fal-ai/flux-general').
    :return: URL of the generated image.
    """
    generator = ImageGenerator(fal_key)
    return generator.generate_image(prompt, lora_path, model_endpoint)
