import os
import time
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from twilio.rest import Client
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Uploads folder setup
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Twilio Client Setup
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
twilio_number = os.getenv('TWILIO_PHONE_NUMBER')

# Ensure credentials are loaded
if not account_sid or not auth_token:
    print("Warning: Twilio credentials not found in .env file!")

client = Client(account_sid, auth_token)

@app.route('/')
def index():
    return render_template('index.html')

# API: WhatsApp Message Bhejne ke liye
@app.route('/api/send-whatsapp', methods=['POST'])
def send_whatsapp():
    data = request.json
    to_number = data.get('to_number')  # Format: 'whatsapp:+919876543210'
    message_body = data.get('message')

    try:
        message = client.messages.create(
            body=message_body,
            from_=twilio_number,
            to=to_number
        )
        return jsonify({"status": "success", "message_sid": message.sid, "message": "WhatsApp sent successfully!"})
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500

# API: Voice Call Karne ke liye
@app.route('/api/make-call', methods=['POST'])
def make_call():
    data = request.json
    to_number = data.get('to_number')  # Format: '+919876543210'
    
    # Twilio ko ek URL chahiye jo call uthane par kya bole (TwiML). 
    # Testing ke liye hum Twilio ka default demo URL use kar rahe hain.
    twiml_url = "http://demo.twilio.com/docs/voice.xml"

    try:
        call = client.calls.create(
            to=to_number,
            from_=os.getenv('TWILIO_PHONE_NUMBER').replace('whatsapp:', ''), # Call ke liye 'whatsapp:' hata dena
            url=twiml_url
        )
        return jsonify({"status": "success", "call_sid": call.sid, "message": "Call initiated successfully!"})
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
