from modules.document_handling.file_processer import FileProcessor


def get_file_handler(file_extension):
    if file_extension.lower() == 'pdf':
        return FileProcessor.process_pdf_for_retrieval
    
    elif file_extension.lower() in ['png', 'jpeg' ,'jpg']:
        return FileProcessor.process_image_description
    

    raise ValueError(f"No handler found for {file_extension} files.")
