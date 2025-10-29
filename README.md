# 🧠 AI-Powered Customer Churn Prediction & Analytics Dashboard

A complete **end-to-end AI system** built using **FastAPI**, **Streamlit**, and **Machine Learning** that predicts customer churn, generates insights from natural language queries (NL2SQL), and visualizes customer data interactively.

This project demonstrates how **data science**, **machine learning**, and **LLM-based automation** can work together in one integrated system — deployed from **local development** to **Azure Cloud**.

---

## 🚀 Key Features

- 🧩 **Machine Learning Churn Predictor**  
  Predicts whether a customer is likely to churn based on demographic and behavioral data.

- ⚙️ **FastAPI Backend**  
  Serves RESTful endpoints for predictions, SQL generation, and database operations.

- 📊 **Interactive Streamlit Dashboard**  
  Visualize customer data, create charts, and explore churn insights intuitively.

- 🤖 **Natural Language to SQL (NL2SQL)**  
  Uses Gemini + LangChain to convert human questions into SQL queries automatically.

- 🗄️ **SQLite Database Integration**  
  Perform live queries and visualize real-time results.

- ☁️ **Azure-Ready Deployment**  
  Designed for smooth deployment via GitHub → Azure App Service.

---

## 🏗️ Project Architecture




project-folder/
│
├── main.py # FastAPI backend (entry point)
├── combined_app.py # Streamlit dashboard
├── Final_AI_churn_pipeline_labelencoded.pkl # ML model
├── data/
│ └── mydb.db # SQLite database
├── requirements.txt # Dependencies
├── .gitignore
└── README.md # Project documentation






---

## 🧮 Tech Stack

| Category | Technology |
|-----------|-------------|
| **Language** | Python 3.10+ |
| **Frameworks** | FastAPI, Streamlit |
| **Machine Learning** | scikit-learn, XGBoost, imbalanced-learn |
| **Visualization** | Plotly, Seaborn, Matplotlib |
| **LLM Integration** | LangChain, Google Generative AI (Gemini) |
| **Database** | SQLite, SQLAlchemy |
| **Deployment** | Microsoft Azure App Service |
| **CI/CD** | GitHub + GitHub Actions |

---

## ⚙️ Installation Guide

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/sumitpariyar1001/azure-churn-app.git
cd azure-churn-app
