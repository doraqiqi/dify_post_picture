### Intro

You can use this API to send the picture to the dify.ai server and get feedback.

### Install env

pip install --no-cache-dir flask requests

### Run

python dify_post_picture.py

### Example

curl -X POST http://127.0.0.1:5000/process-image \
-H "Content-Type: application/json" \
-d '{"image_path": "files/test.jpg"}'
