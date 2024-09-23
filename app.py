from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from services.groq import send_message_to_groq
from models import db, User, Message

# Load environment variables from the .env file
load_dotenv()

app = Flask(__name__)

# Enable CORS for the entire app
CORS(app, supports_credentials=True, origins=['http://localhost:3000'])

# Configure the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db.init_app(app)

# Create the database tables
with app.app_context():
    db.create_all()

@app.route('/init', methods=['POST'])
def init_user():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')

    if not username or not email:
        return jsonify({'error': 'Username and email are required'}), 400

    # Check if the user already exists
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'error': 'User already exists'}), 400

    # Create a new user
    new_user = User(username=username, email=email)
    db.session.add(new_user)
    db.session.commit()

    # Initialize the conversation with a welcome message
    welcome_message = Message(content="Welcome to the chat!", sender='ai', user_id=new_user.id)
    db.session.add(welcome_message)
    db.session.commit()

    return jsonify({'message': 'User created and conversation initialized', 'user_id': new_user.id}), 201

@app.route('/message', methods=['POST'])
def send_message():
    data = request.get_json()
    user_message = data.get('message')
    user_id = data.get('user_id')

    if not user_message or not user_id:
        return jsonify({'error': 'No message or user_id provided'}), 400

    # Save the user message to the database
    user_message_record = Message(content=user_message, sender='user', user_id=user_id)
    db.session.add(user_message_record)
    db.session.commit()

    # Call the function to send the message to Groq
    response_text = send_message_to_groq(user_message)

    # Save the AI response to the database
    ai_message_record = Message(content=response_text, sender='ai', user_id=user_id)
    db.session.add(ai_message_record)
    db.session.commit()

    return jsonify({'response': response_text})

if __name__ == '__main__':
    app.run(debug=True)
