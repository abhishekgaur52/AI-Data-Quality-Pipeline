from flask import Flask
from main import run_pipeline

app = Flask(__name__)

@app.route("/")
def home():
    return {"message": "API running"}

@app.route("/run-pipeline")
def run():
    result = run_pipeline()
    return result


if __name__ == "__main__":
    app.run(port=5000, debug=True)