from flask import Flask, request, jsonify
from services.groq import send_message_to_groq
from flask_cors import CORS, cross_origin

app = Flask(__name__)

CORS(app, support_credentials=True,resources={r'/*' : {'origins': ['http://localhost:5000']}})
app = Flask(__name__)


@app.route('/message', methods=['POST'])
# @cross_origin(supports_credentials=True)
def send_message():
    data = request.get_json()
    user_message = data.get('message')

    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    # Call the function to send the message to Groq
    response_text = send_message_to_groq(user_message)

    return jsonify({'response': response_text})



if __name__ == '__main__':
    app.run(debug=True)





