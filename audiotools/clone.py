import os
from elevenlabs.client import ElevenLabs
from elevenlabs import Voice, VoiceSettings
from langchain import PromptTemplate
from langchain_openai import ChatOpenAI
import pkg_resources

class CloneAudioTools:
    def __init__(self, openai_api_key: str, elevenlabs_api_key: str, prompts_file: str = None):
        """
        Initialize the CloneAudioTools class with API keys and load prompts.

        Args:
            openai_api_key (str): API key for OpenAI.
            elevenlabs_api_key (str): API key for ElevenLabs.
            prompts_file (str, optional): Path to the prompts YAML file. Defaults to 'prompts.yaml' in the package.
        """
        self.llm = ChatOpenAI(api_key=openai_api_key, model="gpt-3.5-turbo")
        self.client = ElevenLabs(api_key=elevenlabs_api_key)
        if prompts_file is None:
            prompts_file = pkg_resources.resource_filename(__name__, 'prompts.yaml')
        with open(prompts_file, 'r') as file:
            self.prompts = yaml.safe_load(file)

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

    def generate_tts(self, text: str, voice: Voice, stability: float = 0.5,
                     similarity_boost: float = 0.5, style: float = 0.5, use_speaker_boost: bool = True) -> bytes:
        """
        Generate text-to-speech audio using ElevenLabs with the cloned voice.

        Args:
            text (str): The text to convert to speech.
            voice (Voice): The cloned voice to use for speech generation.
            stability (float, optional): Stability setting for the voice. Defaults to 0.5.
            similarity_boost (float, optional): Similarity boost setting. Defaults to 0.5.
            style (float, optional): Style setting for the voice. Defaults to 0.5.
            use_speaker_boost (bool, optional): Whether to use speaker boost. Defaults to True.

        Returns:
            bytes: The generated audio in bytes.
        """
        settings = VoiceSettings(
            stability=stability, 
            similarity_boost=similarity_boost, 
            style=style, 
            use_speaker_boost=use_speaker_boost
        )
        audio_generator = self.client.generate(text=text, voice=voice)
        audio = b''.join(audio_generator)
        return audio

    def clone_voice(self, file_path_or_bytes: str, name: str, description: str) -> Voice:
        """
        Clone a user's voice using the provided audio file.

        Args:
            file_path_or_bytes (str): Path to the audio file or bytes of the audio file.
            name (str): The name of the cloned voice.
            description (str): A brief description of the voice.

        Returns:
            Voice: The cloned voice object.
        """
        if os.path.isfile(file_path_or_bytes):
            voice = self.client.clone(name=name, description=description, files=[file_path_or_bytes])
        else:
            voice = self.client.clone(name=name, description=description, files=[file_path_or_bytes])
        return voice

def clone_audio(openai_api_key: str, elevenlabs_api_key: str, text: str, file_path_or_bytes: str, emotion: str = None,
                stability: float = 0.5, similarity_boost: float = 0.5, style: float = 0.5, 
                use_speaker_boost: bool = True, prompts_file: str = None, name: str = '', description: str = '') -> bytes:
    """
    Generate audio from text with optional emotion and specified voice settings. Requires voice cloning.

    Args:
        openai_api_key (str): API key for OpenAI.
        elevenlabs_api_key (str): API key for ElevenLabs.
        text (str): The text to convert to speech.
        file_path_or_bytes (str): Path to the audio file or bytes for cloning the voice (mandatory).
        emotion (str, optional): The emotion to apply to the text. If None, no emotion is applied.
        stability (float, optional): Stability setting for the voice. Defaults to 0.5.
        similarity_boost (float, optional): Similarity boost setting. Defaults to 0.5.
        style (float, optional): Style setting for the voice. Defaults to 0.5.
        use_speaker_boost (bool, optional): Whether to use speaker boost. Defaults to True.
        prompts_file (str, optional): Path to the prompts YAML file. Defaults to None.
        name (str, optional): The name of the cloned voice.
        description (str, optional): Description of the cloned voice.

    Returns:
        bytes: The generated audio in bytes.
    """
    if not file_path_or_bytes:
        raise ValueError("File path or bytes are required for cloning a voice.")
    
    toolkit = CloneAudioTools(openai_api_key, elevenlabs_api_key, prompts_file)
    modified_text = toolkit.generate_prompt(text, emotion)
    
    voice = toolkit.clone_voice(file_path_or_bytes, name, description)
    
    audio = toolkit.generate_tts(modified_text, voice, stability, similarity_boost, style, use_speaker_boost)
    return audio
