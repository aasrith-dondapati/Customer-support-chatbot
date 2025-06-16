from flask import Flask, request, render_template, jsonify
import requests
from datetime import datetime
import os
# from flask_sqlalchemy import SQLAlchemy # For database setup (uncomment for full use)

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@host/dbname'
# db = SQLAlchemy(app)

# # Define a simple model for conversation history (uncomment for full use)
# class Conversation(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.String(255), nullable=False)
#     sender = db.Column(db.String(50), nullable=False) # 'user' or 'bot'
#     message = db.Column(db.Text, nullable=False)
#     timestamp = db.Column(db.DateTime, default=datetime.utcnow)

#     def __repr__(self):
#         return f"<Conversation {self.id} from {self.user_id}>"

RASA_API_URL = "http://localhost:5005/webhooks/rest/webhook" # Rasa server URL

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    user_id = request.json.get('sender', 'default_user') # Or generate a unique ID

    if not user_message:
        return jsonify({"response": "No message received."}), 400

    # Log user message to DB (uncomment for full use)
    # new_entry = Conversation(user_id=user_id, sender='user', message=user_message)
    # db.session.add(new_entry)
    # db.session.commit()

    try:
        # Send message to Rasa
        payload = {"sender": user_id, "message": user_message}
        rasa_response = requests.post(RASA_API_URL, json=payload)
        rasa_response.raise_for_status() # Raise an exception for bad status codes
        bot_responses = rasa_response.json()

        responses_text = []
        for response in bot_responses:
            text_response = response.get('text')
            if text_response:
                responses_text.append(text_response)
                # Log bot response to DB (uncomment for full use)
                # new_entry = Conversation(user_id=user_id, sender='bot', message=text_response)
                # db.session.add(new_entry)
                # db.session.commit()

        return jsonify({"response": responses_text})

    except requests.exceptions.RequestException as e:
        print(f"Error communicating with Rasa server: {e}")
        return jsonify({"response": ["Sorry, the chatbot is currently unavailable. Please try again later."]})
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return jsonify({"response": ["An unexpected error occurred. Please try again later."]})

if __name__ == '__main__':
    # with app.app_context(): # Uncomment for database migration
    #     db.create_all()     # Create tables if they don't exist
    app.run(debug=True, port=5000)