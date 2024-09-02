import os
from fal_client import submit
from .languages import language_codes

class STTTools:
    def __init__(self, api_key: str):
        """
        Initialize the STTTools class with the API key.
        
        Args:
            api_key (str): The API key for authentication.
        """
        os.environ['FAL_KEY'] = api_key

    def submit_request(self, audio_url: str, selected_language: str, task: str = 'transcribe') -> dict:
        """
        Submit a request to the FAL API for transcription or translation.

        Args:
            audio_url (str): The URL of the audio file.
            selected_language (str): The selected language for the audio.
            task (str): The task to perform ('transcribe' or 'translate').

        Returns:
            dict: The result from the FAL API.
        
        Raises:
            ValueError: If the selected language or task is invalid.
        """
        language_code = language_codes.get(selected_language)
        if not language_code:
            raise ValueError(f"Invalid language selected: {selected_language}")

        if task not in {'transcribe', 'translate'}:
            raise ValueError(f"Invalid task selected: {task}")

        arguments = {
            "audio_url": audio_url,
            "task": task,
            "language": language_code,
        }
        
        handler = submit("fal-ai/wizper", arguments=arguments)
        return handler.get()

def stt(api_key: str, audio_url: str, selected_language: str, task: str = 'transcribe') -> dict:
    """
    Convenience function to submit a request for transcription or translation.

    Args:
        api_key (str): The API key for authentication.
        audio_url (str): The URL of the audio file.
        selected_language (str): The selected language for the audio.
        task (str): The task to perform ('transcribe' or 'translate').

    Returns:
        dict: The result from the FAL API.
    """
    toolkit = STTTools(api_key)
    return toolkit.submit_request(audio_url, selected_language, task)
