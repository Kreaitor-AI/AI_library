from setuptools import setup, find_packages

setup(
    name="liveweb",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "beautifulsoup4",
        "langchain",
        "langchain_openai",
        "pyyaml",
    ],
    author="Mohammad Agwan",
    author_email="mohammad.agwan@somaiya.edu",
    description="A toolkit for refining search queries, performing Google searches, fetching and processing web content.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/marchmello1/liveweb",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
