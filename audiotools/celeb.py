import requests
import uuid
import time
import re
import yaml
import os

# Get the path to the voices YAML file
def get_voices_file_path():
    # This will work when running directly from the package or in environments where the package is installed
    return os.path.join(os.path.dirname(__file__), 'voices.yaml')

# Load voices from a YAML file
with open(get_voices_file_path(), 'r') as file:
    fake_you_voice = yaml.safe_load(file)

class FakeYouTTS:
    def __init__(self, username_or_email, password):
        self.cookie = self.authenticate(username_or_email, password)

    def authenticate(self, username_or_email, password):
        login_url = "https://api.fakeyou.com/v1/login"
        login_payload = {
            "username_or_email": username_or_email,
            "password": password
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

        # Extract the session token from the cookie
        session_token = re.search(r"session=([^;]+)", cookie).group(1)
        return session_token

    def make_tts_request(self, text, model_token):
        tts_url = "https://api.fakeyou.com/tts/inference"
        tts_payload = {
            "tts_model_token": model_token,
            "uuid_idempotency_token": str(uuid.uuid4()),
            "inference_text": text
        }
        tts_headers = {
            "Content-Type": "application/json",
            "Cookie": f"session={self.cookie}"
        }

        response = requests.post(tts_url, json=tts_payload, headers=tts_headers)
        response_json = response.json()

        if response_json.get("success"):
            return response_json["inference_job_token"]
        else:
            raise Exception("TTS request failed.")

    def check_tts_status(self, job_token):
        status_url = f"https://api.fakeyou.com/tts/job/{job_token}"
        status_headers = {
            "Accept": "application/json",
            "Cookie": f"session={self.cookie}"
        }

        while True:
            response = requests.get(status_url, headers=status_headers)
            response_json = response.json()

            if response_json["state"]["status"] == "complete_success":
                return response_json["state"]["maybe_public_bucket_wav_audio_path"]
            elif response_json["state"]["status"] == "failed":
                raise Exception("TTS job failed.")

            time.sleep(5)

    def logout(self):
        logout_url = "https://api.fakeyou.com/v1/logout"
        logout_headers = {
            "Content-Type": "application/json",
            "Cookie": f"session={self.cookie}"
        }

        response = requests.post(logout_url, headers=logout_headers)
        response_json = response.json()

        if not response_json.get("success"):
            raise Exception("Logout failed.")

def celeb(username_or_email, password, text, voice_name):
    if voice_name not in fake_you_voice:
        raise ValueError(f"Voice name '{voice_name}' not found in voices.")

    model_token = fake_you_voice[voice_name]
    tts = FakeYouTTS(username_or_email, password)
    job_token = tts.make_tts_request(text, model_token)
    wav_path = tts.check_tts_status(job_token)
    tts.logout()
    
    return wav_path
