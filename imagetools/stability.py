import requests

class StabilityImageGenerator:
    def __init__(self, api_key):
        self.api_key = api_key
        self.host = "https://api.stability.ai/v2beta/stable-image/generate/sd3"
    
    def generate_image(self, prompt, image=None, model="sd3-medium", mode=None, output_format="jpeg", aspect_ratio="1:1", seed=0, strength=0.75):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "image/*",
        }
        
        params = {
            "prompt": prompt,
            "seed": seed,
            "output_format": output_format,
            "model": model,
        }

        if mode == "image-to-image":
            if image is None:
                raise ValueError("Image is required for image-to-image mode")
            params.update({
                "strength": strength,
            })
            files = {"image": open(image, 'rb')}
        else:
            if mode:
                raise ValueError("Mode 'image-to-image' requires an image file")
            files = None
        
        response = self._send_request(headers, params, files)
        return response
    
    def _send_request(self, headers, params, files):
        try:
            response = requests.post(self.host, headers=headers, params=params, files=files)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            return response.content
        except requests.HTTPError as http_err:
            raise Exception(f"HTTP error occurred: {http_err}")
        except Exception as err:
            raise Exception(f"An error occurred: {err}")

def stability(api_key, prompt, image=None, model="sd3-medium", mode=None, output_format="jpeg", aspect_ratio="1:1", seed=0, strength=0.75):
    generator = StabilityImageGenerator(api_key)
    image_content = generator.generate_image(prompt, image, model, mode, output_format, aspect_ratio, seed, strength)
    
    generated_filename = f"generated_{seed}.{output_format}"
    with open(generated_filename, "wb") as f:
        f.write(image_content)
    
    return generated_filename
