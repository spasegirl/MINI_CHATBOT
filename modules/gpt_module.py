from flask import Flask, render_template, request, jsonify
from langchain_openai import AzureChatOpenAI
import os
from dotenv import load_dotenv
from langchain_openai import AzureOpenAIEmbeddings

load_dotenv()

api_key = os.getenv("AZURE_OPENAI_API_KEY")
api_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")

llm = AzureChatOpenAI(
    model_name="gpt-35-turbo-0613",
    azure_endpoint=api_endpoint,
    openai_api_key=api_key,
    api_version="2024-05-01-preview",
    request_timeout=60
)

embedding_model = AzureOpenAIEmbeddings(api_key=api_key, 
                                        azure_endpoint=api_endpoint, 
                                        azure_deployment="text-embedding-ada-002", 
                                        api_version="2024-05-01-preview")
