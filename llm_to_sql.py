from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import create_sql_query_chain
from langchain.sql_database import SQLDatabase
import os

from dotenv import load_dotenv
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")




# Create connection to SQLite
db = SQLDatabase.from_uri("sqlite:///data/mydb.db")

# Initialize Gemini model (make sure GOOGLE_API_KEY is set)
llm = ChatGoogleGenerativeAI(
    model="models/gemini-2.5-flash",
    api_key=GEMINI_API_KEY,
    temperature=0
    )

# Create LangChain chain to generate SQL
chain = create_sql_query_chain(llm, db)

def generate_sql(question: str):
    """Generate SQL from plain English using Gemini."""
    sql_query = chain.invoke({"question": question+"""Only return pure SQL queries, no extra text.
                              Ensure the SQL syntax is compatible with SQLite.
                              No mardkdown formatting, only SQL code.
                              Expected response:
                                SELECT * FROM table_name WHERE condition;
                              Bad response:
                                Here is the SQL query you requested: 
                                ```sql
                                SELECT * FROM table_name WHERE condition;
                                ```
                                or 
                                The SQL query is: SELECT * FROM table_name WHERE condition;
                              """})
    return sql_query
