import pandas as pd
import joblib

from app import app
from flask import jsonify, request
from http.client import HTTPException

model = joblib.load('model.joblib')

@app.errorhandler(Exception)
def handle_error(e):
    code = e.code if isinstance(e, HTTPException) else 500
    return jsonify(error=str(e)), code

@app.route('/predict', methods=['POST'])
def predict():
    if model:
        if request_body := request.get_json():
            df = pd.DataFrame([__encode(request_body)])
            pred_cols = list(df.columns.values)
            prediction = float(pd.Series(model.predict(df[pred_cols])))
            
            return jsonify(
                prediction=prediction,
                message="Prediction successful",
                category="Success",
                status=200
            )
    else:
        return jsonify(
            message="Model not found",
            category="Failure",
            status=400
        )

def __encode(d : dict) -> dict:
    """Simple function to encode the categorical input."""
    proximities = [
        'ocean_proximity_<1H OCEAN',
        'ocean_proximity_INLAND',
        'ocean_proximity_ISLAND',
        'ocean_proximity_NEAR BAY',
        'ocean_proximity_NEAR OCEAN'
    ]

    op = f"ocean_proximity_{d['ocean_proximity']}"
    d.pop('ocean_proximity')
    return d | {px: 1 if px == op else 0 for px in proximities}
