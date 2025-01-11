from flask import Flask, request, render_template, jsonify
from modules.document_handling.document_upload import save_pdf
from modules.document_handling.document_loader import process_pdf_for_retrieval
from modules.document_handling.query_handler import execute_query, chat_with_gpt
import logging

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/uploads/"

# Global variable to store the retrieval chain
retrieval_chain = None

# Setting up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
@app.route("/", methods=["GET", "POST"])
def index():
    global retrieval_chain
    if request.method == "POST":
        # Handle PDF upload
        if "file" not in request.files:
            return "No file part", 400
        file = request.files["file"]
        filepath = save_pdf(file)
        if not filepath:
            return "Invalid file type. Please upload a PDF.", 400

        # Process PDF
        retrieval_chain = process_pdf_for_retrieval(filepath)
        return "PDF uploaded and processed successfully!", 200

    return render_template("index.html")


@app.route("/query", methods=["POST"])
def query():
    global retrieval_chain
    user_query = request.json.get("query")

    # Case 1: If the PDF is not yet processed
    if retrieval_chain is None:
        # For simple chat interaction
        response = chat_with_gpt(user_query)  # Use the simple chat function
        return jsonify({"response": response})

    # Case 2: If the PDF is processed
    if not user_query:
        return "Query cannot be empty.", 400

    try:
        # Handle queries related to the PDF content
        response = execute_query(retrieval_chain, user_query)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/chat", methods=["POST"])  # New chat route
def chat():
    user_query = request.json.get("query")

    # Handle simple chat interaction
    if not user_query:
        return "Query cannot be empty.", 400

    try:
        # For simple chat queries (no PDF processing involved)
        response = chat_with_gpt(user_query)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
