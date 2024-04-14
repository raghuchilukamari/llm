from setuptools import setup

with open('requirements.txt', encoding='utf-8') as f:
    requirements = f.read().splitlines()

setup(
    name='llm-utils',
    version='0.0.1',
    description='LLM Utils',
    long_description='A utility package for LLMs',
    author='Raghu Chilukamari',
    author_email='raghunadh.chilukamari@gmail.com',
    python_requires='>=3.9',
    install_requires=requirements,
    packages=[]
)