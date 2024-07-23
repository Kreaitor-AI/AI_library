import requests
from langchain import PromptTemplate
from langchain_openai import ChatOpenAI
from elevenlabs import ElevenLabs, Voice, VoiceSettings
import yaml
import pkg_resources

class AudioTools:
    def __init__(self, openai_api_key, elevenlabs_api_key, prompts_file=None):
        self.llm = ChatOpenAI(openai_api_key=openai_api_key, model="gpt-4o-mini")
        self.client = ElevenLabs(api_key=elevenlabs_api_key)
        if prompts_file is None:
            prompts_file = pkg_resources.resource_filename(__name__, 'prompts.yaml')
        with open(prompts_file, 'r') as file:
            self.prompts = yaml.safe_load(file)
        self.voice_dict = self.prompts['Voice']

    def generate_prompt(self, text, emotion):
        template = self.prompts['modify_text_with_emotion']
        prompt = PromptTemplate(template=template, input_variables=["text", "emotion"])
        result = prompt | self.llm
        modified_text = result.invoke({"text": text, "emotion": emotion}).content.strip()
        return modified_text

    def generate_tts(self, text, voice_name='Rachel', stability=0.5, similarity_boost=0.5, style=0.5, use_speaker_boost=True):
        voice_id = self.voice_dict.get(voice_name, '21m00Tcm4TlvDq8ikWAM')
        settings = VoiceSettings(stability=stability, similarity_boost=similarity_boost, style=style, use_speaker_boost=use_speaker_boost)
        voice = Voice(voice_id=voice_id, settings=settings)
        audio_generator = self.client.generate(text=text, voice=voice)
        audio = b''.join(audio_generator)
        return audio

def generate_audio(openai_api_key, elevenlabs_api_key, text, emotion, voice_name='Rachel', stability=0.5, similarity_boost=0.5, style=0.5, use_speaker_boost=True, prompts_file=None):
    toolkit = AudioTools(openai_api_key, elevenlabs_api_key, prompts_file)
    modified_text = toolkit.generate_prompt(text, emotion)
    audio = toolkit.generate_tts(modified_text, voice_name, stability, similarity_boost, style, use_speaker_boost)
    return audio
