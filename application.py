from flask import Flask, request, render_template
import numpy as np
import pandas as pd
from src.LAP.pipelines.prediction_pipeline import CustomData, PredictPipeline

application = Flask(__name__)
app = application

@app.route("/")
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/predictdata', methods=['GET', 'POST'])
def predict_datapoint():
    """Single route handles form display and prediction"""
    results = None
    
    if request.method == 'POST':
        try:
            data = CustomData(
                Gender=request.form.get('Gender'),
                Married=request.form.get('Married'),
                Dependents=request.form.get('Dependents'),
                Education=request.form.get('Education'),
                Self_Employed=request.form.get('Self_Employed'),
                ApplicantIncome=float(request.form.get('ApplicantIncome')),
                CoapplicantIncome=float(request.form.get('CoapplicantIncome')),
                LoanAmount=float(request.form.get('LoanAmount')),
                Loan_Amount_Term=float(request.form.get('Loan_Amount_Term')),
                Credit_History=float(request.form.get('Credit_History')),
                Property_Area=request.form.get('Property_Area')
            )

            pred_df = data.get_data_as_data_frame()
            print("Input data:", pred_df)
            
            predict_pipeline = PredictPipeline()
            results = predict_pipeline.predict(pred_df)[0]
            print(f"Prediction: {results}")
            
        except Exception as e:
            print(f"Error: {e}")
            results = -1
    
    return render_template('home.html', results=results)

@app.route("/hello")
def hello():
    return "Welcome to Loan Prediction System"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
