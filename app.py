from flask import Flask, render_template, request, jsonify
from langchain_openai import AzureChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("AZURE_OPENAI_API_KEY")
api_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")

llm = AzureChatOpenAI(
    model_name="gpt-35-turbo-0613",
    azure_endpoint=api_endpoint,
    openai_api_key=api_key,
    api_version="2024-05-01-preview",
    request_timeout=60
)

app = Flask(__name__)

def chat_with_gpt3(prompt):
    response = llm.invoke([{"role": "user", "content": prompt}])
    return response.content.strip()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input']
    bot_response = chat_with_gpt3(user_input)
    return jsonify({'response': bot_response})

if __name__ == "__main__":
    app.run(debug=True)
