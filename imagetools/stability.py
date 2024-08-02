import requests

class StabilityImageGenerator:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.stability.ai/v2beta/stable-image/generate/sd3"
    
    def generate_image(self, prompt, image=None, strength=None, mode="text-to-image", 
                       aspect_ratio="1:1", model="sd3-large", output_format="png", 
                       seed=0, negative_prompt=None):
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json"  # You can change this to "image/*" if you want the image directly
        }
        
        files = {}
        if image:
            files = {
                "image": image
            }
        
        data = {
            "prompt": prompt,
            "mode": mode,
            "aspect_ratio": aspect_ratio,
            "model": model,
            "output_format": output_format,
            "seed": seed,
            "negative_prompt": negative_prompt
        }
        
        if strength is not None:
            data["strength"] = strength
        
        response = requests.post(self.base_url, headers=headers, files=files, data=data)
        
        if response.status_code == 200:
            return response.json() if headers["Accept"] == "application/json" else response.content
        else:
            print(f"Error: {response.status_code}")
            print(f"Response content: {response.content.decode('utf-8')}")
            response.raise_for_status()

def stability(api_key, prompt, image=None, strength=None, mode="text-to-image", 
              aspect_ratio="1:1", model="sd3-large", output_format="png", 
              seed=0, negative_prompt=None):
    generator = StabilityImageGenerator(api_key)
    return generator.generate_image(prompt, image, strength, mode, aspect_ratio, model, 
                                    output_format, seed, negative_prompt)
