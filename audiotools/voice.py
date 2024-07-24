import requests
import uuid
import time
import re
import yaml
from langchain import PromptTemplate
from langchain_openai import ChatOpenAI
from elevenlabs.client import ElevenLabs
from elevenlabs import Voice, VoiceSettings
import pkg_resources

class Celeb:
    def __init__(self, username_or_email, password, voice_dict_file='voices.yaml', openai_api_key=None, elevenlabs_api_key=None, prompts_file=None):
        self.username_or_email = username_or_email
        self.password = password
        self.voice_dict = self.load_voice_dict(voice_dict_file)
        
        if openai_api_key and elevenlabs_api_key:
            self.audio_tools = AudioTools(openai_api_key, elevenlabs_api_key, prompts_file)

    def load_voice_dict(self, file_path):
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)
    
    def authenticate(self):
        login_url = "https://api.fakeyou.com/v1/login"
        login_payload = {
            "username_or_email": self.username_or_email,
            "password": self.password
        }
        login_headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(login_url, json=login_payload, headers=login_headers)
        response_json = response.json()

        if not response_json.get("success"):
            raise Exception("Authentication failed.")

        cookie = response.headers.get("set-cookie")
        if not cookie:
            raise Exception("Failed to retrieve cookie.")

        session_token = re.search(r"session=([^;]+)", cookie).group(1)
        return session_token

    def make_tts_request(self, cookie, text, model_token):
        tts_url = "https://api.fakeyou.com/tts/inference"
        tts_payload = {
            "tts_model_token": model_token,
            "uuid_idempotency_token": str(uuid.uuid4()),
            "inference_text": text
        }
        tts_headers = {
            "Content-Type": "application/json",
            "Cookie": f"session={cookie}"
        }

        response = requests.post(tts_url, json=tts_payload, headers=tts_headers)
        response_json = response.json()

        if response_json.get("success"):
            return response_json["inference_job_token"]
        else:
            raise Exception("TTS request failed.")

    def check_tts_status(self, cookie, job_token):
        status_url = f"https://api.fakeyou.com/tts/job/{job_token}"
        status_headers = {
            "Accept": "application/json",
            "Cookie": f"session={cookie}"
        }

        while True:
            response = requests.get(status_url, headers=status_headers)
            response_json = response.json()

            if response_json["state"]["status"] == "complete_success":
                return response_json["state"]["maybe_public_bucket_wav_audio_path"]
            elif response_json["state"]["status"] == "failed":
                raise Exception("TTS job failed.")

            time.sleep(5)

    def generate_audio(self, text, model_name, emotion=None):
        if hasattr(self, 'audio_tools'):
            # Using AudioTools if available
            if emotion:
                modified_text = self.audio_tools.generate_prompt(text, emotion)
            else:
                modified_text = text
            voice_name = self.voice_dict.get(model_name, 'Rachel')  # Default to 'Rachel' if not found
            audio = self.audio_tools.generate_tts(modified_text, voice_name)
            return audio
        else:
            # Fallback to the old method if AudioTools is not available
            cookie = self.authenticate()
            model_token = self.voice_dict.get(model_name, None)
            if model_token is None:
                raise ValueError(f"Model {model_name} not found in voice dictionary.")
            
            job_token = self.make_tts_request(cookie, text, model_token)
            wav_path = self.check_tts_status(cookie, job_token)
            return wav_path  # Here you would normally download the WAV file or process it further.

    def logout(self, cookie):
        logout_url = "https://api.fakeyou.com/v1/logout"
        logout_headers = {
            "Content-Type": "application/json",
            "Cookie": f"session={cookie}"
        }

        response = requests.post(logout_url, headers=logout_headers)
        response_json = response.json()

        if not response_json.get("success"):
            raise Exception("Logout failed.")

