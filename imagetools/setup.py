from setuptools import setup, find_packages

setup(
    name="imagetools",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "openai",
    ],
    author="Mohammad Agwan",
    author_email="mohammad.agwan@somaiya.edu",
    description="A toolkit for generating images using DALL-E.",
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
