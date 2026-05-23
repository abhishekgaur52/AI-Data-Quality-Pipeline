from flask import Flask, request
import subprocess
import os
import sys

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)

@app.route("/")
def home():
    return {"message": "API running"}

@app.route("/run-pipeline")
def run_pipeline():
    result = subprocess.run(
        ["python", "main.py"],
        cwd=BASE_DIR,              # 🔥 THIS is the key fix
        capture_output=True,
        text=True
    )

    return {
        "status": "success" if result.returncode == 0 else "failed",
        "output": result.stdout,
        "error": result.stderr
    }

@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files["file"]
    save_path = os.path.join(BASE_DIR, "data/raw", file.filename)
    file.save(save_path)
    return {"status": "uploaded", "file": file.filename}

if __name__ == "__main__":
    app.run(debug=True)