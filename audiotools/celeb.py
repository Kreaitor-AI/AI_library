import requests
import uuid
import time
import re

class FakeYouTTS:
    """
    A client class for interacting with a fake TTS API requiring authentication and session handling.
    Parameters:
        - username_or_email (str): The username or email of the user.
        - password (str): The user's password for authentication.
    Processing Logic:
        - Upon initialization, the class attempts to authenticate using the provided credentials to obtain a session cookie.
        - The `authenticate` method centrally handles the authentication process.
        - In `make_tts_request`, we use an idempotency token to ensure the text-to-speech request is processed exactly once.
        - The `check_tts_status` method uses polling to wait for the audio file to become ready or for a failure to occur.
    """
    def __init__(self, username_or_email, password):
        self.cookie = self.authenticate(username_or_email, password)

    def authenticate(self, username_or_email, password):
        """Authenticates a user and retrieves their session token.
        Parameters:
            - username_or_email (str): The username or email of the user.
            - password (str): The password of the user.
        Returns:
            - str: The session token if authentication is successful.
        Processing Logic:
            - The function raises an exception if the "success" key in the response JSON is not True, indicating authentication failed.
            - Another exception is raised if the "set-cookie" header is not present in the response, implying a cookie could not be retrieved.
            - The session token is extracted from the "set-cookie" header using regular expression matching."""
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
        """Makes a POST request to a fake TTS service API to convert text to speech.
        Parameters:
            - text (str): The text to be converted into speech.
            - model_token (str): The token representing the TTS model to be used.
        Returns:
            - str: The inference job token if the request is successful.
        Processing Logic:
            - A unique UUID is generated for each request to ensure idempotency.
            - An exception is raised if the API response indicates a failure."""
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
        """Check the status of a text-to-speech job and retrieve the audio path once completed.
        Parameters:
            - job_token (str): The unique token identifying the specific TTS job.
        Returns:
            - str: The path to the generated WAV audio file if the job is successfully completed.
        Processing Logic:
            - It continuously polls the TTS API until the job is either completed successfully or failed.
            - If the job fails, it raises an exception.
            - Implements a 5-second delay between each poll to avoid overwhelming the API server."""
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
        """Log out a user from the session.
        Parameters:
            - None
        Returns:
            - None
        Processing Logic:
            - Posts a request to a fixed URL to terminate the session.
            - Raises an exception if the logout is not successful."""
        logout_url = "https://api.fakeyou.com/v1/logout"
        logout_headers = {
            "Content-Type": "application/json",
            "Cookie": f"session={self.cookie}"
        }

        response = requests.post(logout_url, headers=logout_headers)
        response_json = response.json()

        if not response_json.get("success"):
            raise Exception("Logout failed.")

def celeb(username_or_email, password, text, model_token):
    tts = FakeYouTTS(username_or_email, password)
    job_token = tts.make_tts_request(text, model_token)
    wav_path = tts.check_tts_status(job_token)
    tts.logout()
    
    return wav_path
