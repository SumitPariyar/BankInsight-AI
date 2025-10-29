# combined_app.py
import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="📊 Unified Dashboard & Churn Predictor", layout="wide")
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Churn Prediction", "NL2SQL Query", "Dashboard"])

# -------------------
# Churn Prediction
# -------------------
if page == "Churn Prediction":
    st.header("🏦 Bank Customer Churn Prediction")
    st.write("Predict if a bank customer is likely to churn or stay.")
    with st.form("churn_form"):
        gender = st.selectbox("Gender", ["Female", "Male"])
        subscription = st.selectbox("Subscription Type", ["Basic", "Standard", "Premium"])
        contract = st.selectbox("Contract Length", ["Monthly", "Quarterly", "Annual"])
        age = st.number_input("Age", min_value=18, max_value=100, value=30)
        tenure = st.number_input("Tenure (months)", min_value=0, max_value=120, value=12)
        usage_frequency = st.number_input("Usage Frequency (per month)", min_value=0, max_value=100, value=10)
        support_calls = st.number_input("Support Calls (last month)", min_value=0, max_value=50, value=0)
        payment_delay = st.number_input("Payment Delay (days)", min_value=0, max_value=365, value=0)
        total_spend = st.number_input("Total Spend ($)", min_value=0, value=1000)
        submitted = st.form_submit_button("Predict Churn")
    if submitted:
        payload = {
            "Gender": gender,
            "Subscription_Type": subscription,
            "Contract_Length": contract,
            "Age": age,
            "Tenure": tenure,
            "Usage_Frequency": usage_frequency,
            "Support_Calls": support_calls,
            "Payment_Delay": payment_delay,
            "Total_Spend": total_spend
        }
        try:
            resp = requests.post(f"{API_URL}/predict-churn", json=payload)
            result = resp.json()
            if result["churn"]:
                st.error(f"⚠️ This customer is likely to CHURN. Probability: {result['probability']:.2f}")
            else:
                st.success(f"✅ This customer is likely to STAY. Probability: {result['probability']:.2f}")
        except Exception as e:
            st.error(f"API error: {e}")

# -------------------
# NL2SQL Query
# -------------------
elif page == "NL2SQL Query":
    st.header("🧠 Natural Language to SQL Query")
    question = st.text_area("Enter your question:", placeholder="e.g., Show all customers who spent more than $1000 last year.")
    if st.button("Generate SQL & Run") and question:
        try:
            sql_resp = requests.post(f"{API_URL}/generate-sql", json={"question": question})
            sql_query = sql_resp.json()["sql"]
            st.code(sql_query, language="sql")
            run_resp = requests.post(f"{API_URL}/run-sql", json={"sql": sql_query})
            data = run_resp.json()
            if data["rows"]:
                df = pd.DataFrame(data["rows"], columns=data["columns"])
                st.dataframe(df)
                st.success(f"Returned {len(df)} rows.")
            else:
                st.warning("No data returned.")
        except Exception as e:
            st.error(f"API error: {e}")

# -------------------
# Dashboard
# -------------------
elif page == "Dashboard":
    st.header("📊 Data Visualization Dashboard")
    try:
        tables_resp = requests.get(f"{API_URL}/tables")
        tables = tables_resp.json()["tables"]
        if tables:
            table_choice = st.selectbox("Select Table", tables)
            # Automatically load table data when a table is selected
            if table_choice:
                data_resp = requests.get(f"{API_URL}/table-data", params={"table": table_choice, "limit": 500})
                data = data_resp.json()
                df = pd.DataFrame(data["rows"], columns=data["columns"])
                st.dataframe(df)
                st.markdown("### 📋 Table Summary")
                st.write(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
                st.write("**Column Types:**")
                st.write(df.dtypes)
                with st.expander("🔍 View Summary Statistics"):
                    st.write(df.describe(include="all"))
                st.markdown("### 📈 Create Chart")
                numeric_cols = df.select_dtypes(include=["int", "float"]).columns.tolist()
                categorical_cols = df.select_dtypes(include=["object"]).columns.tolist()
                chart_type = st.selectbox("Chart Type", ["Bar", "Line", "Pie", "Scatter"])
                if chart_type in ["Bar", "Line"] and numeric_cols:
                    x_axis = st.selectbox("X-axis", categorical_cols + numeric_cols)
                    y_axis = st.selectbox("Y-axis", numeric_cols)
                    if chart_type == "Bar":
                        fig = px.bar(df, x=x_axis, y=y_axis)
                    else:
                        fig = px.line(df, x=x_axis, y=y_axis)
                    st.plotly_chart(fig, use_container_width=True)
                elif chart_type == "Pie" and categorical_cols and numeric_cols:
                    names = st.selectbox("Category (for Pie)", categorical_cols)
                    values = st.selectbox("Values (for Pie)", numeric_cols)
                    fig = px.pie(df, names=names, values=values)
                    st.plotly_chart(fig, use_container_width=True)
                elif chart_type == "Scatter" and len(numeric_cols) >= 2:
                    x_axis = st.selectbox("X-axis", numeric_cols)
                    y_axis = st.selectbox("Y-axis", numeric_cols, index=1)
                    color_col = st.selectbox("Color by (optional)", [None] + categorical_cols)
                    fig = px.scatter(df, x=x_axis, y=y_axis, color=color_col)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Select valid columns for chart.")
        else:
            st.warning("No tables found in database.")
    except Exception as e:
        st.error(f"API error: {e}")
