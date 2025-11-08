from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

# Configure Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'your-api-key-here')
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

chat_history = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')
        
        # Add user message to chat history
        chat_history.append({"role": "user", "content": user_message})
        
        # Get response from Gemini
        chat = model.start_chat(history=chat_history)
        response = chat.send_message(user_message)
        
        # Add AI response to chat history
        chat_history.append({"role": "assistant", "content": response.text})
        
        return jsonify({
            "status": "success",
            "response": response.text
        })
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/clear', methods=['POST'])
def clear_chat():
    chat_history.clear()
    return jsonify({"status": "success", "message": "Chat history cleared"})

if __name__ == '__main__':
    app.run(debug=True)