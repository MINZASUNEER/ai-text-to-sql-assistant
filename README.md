# AI Text-to-SQL Assistant

An AI-powered web application that converts natural-language questions into SQL queries and executes them against a SQLite database.

## Features

- Ask database questions using natural language
- AI-powered SQL generation using Google Gemini
- Automatic database schema detection
- SQL safety validation
- Only SELECT queries are allowed
- SQLite database integration
- Display query results in a table
- FastAPI REST API
- React and TypeScript frontend
- Swagger API documentation

## Tech Stack

### Frontend

- React
- TypeScript
- Vite
- HTML
- CSS

### Backend

- Python
- FastAPI
- Pydantic
- Uvicorn

### AI

- Google Gemini API

### Database

- SQLite

## How It Works

1. User enters a question in natural language.
2. React sends the question to the FastAPI backend.
3. The backend reads the database schema.
4. Google Gemini generates a SQL query.
5. The SQL query is checked for safety.
6. The validated query is executed against SQLite.
7. The results are displayed in the React frontend.

## Example Questions

```text
Show me all students
Show me students older than 20
List all departments
Show all teachers
How many students are there?