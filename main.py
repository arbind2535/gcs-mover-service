from flask import Flask, request, jsonify
from google.cloud import storage

app = Flask(__name__)
storage_client = storage.Client()

@app.route("/", methods=["POST"])
def move_file():
    data = request.get_json()
    source_bucket = data.get("source_bucket")
    destination_bucket = data.get("destination_bucket")
    filename = data.get("filename")

    if not source_bucket or not destination_bucket or not filename:
        return jsonify({"error": "Missing parameters"}), 400

    try:
        source_blob = storage_client.bucket(source_bucket).blob(filename)
        destination_blob = storage_client.bucket(destination_bucket).blob(filename)

        destination_blob.rewrite(source_blob)
        source_blob.delete()

        return jsonify({"status": "success", "file": filename}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
