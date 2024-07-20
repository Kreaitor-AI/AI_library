from openai import OpenAI

class DalleImageGenerator:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    def generate_image(self, prompt, size="1024x1024"):
        response = self.client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size=size,
            quality="standard",
            n=1,
        )
        return response.data[0].url

def dalle(api_key, prompt, size="1024x1024"):
    generator = DalleImageGenerator(api_key)
    return generator.generate_image(prompt, size)
