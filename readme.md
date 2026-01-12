### Intro

You can use this API to send the picture to your dify.ai server and get feedback.

### Install env

pip install --no-cache-dir flask requests

### API configuration
API_KEY = "Your API KEY"  
UPLOAD_URL = "your server/v1/files/upload"  
WORKFLOW_URL = "your server/v1/workflows/run"  

### Run

python dify_post_picture.py

### Example

curl -X POST http://127.0.0.1:5000/process-image \
-H "Content-Type: application/json" \
-d '{"image_path": "files/test.jpg"}'
