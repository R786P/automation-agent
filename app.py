import os
import time
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Uploads folder setup
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# In-memory database (Demo ke liye. Production mein SQLite/PostgreSQL use hoga)
content_queue = []
client_tasks = []

@app.route('/')
def index():
    return render_template('index.html')

# API: CSV Upload handle karne ke liye
@app.route('/api/upload-csv', methods=['POST'])
def upload_csv():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file and file.filename.endswith('.csv'):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return jsonify({"status": "success", "message": f"File {filename} uploaded successfully!"})
    
    return jsonify({"error": "Invalid file type"}), 400

# API: Content Publish karne ka simulation
@app.route('/api/publish', methods=['POST'])
def publish_content():
    data = request.json
    # Yahan baad mein YouTube/LinkedIn API ka code aayega
    time.sleep(2) # 2 second ka delay dikhane ke liye
    return jsonify({"status": "success", "message": f"Successfully published to {data.get('platform')}"})

# API: Client Message send karne ka simulation
@app.route('/api/send-message', methods=['POST'])
def send_message():
    data = request.json
    # Yahan baad mein Gmail/Twilio API ka code aayega
    time.sleep(1.5) # 1.5 second ka delay
    return jsonify({"status": "success", "message": f"Message sent to {data.get('contact')}"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
