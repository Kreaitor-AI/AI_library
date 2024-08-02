import requests

class StabilityImageGenerator:
    def __init__(self, api_key):
        self.api_key = api_key
        self.host = "https://api.stability.ai/v2beta/stable-image/generate/sd3"
    
    def generate_image(self, prompt, image=None, model="sd3-medium", mode=None, output_format="jpeg", aspect_ratio="1:1", seed=0, strength=0.75):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "image/*"  # Change to "application/json" if you want JSON base64 response
        }
        
        files = None
        data = {
            "prompt": prompt,
            "model": model,
            "output_format": output_format,
            "aspect_ratio": aspect_ratio,
            "seed": seed
        }
        
        if mode == "image-to-image":
            if image is None:
                raise ValueError("Image is required for image-to-image mode")
            files = {
                "image": open(image, 'rb')
            }
            data.update({
                "strength": strength,
                "mode": "image-to-image"
            })
        else:
            if mode:
                raise ValueError("Mode 'image-to-image' requires an image file")
            data["mode"] = "text-to-image"
        
        response = self._send_request(headers, data, files)
        return response
    
    def _send_request(self, headers, data, files):
        try:
            response = requests.post(self.host, headers=headers, data=data, files=files)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            return response.content
        except requests.HTTPError as http_err:
            raise Exception(f"HTTP error occurred: {http_err}\nResponse Content: {http_err.response.text}")
        except Exception as err:
            raise Exception(f"An error occurred: {err}")

def stability(api_key, prompt, image=None, model="sd3-medium", mode=None, output_format="jpeg", aspect_ratio="1:1", seed=0, strength=0.75):
    generator = StabilityImageGenerator(api_key)
    image_content = generator.generate_image(prompt, image, model, mode, output_format, aspect_ratio, seed, strength)
    
    generated_filename = f"generated_{seed}.{output_format}"
    with open(generated_filename, "wb") as f:
        f.write(image_content)
    
    return generated_filename
