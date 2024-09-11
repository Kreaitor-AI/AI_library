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

class AudioTools:
    def __init__(self, openai_api_key: str, elevenlabs_api_key: str, prompts_file: str = None):
        """
        Initialize the AudioTools class with API keys and load prompts.

        Args:
            openai_api_key (str): API key for OpenAI.
            elevenlabs_api_key (str): API key for ElevenLabs.
            prompts_file (str, optional): Path to the prompts YAML file. Defaults to 'prompts.yaml' in the package.
        """
        self.llm = ChatOpenAI(openai_api_key=openai_api_key, model="gpt-4o-mini")
        self.client = ElevenLabs(api_key=elevenlabs_api_key)
        if prompts_file is None:
            prompts_file = pkg_resources.resource_filename(__name__, 'prompts.yaml')
        with open(prompts_file, 'r') as file:
            self.prompts = yaml.safe_load(file)
        self.voice_dict = self.prompts['Voice']

    def generate_prompt(self, text: str, emotion: str = None) -> str:
        """
        Generate a modified text prompt based on emotion, if provided.

        Args:
            text (str): The input text.
            emotion (str, optional): The emotion to apply to the text. If None, return the text unchanged.

        Returns:
            str: The modified text with the applied emotion, or original text if no emotion is provided.
        """
        if emotion:
            template = self.prompts['modify_text_with_emotion']
            prompt = PromptTemplate(template=template, input_variables=["text", "emotion"])
            result = prompt | self.llm
            return result.invoke({"text": text, "emotion": emotion}).content.strip()
        return text

    def generate_tts(self, text: str, voice_name: str = 'Rachel', stability: float = 0.5,
                     similarity_boost: float = 0.5, style: float = 0.5, use_speaker_boost: bool = True) -> bytes:
        """
        Generate text-to-speech audio using ElevenLabs.

        Args:
            text (str): The text to convert to speech.
            voice_name (str, optional): The name of the voice to use. Defaults to 'Rachel'.
            stability (float, optional): Stability setting for the voice. Defaults to 0.5.
            similarity_boost (float, optional): Similarity boost setting. Defaults to 0.5.
            style (float, optional): Style setting for the voice. Defaults to 0.5.
            use_speaker_boost (bool, optional): Whether to use speaker boost. Defaults to True.

        Returns:
            bytes: The generated audio in bytes.
        """
        voice_id = self.voice_dict.get(voice_name, '21m00Tcm4TlvDq8ikWAM')
        settings = VoiceSettings(
            stability=stability, 
            similarity_boost=similarity_boost, 
            style=style, 
            use_speaker_boost=use_speaker_boost
        )
        voice = Voice(voice_id=voice_id, settings=settings)
        audio_generator = self.client.generate(text=text, voice=voice)
        audio = b''.join(audio_generator)
        return audio

def generate_audio(openai_api_key: str, elevenlabs_api_key: str, text: str, emotion: str = None, 
                   voice_name: str = 'Rachel', stability: float = 0.5, 
                   similarity_boost: float = 0.5, style: float = 0.5, 
                   use_speaker_boost: bool = True, prompts_file: str = None) -> bytes:
    """
    Generate audio from text with optional emotion and specified voice settings.

    Args:
        openai_api_key (str): API key for OpenAI.
        elevenlabs_api_key (str): API key for ElevenLabs.
        text (str): The text to convert to speech.
        emotion (str, optional): The emotion to apply to the text. If None, no emotion is applied.
        voice_name (str, optional): The name of the voice to use. Defaults to 'Rachel'.
        stability (float, optional): Stability setting for the voice. Defaults to 0.5.
        similarity_boost (float, optional): Similarity boost setting. Defaults to 0.5.
        style (float, optional): Style setting for the voice. Defaults to 0.5.
        use_speaker_boost (bool, optional): Whether to use speaker boost. Defaults to True.
        prompts_file (str, optional): Path to the prompts YAML file. Defaults to None.

    Returns:
        bytes: The generated audio in bytes.
    """
    toolkit = AudioTools(openai_api_key, elevenlabs_api_key, prompts_file)
    modified_text = toolkit.generate_prompt(text, emotion)
    audio = toolkit.generate_tts(modified_text, voice_name, stability, similarity_boost, style, use_speaker_boost)
    return audio
