import os
from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd
import logging
from pycaret.regression import load_model
# Configure logging
logging.basicConfig(filename="app_errors.log", level=logging.ERROR,
                    format="%(asctime)s %(levelname)s: %(message)s")

# Define absolute model path
model_filename = "final_model_pipeline"

# Load model with error handling
model = load_model(model_filename)
# if os.path.exists(model_filename):
#     try:
#         with open(model_filename, "rb") as file:
#             model = pickle.load(model)
#         logging.info(f"Model '{model_filename}' loaded successfully.")
#     except Exception as e:
#         logging.error(f"Error loading model: {e}")
# else:
#     logging.error(f"Model file '{model_filename}' not found at: {model_path}")

# Initialize Flask app
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        if model is None:
            raise FileNotFoundError(f"Model '{model_filename}' not found. Please check the file path.")

        # Extract input data
        data = {
            "Suburb": [request.json["Suburb"]],
            "Rooms": [float(request.json["Rooms"])],
            "Type": [request.json["Type"]],
            "Distance": [float(request.json["Distance"])],
            "Landsize": [float(request.json["Landsize"])],
            "BuildingArea": [float(request.json["BuildingArea"])],
            "YearBuilt": [int(request.json["YearBuilt"])],
        }

        # Convert to DataFrame for model prediction
        df = pd.DataFrame(data)
        prediction = model.predict(df)[0]

        return jsonify({"predicted_price": round(prediction, 2)})

    except Exception as e:
        logging.error(f"Prediction error: {e}")
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True, port=8000)