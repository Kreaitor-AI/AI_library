from setuptools import setup, find_packages

setup(
    name="AI_library",
    version="0.1.3",
    packages=find_packages(),
    install_requires=[
        "requests",
        "beautifulsoup4",
        "langchain",
        "langchain_openai",
        "elevenlabs",
        "openai",
        "pyyaml",
        "together",
        "pydub",
        "langchain_together",
        "aiohttp",
        "asyncio",
        "nest_asyncio",
        "fal-client",
        "boto3",

    ],
    package_data={
        'liveweb': ['prompts.yaml'],
        'audiotools': ['prompts.yaml'],
    },
    author="Mohammad Agwan",
    author_email="mohammad.agwan@somaiya.edu",
    description="A toolkit for refining search queries, performing Google searches, fetching and processing web content, generating images using DALL-E, and generating TTS audio with emotion.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/marchmello1/AI_library",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
