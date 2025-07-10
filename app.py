from flask import Flask, render_template, request, redirect, url_for
from azure.storage.blob import BlobServiceClient
import os

app = Flask(__name__)

# Set these as environment variables or directly for demo
AZURE_CONN_STR = os.environ.get('AZURE_CONN_STR') or '<your_connection_string>'
CONTAINER_NAME = 'uploads'

blob_service = BlobServiceClient.from_connection_string(AZURE_CONN_STR)
container_client = blob_service.get_container_client(CONTAINER_NAME)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            blob_client = container_client.get_blob_client(file.filename)
            blob_client.upload_blob(file, overwrite=True)
    # List blobs
    blobs = container_client.list_blobs()
    return render_template('index.html', blobs=blobs)

@app.route('/download/<filename>')
def download(filename):
    blob_client = container_client.get_blob_client(filename)
    downloader = blob_client.download_blob()
    return downloader.readall()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
