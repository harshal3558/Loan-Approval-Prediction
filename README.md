# 💰 Loan Approval Prediction System

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0.3-black?logo=flask&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?logo=docker&logoColor=white)
![Azure](https://img.shields.io/badge/Azure-Web%20App-0078D4?logo=microsoftazure&logoColor=white)
![DVC](https://img.shields.io/badge/DVC-Data%20Version%20Control-945DD6?logo=dvc&logoColor=white)
![Git](https://img.shields.io/badge/Git-2.47-F05032?logo=git&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

An end-to-end Machine Learning solution designed to predict loan approval eligibility based on applicant details. This system automates the loan process and provides instant results using advanced classification algorithms, fully containerized and ready for cloud deployment.

---

## 📋 Table of Contents
- [About the Project](#-about-the-project)
- [Key Features](#-key-features)
- [Tech Stack](#-tech-stack)
- [Project Architecture](#-project-architecture)
- [Data Versioning](#-data-versioning)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Local Installation](#local-installation)
  - [Running with Docker](#running-with-docker)
- [Deployment on Azure](#-deployment-on-azure)
- [API Endpoints](#-api-endpoints)
- [Contributing](#-contributing)
- [Contact](#-contact)

---

## 📖 About the Project

The **Loan Approval Prediction System** streamlines the decision-making process for financial institutions. By analyzing factors such as income, credit history, education, and marital status, the system predicts whether a loan application is likely to be approved.

Built with a modular design, the project follows industry best practices for ML pipelines, including automated data ingestion from SQL databases, feature engineering, model training with hyperparameter tuning, and a responsive web interface.

---

## ✨ Key Features
- **Intelligent Prediction**: Uses high-performance algorithms (XGBoost, CatBoost, LightGBM) optimized via GridSearchCV.
- **SQL Integration**: Seamlessly fetches training data from MySQL databases.
- **User-Friendly Dashboard**: Easy-to-use web interface for manual data entry and instant results.
- **Robust Pipeline**: Automated Data Ingestion, Transformation, and Model Training components.
- **Production Ready**: Fully Dockerized with Gunicorn for stable deployment.
- **Experiment Tracking**: Integrated with MLflow for monitoring model performance and experiments.

---

## 🛠 Tech Stack

| Category | Technologies |
|----------|--------------|
| **Backend** | Python, Flask, Gunicorn |
| **Machine Learning** | Scikit-learn, XGBoost, LightGBM, CatBoost, Pandas, NumPy |
| **Visualizations** | Matplotlib, Seaborn, Plotly |
| **Database** | MySQL (PyMySQL) |
| **Version Control** | Git, DVC (Data Version Control) |
| **DevOps & Cloud** | Docker, Azure Container Registry (ACR), Azure Web App, GitHub Actions |
| **Monitoring** | MLflow |

---

## 📂 Project Architecture

```
Loan-Approval-Prediction/
├── .github/workflows/    # CI/CD Pipelines
├── artifacts/            # Trained models (pickle) and preprocessors
├── notebook/             # EDA and experimentation notebooks
├── src/                  # Core source code
│   └── LAP/              # Main package
│       ├── components/   # Ingestion, Transformation, Trainer, Monitoring
│       ├── pipelines/    # Training and Prediction scripts
│       ├── utils.py      # Common utilities and SQL handlers
│       └── logger.py     # Logging setup
├── templates/            # HTML front-end (index.html, home.html)
├── application.py        # Flask application entry point
├── Dockerfile            # Container configuration
├── requirements.txt      # Project dependencies
└── setup.py              # Package setup file
```

---

## 💾 Data Versioning

This project uses **DVC (Data Version Control)** to manage large datasets and model artifacts without bloating the Git repository.

**Key benefits:**
- **Reproducibility**: Track exactly which data version was used for a specific model.
- **Remote Storage**: Store heavy `.pkl` and `.csv` files in cloud storage.

To sync data/models:
```bash
dvc pull
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- MySQL Server (running with a 'loan' table)
- Git & Docker

### Local Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/harshal3558/Loan-Approval-Prediction.git
   cd Loan-Approval-Prediction
   ```

2. **Setup Environment**
   ```bash
   conda create -p lenv python=3.10 -y
   conda activate ./lenv
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Database**
   Create a `.env` file with your SQL credentials:
   ```env
   host=localhost
   user=root
   password=yourpassword
   db=yourdatabase
   ```

5. **Run the Application**
   ```bash
   python application.py
   ```
   Visit `http://127.0.0.1:5000`

### Running with Docker

1. **Build the Image**
   ```bash
   docker build -t loan-prediction-app .
   ```

2. **Run the Container**
   ```bash
   docker run -p 5000:5000 loan-prediction-app
   ```

---

## ☁ Deployment on Azure

Deployment is optimized for **Azure Web App for Containers**.

1. **Push to ACR**:
   ```bash
   az acr login --name <your-registry>
   docker tag loan-prediction-app <your-registry>.azurecr.io/loan-app:v1
   docker push <your-registry>.azurecr.io/loan-app:v1
   ```

2. **Deploy**: Configure the Azure Web App to pull from your ACR registry.

---

## 🔌 API Endpoints

- **`GET /`**: Home page.
- **`GET /predictdata`**: Renders the application form.
- **`POST /predictdata`**: Processes form data and returns prediction.
- **`GET /hello`**: Status check endpoint.

**Required Inputs:**
Gender, Married, Dependents, Education, Self_Employed, ApplicantIncome, CoapplicantIncome, LoanAmount, Loan_Amount_Term, Credit_History, Property_Area.

---

## 🤝 Contributing

1. Fork the Project
2. Create Feature Branch (`git checkout -b feature/NewFeature`)
3. Commit Changes (`git commit -m 'Add NewFeature'`)
4. Push to Branch (`git push origin feature/NewFeature`)
5. Open a Pull Request

---

## 📩 Contact

**Harshal** - [harshal3558@gmail.com](mailto:harshal3558@gmail.com)

Project Link: [https://github.com/harshal3558/Loan-Approval-Prediction](https://github.com/harshal3558/Loan-Approval-Prediction)