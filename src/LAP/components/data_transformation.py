import os
import sys
from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

from src.LAP.exception import CustomException
from src.LAP.logger import logging
from src.LAP.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path=os.path.join('artifacts','preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config= DataTransformationConfig()

    def get_data_transformation_object(self):
        try:
            # df=pd.read_csv(r"C:\Users\asd\Desktop\Loan-Approval-Prediction\artifacts\raw.csvv")

            # numerical_columns=[col for col in df.columns if df[col].dtype != "O"]
            # logging.info('Numerical columns are:',numerical_columns)
            discrete_numerical_columns = ['Credit_History','Loan_Amount_Term']
            continuous_numerical_columns = ['LoanAmount','CoapplicantIncome','ApplicantIncome']
            categorical_columns = ['Gender','Married','Dependents','Education','Self_Employed','Property_Area'] 

            # categorical_columns=[col for col in df.columns if df[col].dtype == "O"]
            # logging.info('Categorical Columns are:',categorical_columns)
            

            discrete_num_pipeline = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='most_frequent')),
                ('scaler', StandardScaler())
                ])

            continuous_num_pipeline = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='median')),
                ('scaler', StandardScaler())
                ])

            cat_pipeline = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='most_frequent')),
                ('one_hot_encoder', OneHotEncoder(handle_unknown='ignore'))
                ])

            # ColumnTransformer
            preprocessor = ColumnTransformer(transformers=[
                ('discrete', discrete_num_pipeline, discrete_numerical_columns),
                ('continuous', continuous_num_pipeline, continuous_numerical_columns),
                ('categorical', cat_pipeline, categorical_columns)
                ])

            logging.info(f"Categorical:{categorical_columns}")
            logging.info(f"Numerical Columns:{discrete_numerical_columns}")
            logging.info(f"Numerical Columns:{continuous_numerical_columns}")


            return preprocessor
        
        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_data_transformation(self, train_path, test_path):
        """Read train and test CSVs, infer column types dynamically, build preprocessing pipeline, and return transformed arrays.

        Returns:
            tuple: (train_array, test_array, preprocessor_path)
        """
        try:
            # Load data
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            logging.info('Reading the train and test files')

            # Identify target column
            target_column_name = 'Loan_Status'
            if target_column_name not in train_df.columns or target_column_name not in test_df.columns:
                raise CustomException(f"Target column '{target_column_name}' not found in input data", sys)

            # Separate features and target
            X_train = train_df.drop(columns=[target_column_name])
            y_train = train_df[target_column_name]
            X_test = test_df.drop(columns=[target_column_name])
            y_test = test_df[target_column_name]

            # Dynamically infer column types
            categorical_cols = X_train.select_dtypes(include=['object', 'category']).columns.tolist()
            numeric_cols = X_train.select_dtypes(include=[np.number]).columns.tolist()

            # Split numeric columns into discrete (few unique values) and continuous
            discrete_numeric_cols = [c for c in numeric_cols if X_train[c].nunique() < 10]
            continuous_numeric_cols = [c for c in numeric_cols if c not in discrete_numeric_cols]

            # Pipelines
            discrete_num_pipeline = Pipeline([
                ('imputer', SimpleImputer(strategy='most_frequent')),
                ('scaler', StandardScaler())
            ])
            continuous_num_pipeline = Pipeline([
                ('imputer', SimpleImputer(strategy='median')),
                ('scaler', StandardScaler())
            ])
            cat_pipeline = Pipeline([
                ('imputer', SimpleImputer(strategy='most_frequent')),
                ('one_hot_encoder', OneHotEncoder(handle_unknown='ignore'))
            ])

            # ColumnTransformer
            preprocessor = ColumnTransformer([
                ('discrete', discrete_num_pipeline, discrete_numeric_cols),
                ('continuous', continuous_num_pipeline, continuous_numeric_cols),
                ('categorical', cat_pipeline, categorical_cols)
            ])

            logging.info('Applying preprocessing on training and test dataframes')
            X_train_arr = preprocessor.fit_transform(X_train)
            X_test_arr = preprocessor.transform(X_test)

            # Ensure dense array
            if hasattr(X_train_arr, "toarray"):
                X_train_arr = X_train_arr.toarray()
            if hasattr(X_test_arr, "toarray"):
                X_test_arr = X_test_arr.toarray()

            # Ensure 2D
            if X_train_arr.ndim == 1: X_train_arr = X_train_arr.reshape(-1, 1)
            if X_test_arr.ndim == 1: X_test_arr = X_test_arr.reshape(-1, 1)

            # Log shapes
            logging.info(f"X_train_arr shape: {X_train_arr.shape}, y_train shape: {y_train.shape}")
            logging.info(f"X_test_arr shape: {X_test_arr.shape}, y_test shape: {y_test.shape}")

            # Combine features and target back into arrays
            train_arr = np.c_[X_train_arr, np.array(y_train).reshape(-1, 1)]
            test_arr = np.c_[X_test_arr, np.array(y_test).reshape(-1, 1)]

            # Save preprocessing object
            preprocessor_path = self.data_transformation_config.preprocessor_obj_file_path
            save_object(file_path=preprocessor_path, obj=preprocessor)
            logging.info(f"Saved preprocessing object to {preprocessor_path}")

            return train_arr, test_arr, preprocessor_path
        except Exception as e:
            raise CustomException(e, sys)