from setuptools import setup, find_packages

setup(
    name="agilestories",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'boto3',
        'python-dotenv',
        'openai'
    ]
) 