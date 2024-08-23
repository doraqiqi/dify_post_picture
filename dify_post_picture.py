from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

# API configuration
API_KEY = "Your API KEY"
UPLOAD_URL = "your server/v1/files/upload"
WORKFLOW_URL = "your server/v1/workflows/run"

def upload_image(image_path, api_key):
    """Uploads an image to the server and returns the file ID"""
    headers = {"Authorization": f"Bearer {api_key}"}
    with open(image_path, 'rb') as image_file:
        files = {
            "file": ("image_name.jpg", image_file, "image/jpeg"),
            "user": (None, "abc-123")
        }
        response = requests.post(UPLOAD_URL, headers=headers, files=files)
    
    if response.status_code == 201:
        try:
            response_data = response.json()
            return response_data.get('id')
        except json.JSONDecodeError:
            print("Response is not in JSON format.")
            return None
    else:
        print(f"Failed to upload image: {response.status_code}")
        return None

def run_workflow(upload_file_id, api_key):
    """Execute workflows and process responses"""
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
    }
    data = {
        "inputs": {},
        "response_mode": "blocking",
        "user": "abc-123",
        "files": [{
            "type": "image",
            "transfer_method": "local_file",
            "upload_file_id": upload_file_id
        }]
    }
    
    response = requests.post(WORKFLOW_URL, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        try:
            response_data = response.json()
            return response_data.get('data', {}).get("outputs")
        except json.JSONDecodeError:
            print("Workflow response is not in JSON format.")
            return None
    else:
        print(f"Failed to run workflow: {response.status_code}")
        return None

@app.route('/process-image', methods=['POST'])
def process_image():
    image_path = request.json.get('image_path')
    
    if not image_path:
        return jsonify({"error": "No image path provided"}), 400
    
    upload_file_id = upload_image(image_path, API_KEY)
    
    if not upload_file_id:
        return jsonify({"error": "Failed to upload image"}), 500
    
    outputs = run_workflow(upload_file_id, API_KEY)
    
    if outputs:
        return jsonify({"outputs": outputs}), 200
    else:
        return jsonify({"error": "Failed to process workflow"}), 500

if __name__ == '__main__':
    app.run(debug=True)
