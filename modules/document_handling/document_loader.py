from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document


from modules.gpt_module import llm, embedding_model

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
    # Load the PDF
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