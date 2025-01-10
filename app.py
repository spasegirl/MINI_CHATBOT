from flask import Flask, render_template, request, jsonify
from modules.gpt_module import chat_with_gpt


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input']
    bot_response = chat_with_gpt(user_input)
    return jsonify({'response': bot_response})

if __name__ == "__main__":
    app.run(debug=True)
