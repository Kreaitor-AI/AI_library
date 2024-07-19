from setuptools import setup, find_packages

setup(
    name="liveweb",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.1",
        "beautifulsoup4>=4.9.3",
        "langchain>=0.0.1",
        "langchain_openai>=0.0.1",
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

