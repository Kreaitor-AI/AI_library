from imagetools import flux
from memelora import lora
from chat import llama3
from src.config import Config
from typing import Optional, Dict

class GenerateImage:
    CHARACTER_CONFIG: Dict[str, Dict[str, Optional[str]]] = {
        "ginnan": {
            "model_endpoint": "fal-ai/flux-lora",
            "lora_path": "https://storage.googleapis.com/fal-flux-lora/62ac63a1d08f4c0889f993b410ee94f3_pytorch_lora_weights.safetensors"
        },
        "neiro_test_dev": {
            "model_endpoint": "fal-ai/flux-lora",
            "lora_path": "https://storage.googleapis.com/fal-flux-lora/21f72ae8e3e3483a9b5ab601b91d679f_pytorch_lora_weights.safetensors"
        },
        "neiro_bot": {
            "model_endpoint": "fal-ai/flux-lora",
            "lora_path": "https://storage.googleapis.com/fal-flux-lora/4e10d382067d48dc959ad2f02e6cf407_pytorch_lora_weights.safetensors"
        },
        "TBull_bot": {
            "model_endpoint": "fal-ai/flux-lora",
            "lora_path": "https://storage.googleapis.com/fal-flux-lora/2365de7d12234465947939bde3591181_pytorch_lora_weights.safetensors"
        },
        "TBull_botV2": {
            "model_endpoint": "fal-ai/flux-lora",
            "lora_path": "https://storage.googleapis.com/fal-flux-lora/b6bab56a352f46ebba26d85a1e6ed15f_pytorch_lora_weights.safetensors"
        },
        "cate": {
            "model_endpoint": "fal-ai/flux-lora",
            "lora_path": "https://storage.googleapis.com/fal-flux-lora/266d7154a467435bb1841a5d814656e3_pytorch_lora_weights.safetensors"
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
        else:
            return flux(fal_key=Config.FAL_KEY_SECRET, prompt=prompt)

    def generate_for_character(self, character_name: str, user_prompt: str, prompt_template: str) -> str:
        config = self.CHARACTER_CONFIG.get(character_name, self.CHARACTER_CONFIG["default"])
        prompt = self._generate_prompt(user_prompt, prompt_template)
        return self._request_image_url(prompt, model_endpoint=config["model_endpoint"], lora_path=config.get("lora_path"))


def meme(character_name: str, user_prompt: str, prompt_template: str) -> str:
    generator = GenerateImage()
    return generator.generate_for_character(character_name, user_prompt, prompt_template)