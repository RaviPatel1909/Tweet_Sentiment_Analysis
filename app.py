from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib

app = Flask(__name__)
CORS(app)

# Load model
try:
    model = joblib.load(r"C:\Web\Sentiment_Analysis\my-app\twitter_sentiment_model.pkl")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

@app.route("/")
def index():
    return jsonify({
        "status": "running",
        "message": "Sentiment Analysis API",
        "version": "1.0"
    })

@app.route("/predict", methods=["POST"])
def predict():
    if not model:
        return jsonify({"error": "Model not loaded"}), 500

    data = request.get_json()
    text = data.get("text", "").strip()

    if not text:
        return jsonify({"error": "No text provided"}), 400

    try:
        prediction = model.predict([text])[0]

        return jsonify({
            "text": text,
            "prediction": prediction
        })
    except Exception as e:
        import traceback
        traceback.print_exc()  # <-- THIS MUST BE HERE

        return jsonify({
            "error": "Prediction failed",
            "message": str(e)
        }), 500



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
