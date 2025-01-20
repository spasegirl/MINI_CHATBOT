from modules.gpt_module import llm
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def rag_pipeline(user_input, retriever=None, image_description=None):
    """
    Handles user input with a preference for context-based responses. 
    Falls back to general GPT response if the query is unrelated to the context.
    
    Args:
        user_input (str): User's question or query.
        retriever (Optional): Context retriever for documents.
        image_description (Optional[str]): Description of an uploaded image.
    
    Returns:
        str: Response from GPT.
    """
    context = ""

    # Step 1: Build context
    if image_description:
        context = f"Image description: {image_description}"
    elif retriever:
        try:
            retrieved_docs = retriever.get_relevant_documents(user_input)
            if retrieved_docs:
                context = "\n".join(doc.page_content for doc in retrieved_docs)
        except Exception as e:
            logging.error(f"Error retrieving documents: {e}")

    # Step 2: Check if context exists and use it
    if context:
        prompt_with_context = f"""
        You are an assistant that answers questions based on a provided context.
        If the question is unrelated to the context, let me know by responding, 
        "This question is unrelated to the context." Then answer the question generally.

        Context: {context}
        Question: {user_input}
        Answer:
        """
        response = llm.invoke([{"role": "user", "content": prompt_with_context}])
        response_text = response.content.strip()

        # If the response indicates irrelevance, fallback to general conversation
        if "This question is unrelated to the context" in response_text:
            context = None  # Mark context as not used
        else:
            return response_text

    # Step 3: General fallback (no context)
    prompt_general = f"""
        You are a helpful conversational assistant with knowledge of various topics. 
        - If the user asks a question unrelated to the provided/uploaded context, you should respond with general knowledge.
        - If the user provides some context or asks a question related to it, try to incorporate the relevant context in your response. 
        - Otherwise, answer as clearly and informatively as possible based on your general knowledge.

        Question: {user_input}
        Answer:
        """

    general_response = llm.invoke([{"role": "user", "content": prompt_general}])
    return general_response.content.strip()
