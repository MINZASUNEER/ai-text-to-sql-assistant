from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai

import os
import sqlite3
import re

from app.clarification import detect_ambiguity
from app.retriever import get_relevant_schema, index_schema


# --------------------------------------------------
# Load environment variables
# --------------------------------------------------

load_dotenv()


# --------------------------------------------------
# Create FastAPI app
# --------------------------------------------------

app = FastAPI()


# --------------------------------------------------
# Index database schema when backend starts
# --------------------------------------------------

@app.on_event("startup")
def startup_event():
    index_schema()


# --------------------------------------------------
# CORS
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174"
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
# SQL safety
# --------------------------------------------------

def is_safe_sql(sql):
    sql = sql.strip()

    # Remove markdown formatting if Gemini returns it
    sql = re.sub(
        r"```sql",
        "",
        sql,
        flags=re.IGNORECASE
    )

    sql = sql.replace("```", "").strip()

    # Only allow SELECT queries
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

        # Get column names
        columns = [
            description[0]
            for description in cursor.description
        ]

        # Make duplicate column names unique
        seen = {}
        unique_columns = []

        for column in columns:

            if column not in seen:

                seen[column] = 0
                unique_columns.append(column)

            else:

                seen[column] += 1

                unique_columns.append(
                    f"{column}_{seen[column]}"
                )

        # Convert rows into dictionaries
        results = [
            dict(zip(unique_columns, row))
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


    # --------------------------------------------------
    # Empty question
    # --------------------------------------------------

    if not question:

        return {
            "question": question,
            "status": "error",
            "clarification_question": None,
            "sql": "",
            "results": [],
            "error": "Please enter a question."
        }


    # --------------------------------------------------
    # 1. Ambiguity Check
    # --------------------------------------------------

    clarification_result = detect_ambiguity(question)

    if clarification_result["needs_clarification"]:

        return {
            "question": question,
            "status": "needs_clarification",
            "clarification_question": (
                clarification_result[
                    "clarification_question"
                ]
            ),
            "sql": "",
            "results": [],
            "error": None
        }


    # --------------------------------------------------
    # 2. RAG Schema Retrieval
    # --------------------------------------------------

    try:

        relevant_schema = get_relevant_schema(
            question,
            top_k=5
        )

    except Exception as error:

        print("RAG ERROR:", error)

        return {
            "question": question,
            "status": "error",
            "clarification_question": None,
            "sql": "",
            "results": [],
            "error": (
                f"Schema retrieval error: {str(error)}"
            )
        }


    # --------------------------------------------------
    # 3. Prompt Construction
    # --------------------------------------------------

    prompt = f"""
You are an expert Text-to-SQL assistant.

Convert the user's English question into a valid SQLite SQL query.

Use ONLY the database schema provided below.

Relevant Database Schema:
{relevant_schema}

User question:
{question}

Rules:

1. Return ONLY the SQL query.
2. Do not return explanations.
3. Do not use markdown code blocks.
4. Use only tables and columns present in the schema.
5. Use valid SQLite syntax.
6. Only generate SELECT queries.
7. If the question requires information from multiple tables,
   use an appropriate JOIN.
8. Use the relationships provided in the schema when joining tables.
9. When selecting columns with the same name from different tables,
   ALWAYS use clear aliases.
10. When filtering using a table from another table,
    use the appropriate JOIN.
11. Do not invent table names or column names.

Example:

SELECT
    students.name AS student_name,
    departments.name AS department_name
FROM students
JOIN departments
    ON students.department_id = departments.id;

SQL:
"""


    # --------------------------------------------------
    # 4. Generate SQL using Gemini
    # --------------------------------------------------

    try:

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        sql = response.text.strip()

    except Exception as error:

        # Print the REAL Gemini error in terminal
        print("========================================")
        print("GEMINI ERROR:")
        print(error)
        print("========================================")

        return {
            "question": question,
            "status": "error",
            "clarification_question": None,
            "sql": "",
            "results": [],
            "error": (
                "AI service is temporarily unavailable. "
                "Please try again."
            )
        }


    # --------------------------------------------------
    # Clean generated SQL
    # --------------------------------------------------

    sql = re.sub(
        r"```sql",
        "",
        sql,
        flags=re.IGNORECASE
    )

    sql = sql.replace("```", "").strip()


    # --------------------------------------------------
    # 5. SQL Safety Validation
    # --------------------------------------------------

    if not is_safe_sql(sql):

        print("UNSAFE SQL REJECTED:", sql)

        return {
            "question": question,
            "status": "error",
            "clarification_question": None,
            "sql": sql,
            "results": [],
            "error": (
                "The generated SQL query was "
                "rejected for safety reasons."
            )
        }


    # --------------------------------------------------
    # 6. Execute SQL
    # --------------------------------------------------

    try:

        results = execute_sql(sql)

    except Exception as error:

        print("SQL EXECUTION ERROR:", error)
        print("GENERATED SQL:", sql)

        return {
            "question": question,
            "status": "error",
            "clarification_question": None,
            "sql": sql,
            "results": [],
            "error": (
                "The generated SQL could not be executed."
            )
        }


    # --------------------------------------------------
    # 7. Return response
    # --------------------------------------------------

    return {
        "question": question,
        "status": "success",
        "clarification_question": None,
        "sql": sql,
        "results": results,
        "error": None
    }