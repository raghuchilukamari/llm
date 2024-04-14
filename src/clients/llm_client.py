import os, cohere
from dotenv import load_dotenv
from langchain_community.llms import HuggingFaceEndpoint

load_dotenv()


def get_cohere_client():
    co = cohere.Client(os.getenv('COHERE_API_KEY'))
    return co


def get_huggingface_enpoint(model_id):
    return HuggingFaceEndpoint(
    repo_id=model_id,
    temperature=1,
    max_new_tokens=100 )


