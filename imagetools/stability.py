import requests

class StabilityImageGenerator:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.stability.ai/v2beta/stable-image/generate/sd3"
        self.headers = {
            "authorization": f"Bearer {self.api_key}"
        }
    
    def generate_image(self, prompt, aspect_ratio="1:1", model="sd3-medium", seed=0, output_format="png", negative_prompt=None):
        data = {
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "model": model,
            "seed": seed,
            "output_format": output_format
        }
        
        if negative_prompt:
            data['negative_prompt'] = negative_prompt
        
        response = requests.post(
            self.base_url,
            headers=self.headers,
            data=data
        )
        
        if response.status_code == 200:
            return response.content
        else:
            raise Exception(str(response.json()))
    
    def save_image(self, image_content, file_path):
        with open(file_path, 'wb') as file:
            file.write(image_content)

def stability(api_key, prompt, aspect_ratio="1:1", model="sd3-large", seed=0, output_format="png", negative_prompt=None, file_path="output_image.png"):
    generator = StabilityImageGenerator(api_key)
    image_content = generator.generate_image(
        prompt=prompt,
        aspect_ratio=aspect_ratio,
        model=model,
        seed=seed,
        output_format=output_format,
        negative_prompt=negative_prompt
    )
    generator.save_image(image_content, file_path)
    return file_path
