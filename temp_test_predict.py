import pandas as pd
import os, sys
sys.path.append(os.path.abspath('c:/Users/harsh/OneDrive/Desktop/Loan-Approval-Prediction'))
from src.LAP.pipelines.prediction_pipeline import PredictPipeline

# Create dummy features DataFrame matching training schema (excluding Loan_ID)
features = pd.DataFrame({
    'Gender': ['Male'],
    'Married': ['Yes'],
    'Dependents': ['0'],
    'Education': ['Graduate'],
    'Self_Employed': ['No'],
    'ApplicantIncome': [5000],
    'CoapplicantIncome': [0],
    'LoanAmount': [200],
    'Loan_Amount_Term': [360],
    'Credit_History': [1.0],
    'Property_Area': ['Urban']
})

print('Features columns:', features.columns.tolist())
pp = PredictPipeline()
print('Prediction result:', pp.predict(features))
