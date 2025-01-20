from flask import Flask, request, render_template, jsonify
from modules.document_handling import get_file_handler, save_file
from modules.query_handling.query_handler import rag_pipeline
from modules.document_handling.file_processer import FileProcessor

import logging
from modules.gpt_module import llm

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/uploads/"


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    global retriever, image_description
    if request.method == "POST":
        # HandlING PDF upload
        if "file" not in request.files:
            return "No file part", 400
        file = request.files["file"]
        
        # SavING file
        filepath = save_file(file)
        if not filepath:
            return "Invalid file type. Please upload a file.", 400
        
        #  file handler based on the file extension
        file_extension = filepath.rsplit('.', 1)[1].lower()
        try:
            # Resetting context
            retriever = None
            image_description = None

            if file_extension in ["pdf"]:
                retriever = get_file_handler(file_extension)(filepath)
                return jsonify({"message": "PDF uploaded and processed successfully!"}), 200
            elif file_extension in ["jpg", "jpeg", "png"]:
                image_description = get_file_handler(file_extension)(filepath)
                return jsonify({"message": "Image uploaded and processed successfully!", "description": image_description}), 200
            else:
                return "Unsupported file type. Please upload a PDF or image.", 400
        except Exception as e:
            logger.error(f"Error processing file: {e}")
            return jsonify({"error": f"Error processing file: {e}"}), 500

    return render_template("index.html")




@app.route("/query", methods=["POST"])
def query():
    global retriever, image_description
    user_query = request.json.get("query")

    if not user_query:
        return jsonify({"error": "Query cannot be empty."}), 400

    try:
        # RAG pipeline for all queries, retriever may be None
        response = rag_pipeline(user_query, retriever=retriever, image_description=image_description)
        return jsonify({"response": response})
    except Exception as e:
        logger.error(f"Error in query execution: {e}")
        return jsonify({"error": "An error occurred while processing your query."}), 500

 # chat route for general queries without PDF
@app.route("/chat", methods=["POST"])
def chat():
    user_query = request.json.get("query")

    if not user_query:
        return jsonify({"error": "Query cannot be empty."}), 400

    try:
        response = rag_pipeline(user_query, retriever=None, image_description=None)
        return jsonify({"response": response})
    except Exception as e:
        logger.error(f"Error in chat execution: {e}")
        return jsonify({"error": "An error occurred while processing your query."}), 500


if __name__ == "__main__":
    app.run(debug=True)
