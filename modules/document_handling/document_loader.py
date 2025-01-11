from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from modules.gpt_module import llm, embedding_model


def process_pdf_for_retrieval(file_path):
    """
    Processes a PDF file and sets up a retrieval chain for RAG.
    
    Args:
        file_path (str): Path to the PDF file.

    Returns:
        retrieval_chain (Runnable): A chain that retrieves context and generates answers.
    """
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

    doc_search = FAISS.from_documents(doc_objects, embedding_model)

    # retriever
    retriever = doc_search.as_retriever()

    #  prompt definition
    template = """Answer the question based only on the following context:
    {context}

    Question: {question}
    """
    prompt = ChatPromptTemplate.from_template(template)

    # retrieval chain
    retrieval_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return retrieval_chain
