from setuptools import setup, find_packages

setup(
    name="agilestories",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "python-multipart",
        "pydantic",
        "boto3"
    ],
) 