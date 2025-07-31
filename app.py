import os
import logging
from flask import Flask, render_template, request, jsonify
from chatbot import AsuraAI

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "asura-ai-secret-key-2024")

# Initialize chatbot
chatbot = AsuraAI()

@app.route('/')
def index():
    """Render the main chat interface"""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages and return AI responses"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({
                'error': 'Message cannot be empty',
                'response': 'Please provide a message to get a response.'
            }), 400
        
        # Get response from chatbot
        response = chatbot.get_response(user_message)
        
        return jsonify({
            'response': response,
            'status': 'success'
        })
        
    except Exception as e:
        logging.error(f"Error processing chat request: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'response': 'I apologize, but I encountered an error processing your request. Please try again.'
        }), 500

@app.route('/api/topics', methods=['GET'])
def get_topics():
    """Get available knowledge topics"""
    topics = chatbot.get_available_topics()
    return jsonify({'topics': topics})

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'Asura-AI'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
