from flask import Flask, request, render_template
import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler
from src.LAP.pipelines.prediction_pipeline import CustomData, PredictPipeline

application = Flask(__name__)
app = application

## Route for home page
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predictdata', methods=['GET', 'POST'])
def predict_datapoint():
    if request.method == 'GET':
        return render_template('home.html')
    else:
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
        print(pred_df)
        print('Before Prediction')

        predict_pipeline = PredictPipeline()
        print("Mid Prediction")
        results = predict_pipeline.predict(pred_df)
        print("After Prediction")

        return render_template('home.html', results=results[0])


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)





# from src.LAP.logger import logging
# from src.LAP.exception import CustomException
# from src.LAP.components.data_ingestion import DataIngestion
# from src.LAP.components.data_ingestion import DataIngestionConfig
# from src.LAP.components.data_transformation import DataTransformation
# from src.LAP.components.data_transformation import DataTransformationConfig
# from src.LAP.components.model_tranier import ModelTrainerConfig
# from src.LAP.components.model_tranier import ModelTrainer

# import sys

# if __name__ == "__main__":
#     logging.info("The execution has started")

#     try:
#         # data_ingestion_config=DataIngestionConfig()
#         data_ingestion=DataIngestion() 
#         # data_ingestion.initiate_data_ingestion()
#         train_data_path,test_data_path=data_ingestion.initiate_data_ingestion()

#         # data_transformation_config=DataIngestionConfig()
#         data_transformation=DataTransformation()
#         # data_transformation.initiate_data_transformation(train_data_path,test_data_path)
#         train_arr,test_arr,_=data_transformation.initiate_data_transformation(train_data_path,test_data_path)
        
#         # ## Model Training

#         model_trainer=ModelTrainer()
#         print(model_trainer.initiate_model_trainer(train_arr,test_arr))


#     except Exception as e:
#         logging.info("Custom Exception")
#         raise CustomException(e,sys)