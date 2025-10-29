import pandas as pd
from sqlalchemy import create_engine

csv_path = "data/customer_churn_dataset-training-master.csv"
db_path = "sqlite:///data/mydb.db"

df = pd.read_csv(csv_path)
engine = create_engine(db_path)
df.to_sql("my_table", engine, if_exists="replace", index=False)

print("✅ CSV successfully loaded into SQLite table 'my_table'")
