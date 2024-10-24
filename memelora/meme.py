from imagetools import flux
from memelora import lora
from chat import gpt4omini
from src.config import Config
from typing import Optional, Dict

class GenerateImage:
    """
    Handles the generation of images based on character configuration using specified prompts and models.
    Parameters:
        - character_name (str): Identifier for the character configuration to use.
        - user_prompt (str): The base user prompt used for image generation.
        - prompt_template (str): A template string that incorporates the user prompt into a full prompt.
    Processing Logic:
        - Customizes prompt generation based on input and a predefined template.
        - Determines the appropriate model endpoint and weights for the character from a configuration mapping.
        - Supports optional model weights path for the image generation request.
        - Falls back to a default configuration if the character is not present in the mapping.
    """
    CHARACTER_CONFIG: Dict[str, Dict[str, Optional[str]]] = {
        "ginnan": {
            "model_endpoint": "fal-ai/flux-lora",
            "lora_path": "https://storage.googleapis.com/fal-flux-lora/80dfafdbca9f4bbc868cbeac916bc1d2_pytorch_lora_weights.safetensors"
        },
        "neiro_test_dev": {
            "model_endpoint": "fal-ai/flux-lora",
            "lora_path": "https://storage.googleapis.com/fal-flux-lora/3f298811f2714a6e8db107c7b9850354_pytorch_lora_weights.safetensors"
        },
        "neiro_bot": {
            "model_endpoint": "fal-ai/flux-lora",
            "lora_path": "https://storage.googleapis.com/fal-flux-lora/51fb01637828495bab1c56a6f0d04662_pytorch_lora_weights.safetensors"
        },
        "TBull_bot": {
            "model_endpoint": "fal-ai/flux-lora",
            "lora_path": "https://storage.googleapis.com/fal-flux-lora/32600fc5a2c1409cbb9293327eab91ed_pytorch_lora_weights.safetensors"
        },
        "TBull_botV2": {
            "model_endpoint": "fal-ai/flux-lora",
            "lora_path": "https://storage.googleapis.com/fal-flux-lora/51fb01637828495bab1c56a6f0d04662_pytorch_lora_weights.safetensors"
        },
        "NeiroV2": {
            "model_endpoint": "fal-ai/flux-lora",
            "lora_path": "https://storage.googleapis.com/fal-flux-lora/51fb01637828495bab1c56a6f0d04662_pytorch_lora_weights.safetensors"
        },
        "cate": {
            "model_endpoint": "fal-ai/flux-lora",
            "lora_path": "https://storage.googleapis.com/fal-flux-lora/d85d61819687421187d5d1c2140f55db_pytorch_lora_weights.safetensors"
        },
        "roost": {
            "model_endpoint": "fal-ai/flux-lora",
            "lora_path": "https://storage.googleapis.com/fal-flux-lora/b569e12a0c6f48bfa6ffb64c8891371c_pytorch_lora_weights.safetensors"
        },
        "mumu": {
            "model_endpoint": "fal-ai/flux-lora",
            "lora_path": "https://storage.googleapis.com/fal-flux-lora/d85d61819687421187d5d1c2140f55db_pytorch_lora_weights.safetensors"
        },
        "tora": {
            "model_endpoint": "fal-ai/flux-lora",
            "lora_path": "https://storage.googleapis.com/fal-flux-lora/883acc1c260549b9a285461b55e7c150_pytorch_lora_weights.safetensors"
        },
        "simons_cat": {
            "model_endpoint": "fal-ai/flux-lora", 
            "lora_path": "https://storage.googleapis.com/fal-flux-lora/d6ffe2c730ac4a8fa5b0d5cad2d71997_pytorch_lora_weights.safetensors"
        },
        "hoops": {
            "model_endpoint": "fal-ai/flux-lora", 
            "lora_path": "https://storage.googleapis.com/fal-flux-lora/4cf85b1ac3674ddfb3a1d1bd579747a0_pytorch_lora_weights.safetensors"
        },
        "brett": {
            "model_endpoint": "fal-ai/flux-lora", 
            "lora_path": "https://storage.googleapis.com/fal-flux-lora/ff25b9bc83c9440b87ae06d256c65904_pytorch_lora_weights.safetensors"
        },
        "klaus": {
            "model_endpoint": "fal-ai/flux-lora", 
            "lora_path": "https://storage.googleapis.com/fal-flux-lora/93bdc35b9e4e408d92d242d09d27331c_pytorch_lora_weights.safetensors"
        },
        "klaus_V2": {
            "model_endpoint": "fal-ai/flux-lora", 
            "lora_path": "https://storage.googleapis.com/fal-flux-lora/93bdc35b9e4e408d92d242d09d27331c_pytorch_lora_weights.safetensors"
        },
        "buttman": {
            "model_endpoint": "fal-ai/flux-lora", 
            "lora_path": "https://storage.googleapis.com/fal-flux-lora/078201ae10f24b88b8792dca0e15d9a5_pytorch_lora_weights.safetensors"
        },
        "brian": {
            "model_endpoint": "fal-ai/flux-lora", 
            "lora_path": "https://storage.googleapis.com/fal-flux-lora/461fa7dad5e44c609ec6ddc97c04a24b_pytorch_lora_weights.safetensors"
        },
        "mad": {
            "model_endpoint": "fal-ai/flux-lora", 
            "lora_path": "https://storage.googleapis.com/fal-flux-lora/7e601db519b14be99d3087d4c004cfd4_pytorch_lora_weights.safetensors"
        },
        "fwog": {
            "model_endpoint": "fal-ai/flux-lora", 
            "lora_path": "https://storage.googleapis.com/fal-flux-lora/eb3a7fb859244df9a7670b0a5823b4b5_pytorch_lora_weights.safetensors"
        },
        "bork": {
            "model_endpoint": "fal-ai/flux-lora", 
            "lora_path": "https://storage.googleapis.com/fal-flux-lora/5ec7b1ef54854457bc746c87ec52a4ca_pytorch_lora_weights.safetensors"
        },
        "stabby_duck": {
            "model_endpoint": "fal-ai/flux-lora", 
            "lora_path": "https://storage.googleapis.com/fal-flux-lora/43fddb1c8d274c00b23715a3537a7dd1_pytorch_lora_weights.safetensors"
        },
        "default": {
            "model_endpoint": "correct-model-endpoint",  # Replace with the default endpoint
            "lora_path": None
        }
    }

    def _generate_prompt(self, user_prompt: str, prompt_template: str) -> str:
        llama_prompt = prompt_template.format(user_prompt=user_prompt)
        return gpt4omini(prompt=llama_prompt, api_key=Config.OPENAI_API_KEY)

    def _request_image_url(self, prompt: str, model_endpoint: str, lora_path: Optional[str] = None) -> str:
        if lora_path:
            return lora(fal_key=Config.FAL_KEY_SECRET, lora_path=lora_path, prompt=prompt, model_endpoint=model_endpoint)
        return flux(fal_key=Config.FAL_KEY_SECRET, prompt=prompt)

    def generate_for_character(self, character_name: str, user_prompt: str, prompt_template: str) -> str:
        config = self.CHARACTER_CONFIG.get(character_name, self.CHARACTER_CONFIG["default"])
        prompt = self._generate_prompt(user_prompt, prompt_template)
        return self._request_image_url(prompt, model_endpoint=config["model_endpoint"], lora_path=config.get("lora_path"))


def meme(character_name: str, user_prompt: str, prompt_template: str) -> str:
    generator = GenerateImage()
    return generator.generate_for_character(character_name, user_prompt, prompt_template)
