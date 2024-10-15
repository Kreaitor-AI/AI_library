from imagetools import flux
from memelora import lora
from chat import llama3
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
            "lora_path": "https://storage.googleapis.com/fal-flux-lora/62ac63a1d08f4c0889f993b410ee94f3_pytorch_lora_weights.safetensors"
        },
        "neiro_test_dev": {
            "model_endpoint": "fal-ai/flux-lora",
            "lora_path": "https://storage.googleapis.com/fal-flux-lora/b853dee01f2749a6a81e0fbf5cdd41fd_pytorch_lora_weights.safetensors"
        },
        "neiro_bot": {
            "model_endpoint": "fal-ai/flux-lora",
            "lora_path": "https://storage.googleapis.com/fal-flux-lora/4e10d382067d48dc959ad2f02e6cf407_pytorch_lora_weights.safetensors"
        },
        "TBull_bot": {
            "model_endpoint": "fal-ai/flux-lora",
            "lora_path": "https://storage.googleapis.com/fal-flux-lora/32600fc5a2c1409cbb9293327eab91ed_pytorch_lora_weights.safetensors"
        },
        "TBull_botV2": {
            "model_endpoint": "fal-ai/flux-lora",
            "lora_path": "https://storage.googleapis.com/fal-flux-lora/b6bab56a352f46ebba26d85a1e6ed15f_pytorch_lora_weights.safetensors"
        },
        "cate": {
            "model_endpoint": "fal-ai/flux-lora",
            "lora_path": "https://storage.googleapis.com/fal-flux-lora/266d7154a467435bb1841a5d814656e3_pytorch_lora_weights.safetensors"
        },
        "roost": {
            "model_endpoint": "fal-ai/flux-lora",
            "lora_path": "https://storage.googleapis.com/fal-flux-lora/b569e12a0c6f48bfa6ffb64c8891371c_pytorch_lora_weights.safetensors"
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
            "lora_path": "https://storage.googleapis.com/fal-flux-lora/8ffdc397b30c4da8ba18752de44fbc62_pytorch_lora_weights.safetensors"
        },
        "buttman": {
            "model_endpoint": "fal-ai/flux-lora", 
            "lora_path": "https://storage.googleapis.com/fal-flux-lora/078201ae10f24b88b8792dca0e15d9a5_pytorch_lora_weights.safetensors"
        },
        "default": {
            "model_endpoint": "correct-model-endpoint",  # Replace with the default endpoint
            "lora_path": None
        }
    }

    def _generate_prompt(self, user_prompt: str, prompt_template: str) -> str:
        llama_prompt = prompt_template.format(user_prompt=user_prompt)
        return llama3(prompt=llama_prompt, api_key=Config.TOGETHER_API_KEY)

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
