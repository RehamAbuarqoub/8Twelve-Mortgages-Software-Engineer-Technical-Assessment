from flask import Flask, jsonify
from app.routes.leads import leads_bp

app = Flask(__name__)
app.register_blueprint(leads_bp)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Lead Assessment API is running"}), 200

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(debug=True)