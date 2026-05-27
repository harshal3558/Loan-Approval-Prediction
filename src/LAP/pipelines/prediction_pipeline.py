import sys
import pandas as pd
from src.LAP.exception import CustomException
from src.LAP.utils import load_object
import os

class PredictPipeline:
    def __init__(self):
        pass

    def predict(self, features: pd.DataFrame):
        """Predict loan approval status.

        Parameters
        ----------
        features : pd.DataFrame
            DataFrame containing the input features. Must include the same columns
            that were used during training. Missing columns are filled with a
            placeholder value (0) to avoid shape mismatches.
        """
        try:
            # Ensure stdout can handle Unicode (emoji) from mlflow or other logging
            if hasattr(sys.stdout, "reconfigure"):
                sys.stdout.reconfigure(encoding='utf-8')

            project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
            model_path = os.path.join(project_root, "artifacts", "model.pkl")
            preprocessor_path = os.path.join(project_root, "artifacts", "preprocessor.pkl")

            model = load_object(file_path=model_path)
            preprocessor = load_object(file_path=preprocessor_path)

            # Align features with the preprocessor expectations
            expected_cols = getattr(preprocessor, "feature_names_in_", None)
            if expected_cols is not None:
                # Add any missing columns with a default placeholder (0)
                missing = set(expected_cols) - set(features.columns)
                for col in missing:
                    features[col] = 0
                # Reorder columns to match training order
                features = features[expected_cols]
            else:
                # Preprocessor does not expose expected columns; ensure Loan_ID exists as placeholder
                if 'Loan_ID' not in features.columns:
                    features['Loan_ID'] = 0

            data_scaled = preprocessor.transform(features)

            preds = model.predict(data_scaled)
            return preds

        except Exception as e:
            raise CustomException(e,sys)
        

class CustomData:
    def __init__(self,
                 Gender: str,
                 Married: str,
                 Dependents: str,
                 Education: str,
                 Self_Employed: str,
                 ApplicantIncome: float,
                 CoapplicantIncome: float,
                 LoanAmount: float,
                 Loan_Amount_Term: float,
                 Credit_History: float,
                 Property_Area: str):
        
        self.Gender = Gender
        self.Married = Married
        self.Dependents = Dependents
        self.Education = Education
        self.Self_Employed = Self_Employed
        self.ApplicantIncome = ApplicantIncome
        self.CoapplicantIncome = CoapplicantIncome
        self.LoanAmount = LoanAmount
        self.Loan_Amount_Term = Loan_Amount_Term
        self.Credit_History = Credit_History
        self.Property_Area = Property_Area
    
    def get_data_as_data_frame(self):
        try:
            custom_data_input_dict = {
                "Gender": [self.Gender],
                "Married": [self.Married],
                "Dependents": [self.Dependents],
                "Education": [self.Education],
                "Self_Employed": [self.Self_Employed],
                "ApplicantIncome": [self.ApplicantIncome],
                "CoapplicantIncome": [self.CoapplicantIncome],
                "LoanAmount": [self.LoanAmount],
                "Loan_Amount_Term": [self.Loan_Amount_Term],
                "Credit_History": [self.Credit_History],
                "Property_Area": [self.Property_Area]
            }
            return pd.DataFrame(custom_data_input_dict)
        except Exception as e:
            raise CustomException(e, sys)
