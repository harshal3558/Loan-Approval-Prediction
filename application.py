from flask import Flask, request, render_template

from src.LAP.pipelines.prediction_pipeline import CustomData, PredictPipeline

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/predictdata", methods=["GET", "POST"])
def predict_datapoint():

    # Load page (iframe support)
    if request.method == "GET":
        return render_template("home.html")

    try:
        # ✅ Collect form data (must match HTML names exactly)
        data = CustomData(
            Gender=request.form.get("Gender"),
            Married=request.form.get("Married"),
            Dependents=request.form.get("Dependents"),
            Education=request.form.get("Education"),
            Self_Employed=request.form.get("Self_Employed"),
            ApplicantIncome=int(request.form.get("ApplicantIncome")),
            CoapplicantIncome=int(request.form.get("CoapplicantIncome")),
            LoanAmount=int(request.form.get("LoanAmount")),
            Loan_Amount_Term=int(request.form.get("Loan_Amount_Term")),
            Credit_History=float(request.form.get("Credit_History")),
            Property_Area=request.form.get("Property_Area")
        )

        # 🔥 FIXED METHOD NAME (THIS WAS YOUR ERROR)
        pred_df = data.get_data_as_data_frame()

        pipeline = PredictPipeline()
        result = pipeline.predict(pred_df)

        prediction = "🔴 Loan Rejected" if result[0] == 1 else "🟢 Loan Approved"

        return f"""
        <div style="font-size:18px; font-weight:bold; text-align:center;">
            {prediction}
        </div>
        """

    except Exception as e:
        return f"""
        <div style="color:red; font-weight:bold; text-align:center;">
            Error: {str(e)}
        </div>
        """


if __name__ == "__main__":
    app.run(debug=True)