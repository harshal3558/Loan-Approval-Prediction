# Loan Approval Prediction System – Senior Engineer Documentation

---

## 📌 Project Overview
A production‑grade machine‑learning service that predicts loan approval eligibility in real‑time. It integrates robust data ingestion from MySQL, feature engineering, model training (XGBoost, LightGBM, CatBoost), and a low‑latency Flask API, all containerized for cloud deployment.

- **Goal**: Automate loan eligibility decisions with high accuracy and full auditability.
- **Key Metrics**: Model F1‑score > 0.92, inference latency < 200 ms, uptime 99.9%.

---

## 🏗️ Architecture Diagram
```mermaid
flowchart LR
    subgraph Data
        Ingestion[Data Ingestion (MySQL)] --> FeatureStore[Feature Store]
    end
    subgraph Training
        FeatureStore --> Trainer[Model Training (XGBoost, LightGBM, CatBoost)]
        Trainer --> ModelRegistry[Model Registry (MLflow)]
    end
    subgraph Deployment
        ModelRegistry --> API[Flask API Service]
        API --> FrontEnd[Frontend (HTML/JS)]
        API --> Monitoring[MLflow Tracking]
    end
    subgraph CI/CD
        GitHubActions[GitHub Actions] --> Docker[Docker Image]
        Docker --> AWS[ECS/Fargate]
    end
```

---

## 🛠️ Tech Stack
| Category | Technologies |
|----------|--------------|
| **Backend** | Python 3.10+, Flask 3.0.3, Gunicorn |
| **ML** | scikit‑learn, XGBoost, LightGBM, CatBoost, Pandas, NumPy |
| **Data Versioning** | DVC, MLflow |
| **Container** | Docker, Docker Compose |
| **CI/CD** | GitHub Actions, AWS ECR, IAM, ECS (Fargate) |
| **Database** | MySQL (PyMySQL) |
| **Monitoring** | MLflow UI, AWS CloudWatch |
| **Testing** | pytest, coverage |

---

## 📦 Installation & Deployment
### Local Development
1. **Clone the repository**
```bash
git clone https://github.com/harshal3558/Loan-Approval-Prediction.git
cd Loan-Approval-Prediction
```
2. **Create a Python environment**
```bash
conda create -p ./lenv python=3.10 -y
conda activate ./lenv
```
3. **Install dependencies**
```bash
pip install -r requirements.txt
```
4. **Configure secrets** – copy `.env.example` to `.env` and fill MySQL credentials.
5. **Run the service**
```bash
python application.py
```
   Visit `http://127.0.0.1:5000`.

---

### Docker
```bash
# Build the image
docker build -t loan-prediction-app .
# Run the container
docker run -p 5000:5000 loan-prediction-app
```

---

### ☁ AWS Deployment
1. **Push image to Amazon ECR**
```bash
aws ecr get-login-password --region <region> |
  docker login --username AWS --password-stdin <aws_account_id>.dkr.ecr.<region>.amazonaws.com

docker tag loan-prediction-app:latest <aws_account_id>.dkr.ecr.<region>.amazonaws.com/loan-app:latest
docker push <aws_account_id>.dkr.ecr.<region>.amazonaws.com/loan-app:latest
```
2. **Create an ECS Fargate Task Definition** (via AWS Console or CLI) that references the image.
3. **Run the service on ECS** using the task definition, configure CPU/memory, and attach an Application Load Balancer (ALB) for HTTPS termination.
4. **Configure environment variables** (e.g., `DB_HOST`, `DB_USER`, `DB_PASSWORD`) in the task definition or via AWS Systems Manager Parameter Store.
5. **Enable logging** → forward container logs to CloudWatch for monitoring.

---
## 📹 Demo Video
Watch the deployment walkthrough:
[Deployment Video](https://drive.google.com/file/d/1XPcGe21EjQXIbaMoPnQJstcbxX67TR3I/view?usp=sharing)

---

## 🔌 API Reference
| Method | Endpoint | Description | Example |
|--------|----------|-------------|---------|
| `GET` | `/` | Health‑check (returns HTML home page) | `curl http://localhost:5000/` |
| `GET` | `/predictdata` | Render input form | `curl http://localhost:5000/predictdata` |
| `POST` | `/predictdata` | Accepts loan applicant fields, returns prediction | `curl -X POST -d "Gender=Male&Married=Yes&..." http://localhost:5000/predictdata` |

**Request payload** (form‑url‑encoded): `Gender, Married, Dependents, Education, Self_Employed, ApplicantIncome, CoapplicantIncome, LoanAmount, Loan_Amount_Term, Credit_History, Property_Area`.

**Response** – HTML snippet containing a green ✅ (approved) or red ❌ (rejected) badge.

---

## 📈 Operational Guidance
- **Logging**: Structured JSON logs via `src/LAP/logger.py`; rotated daily.
- **Monitoring**: MLflow UI (`http://localhost:5000/mlflow`) for experiment tracking; CloudWatch metrics for ECS health.
- **Health Checks**: `/` endpoint returns `200 OK`; configure ALB health probe accordingly.
- **Scaling**: ECS Fargate automatically scales with desired task count; stateless design ensures horizontal scaling.
- **Security**: Store DB credentials in AWS Secrets Manager or Parameter Store; enforce HTTPS via ALB.

---

## 🧪 Testing Strategy
- **Unit Tests** – located in `tests/unit/`; run with `pytest`.
- **Integration Tests** – spin up Docker Compose stack and hit API endpoints.
- **Coverage Goal** – ≥ 85 % code coverage; enforced via CI badge.
- **CI Pipeline** – GitHub Actions runs lint (`ruff`), tests, builds Docker image, and pushes to ECR on merge.

---

## 🤝 Contribution Guidelines
1. Fork the repository.
2. Create a feature branch (`git checkout -b feat/xyz`).
3. Follow PEP‑8 and run `ruff check .` for linting.
4. Write unit tests for any new functionality.
5. Submit a PR with a clear description and reference the related issue.
6. Ensure the PR passes all CI checks before merging.

---

## 📜 License & Contact
**License:** MIT © 2024 Harshal

**Maintainer:** Harshal – [harshal3558@gmail.com](mailto:harshal3558@gmail.com)

Project link: https://github.com/harshal3558/Loan-Approval-Prediction