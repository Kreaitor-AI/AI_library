import os
import fal_client
from .languages import language_codes

class STTTools:
    def __init__(self, api_key):
        """
        Initialize the STTTools class with the API key.
        
        Args:
            api_key (str): The API key for authentication.
        """
        os.environ['FAL_KEY'] = api_key

    def submit_request(self, audio_url, selected_language, task='transcribe', diarize=False, num_speakers=None):
        """
        Submit a request to the FAL API for transcription or translation.

        Args:
            audio_url (str): The URL of the audio file.
            selected_language (str): The selected language for the audio.
            task (str): The task to perform ('transcribe' or 'translate').
            diarize (bool): Whether to diarize the audio.
            num_speakers (int, optional): The number of speakers in the audio.

        Returns:
            dict: The result from the FAL API.
        
        Raises:
            ValueError: If the selected language or task is invalid.
        """
        language_code = language_codes.get(selected_language)
        if not language_code:
            raise ValueError(f"Invalid language selected: {selected_language}.")
        
        if task not in ['transcribe', 'translate']:
            raise ValueError(f"Invalid task: {task}. Choose 'transcribe' or 'translate'.")
        
        arguments = {
            "audio_url": audio_url,
            "task": task,
            "language": language_code,
            "diarize": diarize,
            "num_speakers": num_speakers
        }
        
        handler = fal_client.submit("fal-ai/whisper", arguments=arguments)
        result = handler.get()
        return result

def stt(api_key, audio_url, selected_language, task='transcribe', diarize=False, num_speakers=None):
    """
    Convenience function to submit a request for transcription or translation.

    Args:
        api_key (str): The API key for authentication.
        audio_url (str): The URL of the audio file.
        selected_language (str): The selected language for the audio.
        task (str): The task to perform ('transcribe' or 'translate').
        diarize (bool): Whether to diarize the audio.
        num_speakers (int, optional): The number of speakers in the audio.

    Returns:
        dict: The result from the FAL API.
    """
    toolkit = STTTools(api_key)
    return toolkit.submit_request(audio_url, selected_language, task, diarize, num_speakers)

