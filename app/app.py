from flask import Flask, request, jsonify, render_template_string
from pymongo import MongoClient
import os

app = Flask(__name__)

# MongoDB configuration
mongo_uri = os.getenv('MONGO_URI', 'mongodb://mongo:27017/mydatabase')
try:
    client = MongoClient(mongo_uri)
    db = client.mydatabase
    collection = db.mycollection
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")

@app.route('/')
def index():
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Input Form</title>
            <script>
                function submitData() {
                    var input = document.getElementById('inputField').value;
                    fetch('/store', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ data: input }),
                    })
                    .then(response => response.json())
                    .then(data => {
                        alert('Success: ' + data.status);
                    })
                    .catch((error) => {
                        console.error('Error:', error);
                    });
                }
            </script>
        </head>
        <body>
            <h1>Enter Data</h1>
            <input type="text" id="inputField" placeholder="Enter some data"/>
            <button onclick="submitData()">Submit</button>
        </body>
        </html>
    ''')

@app.route('/store', methods=['POST'])
def store_data():
    data = request.json
    if not data or 'data' not in data:
        return jsonify({"error": "No data provided"}), 400
    try:
        collection.insert_one({"data": data['data']})
        return jsonify({"status": "Data stored successfully"}), 201
    except Exception as e:
        return jsonify({"error": f"Failed to store data: {e}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
