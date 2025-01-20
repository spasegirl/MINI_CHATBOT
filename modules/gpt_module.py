from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings, AzureOpenAI
from config import AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, VISION_API_KEY, VISION_API_ENDPOINT

llm = AzureChatOpenAI(
    model_name="gpt-35-turbo-0613",
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    openai_api_key=AZURE_OPENAI_API_KEY,
    api_version="2024-05-01-preview"
)

embedding_model = AzureOpenAIEmbeddings(
    api_key=AZURE_OPENAI_API_KEY,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    azure_deployment="text-embedding-ada-002",
    api_version="2024-05-01-preview"
)

vision_model = AzureOpenAI(
    api_key=VISION_API_KEY,
    azure_endpoint=VISION_API_ENDPOINT,
    api_version="2024-05-01-preview"
)