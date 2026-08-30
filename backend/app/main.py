from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai
import os
import sqlite3
import re

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI()


# --------------------------------------------------
# CORS
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# Gemini
# --------------------------------------------------

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY is not configured.")

client = genai.Client(api_key=api_key)


# --------------------------------------------------
# Request model
# --------------------------------------------------

class Question(BaseModel):
    question: str


# --------------------------------------------------
# Database schema
# --------------------------------------------------

def get_database_schema():

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        AND name NOT LIKE 'sqlite_%'
    """)

    tables = cursor.fetchall()

    schema = ""

    for table in tables:

        table_name = table[0]

        cursor.execute(
            f"PRAGMA table_info({table_name})"
        )

        columns = cursor.fetchall()

        column_names = [
            column[1]
            for column in columns
        ]

        schema += f"Table: {table_name}\n"
        schema += f"Columns: {', '.join(column_names)}\n\n"

    connection.close()

    return schema


# --------------------------------------------------
# SQL safety
# --------------------------------------------------

def is_safe_sql(sql):

    sql = sql.strip()

    # Remove markdown if Gemini accidentally returns it
    sql = re.sub(r"```sql", "", sql, flags=re.IGNORECASE)
    sql = sql.replace("```", "").strip()

    # Only allow SELECT
    if not sql.upper().startswith("SELECT"):
        return False

    dangerous_commands = [
        "INSERT",
        "UPDATE",
        "DELETE",
        "DROP",
        "ALTER",
        "CREATE",
        "REPLACE",
        "TRUNCATE",
        "ATTACH",
        "DETACH",
        "PRAGMA"
    ]

    upper_sql = sql.upper()

    for command in dangerous_commands:

        if re.search(rf"\b{command}\b", upper_sql):
            return False

    return True


# --------------------------------------------------
# Execute SQL
# --------------------------------------------------

def execute_sql(sql):

    connection = sqlite3.connect("database.db")

    try:

        cursor = connection.cursor()

        cursor.execute(sql)

        rows = cursor.fetchall()

        if cursor.description is None:
            return []

        columns = [
            description[0]
            for description in cursor.description
        ]

        results = [
            dict(zip(columns, row))
            for row in rows
        ]

        return results

    finally:

        connection.close()


# --------------------------------------------------
# Home
# --------------------------------------------------

@app.get("/")
def home():

    return {
        "message": "AI Text-to-SQL Assistant is running!"
    }


# --------------------------------------------------
# Ask AI
# --------------------------------------------------

@app.post("/ask")
def ask_question(data: Question):

    question = data.question.strip()

    # Check empty question
    if not question:

        return {
            "question": question,
            "sql": "",
            "results": [],
            "error": "Please enter a question."
        }


    # Get database schema
    try:

        schema = get_database_schema()

    except Exception as error:

        return {
            "question": question,
            "sql": "",
            "results": [],
            "error": f"Database error: {str(error)}"
        }


    # Gemini prompt
    prompt = f"""
You are a Text-to-SQL assistant.

Convert the user's English question into
a valid SQLite SQL query.

Database schema:

{schema}

User question:

{question}

Rules:
- Return ONLY the SQL query.
- Do not use markdown.
- Do not use ```sql.
- Use only tables and columns that exist.
- Use valid SQLite syntax.
- Only generate SELECT queries.

SQL:
"""


    # Ask Gemini
    try:

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        sql = response.text.strip()

    except Exception:

        return {
            "question": question,
            "sql": "",
            "results": [],
            "error": "AI service is temporarily unavailable. Please try again."
        }


    # Clean SQL
    sql = re.sub(
        r"```sql",
        "",
        sql,
        flags=re.IGNORECASE
    )

    sql = sql.replace("```", "").strip()


    # Check SQL safety
    if not is_safe_sql(sql):

        return {
            "question": question,
            "sql": sql,
            "results": [],
            "error": "The generated SQL query was rejected for safety reasons."
        }


    # Execute SQL
    try:

        results = execute_sql(sql)

    except Exception:

        return {
            "question": question,
            "sql": sql,
            "results": [],
            "error": "The generated SQL could not be executed."
        }


    # Successful response
    return {
        "question": question,
        "sql": sql,
        "results": results,
        "error": None
    }