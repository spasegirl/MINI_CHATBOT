from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
import base64
from mimetypes import guess_type
import logging
from playground.image_processor import ImageProcessor
import os
from dotenv import load_dotenv

from modules.gpt_module import embedding_model, vision_model


VISION_API_KEY = os.getenv("VISION_API_KEY")
VISION_API_ENDPOINT = os.getenv("VISION_API_ENDPOINT")

retriever = None
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.ERROR)
retriever = None

class FileProcessor:

    retriever = None

    def process_pdf_for_retrieval(file_path):
        """
        Processes a PDF file and sets up a retrieval chain for RAG.
        
        Args:
            file_path (str): Path to the PDF file.

        Returns:
            retrieval_chain (Runnable): A chain that retrieves context and generates answers.
        """
        global retriever
        # Loading the PDF
        loader = PyPDFLoader(file_path)
        documents = loader.load()

        # Text splitting
        re_char_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000,
            chunk_overlap=100,
            length_function=len,
            is_separator_regex=False,
        )
        chunks = re_char_splitter.split_documents(documents)

        # documents for FAISS
        doc_objects = [Document(page_content=str(chunk)) for chunk in chunks]
        print(f"Retrieved documents: {[doc.page_content for doc in doc_objects]}")

        doc_search = FAISS.from_documents(doc_objects, embedding_model)

        # retriever
        retriever = doc_search.as_retriever()
        print("Retriever created")


        return retriever
    

    def local_image_to_data_url(image_path):

        mime_type, _ = guess_type(image_path)
        if mime_type is None:
            mime_type = 'application/octet-stream'  

        # reading and encoding the image file
        with open(image_path, "rb") as image_file:
            base64_encoded_data = base64.b64encode(image_file.read()).decode('utf-8')

        # data URL
        return f"data:{mime_type};base64,{base64_encoded_data}"
    

    def process_image_description(image_path):

        image_processor = ImageProcessor(api_key=VISION_API_KEY, azure_endpoint= VISION_API_ENDPOINT, api_version="2024-05-01-preview")
        return image_processor.describe_image(image_path)




    

    def process_image(image_path):
        """
        Processes an image and retrieves a description using GPT-4 Vision.
        """
        try:
            # Convert image to data URL
            data_url = FileProcessor.local_image_to_data_url(image_path)

            # Use vision_model to generate a description
            response = vision_model.chat.completions.create(
                model="gpt-4-vision",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Describe the image in detail, or say 'No description for this image'."
                            },
                            {
                                "type": "image_url",
                                "image_url": {"url": data_url},
                            },
                        ],
                    }
                ],
                max_tokens=100,
                temperature=0
            )
            return response.content.strip()
        except Exception as e:
            logger.error(f"Error processing image: {e}")
            raise RuntimeError("Failed to process the image. Check endpoint, deployment, and API key.")
