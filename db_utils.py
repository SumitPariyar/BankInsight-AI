
import re
import pandas as pd
from sqlalchemy import create_engine, text

engine = create_engine("sqlite:///data/mydb.db", connect_args={"check_same_thread": False})
SELECT_ONLY_RE = re.compile(r"^\s*SELECT\s", re.I)

def is_select_query(sql: str) -> bool:
    return bool(SELECT_ONLY_RE.match(sql.strip()))

def run_sql_safe(sql: str, limit: int = 200) -> pd.DataFrame:
    if not is_select_query(sql):
        raise ValueError("Only SELECT queries are allowed.")
    wrapped = f"SELECT * FROM ({sql}) LIMIT {limit}"
    with engine.connect() as conn:
        result = conn.execute(text(wrapped))
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
    return df
