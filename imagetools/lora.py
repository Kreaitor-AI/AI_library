import torch
from diffusers import StableDiffusion3Pipeline

class ImageGenerator:
    def __init__(self, model_name="stabilityai/stable-diffusion-3-medium-diffusers", 
                 lora_weights_path=None, device="cuda", torch_dtype=torch.float16, 
                 text_encoder_3=None, tokenizer_3=None):
        
        # Initialize the Stable Diffusion pipeline with optional parameters
        self.pipe = StableDiffusion3Pipeline.from_pretrained(
            model_name,
            text_encoder_3=text_encoder_3, 
            tokenizer_3=tokenizer_3, 
            torch_dtype=torch_dtype
        ).to(device)
        
        # Load LoRA weights if provided
        if lora_weights_path:
            self.pipe.load_lora_weights(lora_weights_path)
    
    def generate_image(self, prompt):
        # Generate the image using the prompt and LoRA weights
        image = self.pipe(prompt=prompt).images[0]
        return image

# Utility function to simplify usage
def lora(model_name="stabilityai/stable-diffusion-3-medium-diffusers", prompt="", lora_weights_path=None, 
         device="cuda", torch_dtype=torch.float16, text_encoder_3=None, tokenizer_3=None):
    
    generator = ImageGenerator(
        model_name=model_name, 
        lora_weights_path=lora_weights_path,
        device=device, 
        torch_dtype=torch_dtype,
        text_encoder_3=text_encoder_3,
        tokenizer_3=tokenizer_3
    )
    
    return generator.generate_image(prompt=prompt)
