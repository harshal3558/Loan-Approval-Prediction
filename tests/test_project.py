import os
import sys
import tempfile
import numpy as np
import pandas as pd
import pytest

# Ensure project root is in sys.path for imports
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Duplicate PROJECT_ROOT line removed
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from src.LAP.components.data_transformation import DataTransformation
from src.LAP.components.model_trainer import ModelTrainer


def test_initiate_data_transformation_basic():
    # Create a tiny dataset with both numeric and categorical columns
    df = pd.DataFrame({
        "Gender": ["Male", "Female"],
        "Married": ["Yes", "No"],
        "LoanAmount": [100.0, 200.0],
        "Loan_Status": ["Y", "N"]
    })
    # Write train and test CSVs
    with tempfile.TemporaryDirectory() as tmpdir:
        train_path = os.path.join(tmpdir, "train.csv")
        test_path = os.path.join(tmpdir, "test.csv")
        df.to_csv(train_path, index=False)
        df.to_csv(test_path, index=False)

        dt = DataTransformation()
        train_arr, test_arr, preproc_path = dt.initiate_data_transformation(train_path, test_path)
        # Expect rows and at least one feature column + target
        assert train_arr.shape[0] == 2
        assert test_arr.shape[0] == 2
        # Preprocessor file should exist
        assert os.path.isfile(preproc_path)


def test_eval_metrics_positive_label_detection():
    mt = ModelTrainer()
    actual = np.array(["Y", "N", "Y", "N"])
    pred = np.array(["Y", "Y", "Y", "N"])
    accuracy, precision, f1 = mt.eval_metrics(actual, pred)
    assert 0.0 <= accuracy <= 1.0
    assert 0.0 <= precision <= 1.0
    assert 0.0 <= f1 <= 1.0
    # Numeric fallback
    actual_num = np.array([1, 0, 1, 0])
    pred_num = np.array([1, 1, 1, 0])
    accuracy2, precision2, f12 = mt.eval_metrics(actual_num, pred_num)
    assert 0.0 <= accuracy2 <= 1.0
    assert 0.0 <= precision2 <= 1.0
    assert 0.0 <= f12 <= 1.0
