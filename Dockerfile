# =====================================
# 1️⃣ Base Image
# =====================================
FROM python:3.11-slim

# =====================================
# 2️⃣ Set working directory
# =====================================
WORKDIR /app

# =====================================
# 3️⃣ Copy project files
# =====================================
COPY . /app

# =====================================
# 4️⃣ Install dependencies
# =====================================
RUN pip install --no-cache-dir -r requirements.txt

# =====================================
# 5️⃣ Expose ports
# =====================================
# FastAPI → 8000 | Streamlit → 8501
EXPOSE 8000
EXPOSE 8501

# =====================================
# 6️⃣ Set permissions (optional but recommended)
# =====================================
RUN chmod -R 777 /app

# =====================================
# 7️⃣ Run both FastAPI + Streamlit
# =====================================
# 👉 Make sure:
#    - FastAPI file is main.py and app object is "combined_app"
#    - Streamlit file is combined_app.py
CMD ["bash", "-c", "uvicorn main:combined_app --host 0.0.0.0 --port 8000 & streamlit run combined_app.py --server.port 8501 --server.address 0.0.0.0"]
