import os
import fal_client

class ImageGenerator:
    def __init__(self, fal_key):
        # Set the FAL_KEY environment variable with the API key
        os.environ["FAL_KEY"] = fal_key

    def generate_image(self, prompt):
        handler = fal_client.submit(
            "fal-ai/flux/schnell",
            arguments={"prompt": prompt},
        )
        result = handler.get()
        if 'images' in result and len(result['images']) > 0:
            return result['images'][0]['url']
        else:
            raise Exception("Image generation failed or no image returned.")

def flux(fal_key, prompt):
    generator = ImageGenerator(fal_key)
    return generator.generate_image(prompt)
