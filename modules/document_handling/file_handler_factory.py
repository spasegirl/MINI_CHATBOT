from .file_processer import process_pdf_for_retrieval

def get_file_handler(file_extension):
    if file_extension.lower() == 'pdf':
        return process_pdf_for_retrieval

    raise ValueError(f"No handler found for {file_extension} files.")
