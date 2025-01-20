from modules.gpt_module import llm
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def rag_pipeline(user_input, retriever=None, image_description=None):
    """
    Unified pipeline for both RetrievalQA and direct LLM interaction.
    
    Args:
        user_input (str): The query or input from the user.
        retriever (Retriever, optional): The retriever object for document search. Defaults to None.
        image_description (str, optional): Description of the uploaded image.
    
    Returns:
        str: Response generated by the LLM.
    """
    context = ""

    # Use single context
    if image_description:
        context = f"Image description: {image_description}"
    elif retriever:
        try:
            retrieved_docs = retriever.get_relevant_documents(user_input)
            if retrieved_docs:
                context = "\n".join(doc.page_content for doc in retrieved_docs)
        except Exception as e:
            logger.error(f"Error during document retrieval: {e}")

    # Fallback if no context is available
    if not context:
        context = "No relevant context found."

    # Prepare the prompt for the LLM
    prompt_text = f"""
    You are an assistant that can answer questions based on a document or provide general assistance.
    When the context is provided, answer using the context; otherwise, respond directly to the user's query.

    Context: {context}
    Question: {user_input}
    Answer:
    """

    # Get the response from the LLM
    response = llm.invoke([{"role": "user", "content": prompt_text}])

    return response.content.strip()
