from setuptools import setup, find_packages

setup(
    name="aipodcast",
    version="1.0.0",
    description="AI-powered podcast generator using Ollama models",
    author="Avinash",
    packages=find_packages(),
    install_requires=[
        "pyyaml",
        "requests"
    ],
    entry_points={
        "console_scripts": [
            "aipodcast=main:main",
        ],
    },
    python_requires='>=3.8',
)
