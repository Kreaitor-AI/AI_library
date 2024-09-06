import os
import fal_client
from chat import llama3  # Assuming llama3 is the model used for prompt generation

class ImageGenerator:
    def __init__(self, fal_key):
        # Set the FAL_KEY environment variable with the API key
        os.environ["FAL_KEY"] = fal_key

    def generate_image(self, prompt, lora_path, together_api_key, model_endpoint):
        # Generate the final prompt using llama3
        llama_prompt = llama3(prompt=prompt, api_key=together_api_key)

        # Submit the request to the specified model (either LoRA or General)
        handler = fal_client.submit(
            model_endpoint,  # Dynamically choose the endpoint
            arguments={
                "prompt": llama_prompt,  # Use the formatted llama3 prompt
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
        else:
            raise Exception("Image generation failed or no image returned.")

# Public function to generate image using the specified model
def lora(fal_key, lora_path, prompt, together_api_key, model_endpoint="fal-ai/flux-lora"):
    """
    Public function to generate an image using either LoRA or General models.
    
    :param fal_key: The FAL API key for authentication.
    :param lora_path: The path to the LoRA model weights (required for all models).
    :param prompt: The user input or description for the image.
    :param together_api_key: The API key for the llama3 model to generate the prompt.
    :param model_endpoint: The model endpoint to use ('fal-ai/flux-lora' or 'fal-ai/flux-general').
    :return: URL of the generated image.
    """
    generator = ImageGenerator(fal_key)
    return generator.generate_image(prompt, lora_path, together_api_key, model_endpoint)
