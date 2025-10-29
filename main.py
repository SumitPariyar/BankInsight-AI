from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import pickle
from pydantic import BaseModel
from sqlalchemy import create_engine, text
import os

# ---------------------------------------------------
# 🔧 FASTAPI CONFIG
# ---------------------------------------------------
app = FastAPI()

# Allow Streamlit or any frontend to access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "✅ API is running successfully"}

# ---------------------------------------------------
# 🧠 MODEL LOADING
# ---------------------------------------------------

# Recreate the missing custom function here BEFORE loading model
def custom_encoder(data):
    # Accept either dict or DataFrame
    if isinstance(data, dict):
        df = pd.DataFrame([data])
    else:
        df = data.copy()
    # Map only if column exists and is string type
    if "Gender" in df.columns and df["Gender"].dtype == object:
        df["Gender"] = df["Gender"].map({"Female": 0, "Male": 1})
    if "Subscription Type" in df.columns and df["Subscription Type"].dtype == object:
        subscription_mapping = {"Basic": 0, "Standard": 1, "Premium": 2}
        df["Subscription Type"] = df["Subscription Type"].map(subscription_mapping)
    if "Contract Length" in df.columns and df["Contract Length"].dtype == object:
        contract_mapping = {"Monthly": 0, "Quarterly": 1, "Annual": 2}
        df["Contract Length"] = df["Contract Length"].map(contract_mapping)
    final_columns = [
        "Age", "Gender", "Tenure", "Usage Frequency", "Support Calls", "Payment Delay",
        "Subscription Type", "Contract Length", "Total Spend"
    ]
    return df[final_columns]

# 🩵 Load the model safely
MODEL_PATH = "Final_AI_churn_pipeline_labelencoded.pkl"
DB_PATH = "data/mydb.db"

def load_model():
    import sys
    # Register the function name globally so pickle can find it
    import __main__
    __main__.custom_encoder = custom_encoder

    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    return model

model = load_model()

# ---------------------------------------------------
# 📦 PYDANTIC INPUT MODEL
# ---------------------------------------------------
class ChurnInput(BaseModel):
    Gender: str
    Subscription_Type: str
    Contract_Length: str
    Age: int
    Tenure: int
    Usage_Frequency: int
    Support_Calls: int
    Payment_Delay: int
    Total_Spend: float

# ---------------------------------------------------
# 🔮 PREDICTION ENDPOINT
# ---------------------------------------------------
@app.post("/predict-churn")
def predict_churn(input: ChurnInput):
    data = {
        "Gender": input.Gender,
        "Subscription Type": input.Subscription_Type,
        "Contract Length": input.Contract_Length,
        "Age": input.Age,
        "Tenure": input.Tenure,
        "Usage Frequency": input.Usage_Frequency,
        "Support Calls": input.Support_Calls,
        "Payment Delay": input.Payment_Delay,
        "Total Spend": input.Total_Spend
    }

    X = custom_encoder(data)
    proba = model.predict_proba(X)[:, 1][0]
    pred = model.predict(X)[0]

    return {"churn": bool(pred >= 0.5), "probability": float(proba)}

# ---------------------------------------------------
# 🧠 SQL GENERATION (Gemini or fallback)
# ---------------------------------------------------
try:
    from llm_to_sql import generate_sql
except ImportError:
    def generate_sql(question: str):
        return "SELECT * FROM my_table LIMIT 10;"  # fallback

class SQLGenInput(BaseModel):
    question: str

@app.post("/generate-sql")
def generate_sql_endpoint(input: SQLGenInput):
    sql = generate_sql(input.question)
    return {"sql": sql}

# ---------------------------------------------------
# 🧾 SQL EXECUTION
# ---------------------------------------------------
class SQLRunInput(BaseModel):
    sql: str

@app.post("/run-sql")
def run_sql_endpoint(input: SQLRunInput):
    engine = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})
    with engine.connect() as conn:
        df = pd.read_sql(input.sql, conn)
    return {"columns": df.columns.tolist(), "rows": df.values.tolist()}

# ---------------------------------------------------
# 📋 DATABASE UTILITIES
# ---------------------------------------------------
@app.get("/tables")
def list_tables():
    engine = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})
    with engine.connect() as conn:
        tables = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table';")).fetchall()
    return {"tables": [t[0] for t in tables]}

@app.get("/table-data")
def get_table_data(table: str, limit: int = 500):
    engine = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})
    with engine.connect() as conn:
        df = pd.read_sql(f"SELECT * FROM {table} LIMIT {limit}", conn)
    return {"columns": df.columns.tolist(), "rows": df.values.tolist()}
