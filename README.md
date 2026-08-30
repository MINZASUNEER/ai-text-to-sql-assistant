\# 🤖 AI Text-to-SQL Assistant



An AI-powered web application that converts \*\*natural-language questions into SQL queries\*\* and executes them against a SQLite database.



Instead of writing SQL manually, users can simply ask questions such as:



> "Show me all students older than 20"



The application uses \*\*Google Gemini\*\* to generate the SQL query, validates the generated query for safety, executes it against the database, and displays the results through a React interface.



\---



\## ✨ Features



\* 🗣️ Ask database questions using natural language

\* 🤖 AI-powered SQL generation using Google Gemini

\* 🧠 Automatic database schema detection

\* 🔐 SQL safety validation

\* 🛡️ Only `SELECT` queries are allowed

\* 🗄️ SQLite database integration

\* 📊 Display query results in a table

\* ⚡ FastAPI REST API

\* ⚛️ React + TypeScript frontend

\* 📖 Interactive Swagger API documentation

\* 🧹 Clear/reset query interface

\* ❌ User-friendly error handling



\---



\## 🛠️ Tech Stack



\### Frontend



\* React

\* TypeScript

\* Vite

\* HTML

\* CSS



\### Backend



\* Python

\* FastAPI

\* Pydantic

\* Uvicorn



\### AI



\* Google Gemini API



\### Database



\* SQLite



\### Development Tools



\* Git

\* GitHub

\* VS Code

\* Swagger / OpenAPI



\---



\## 🏗️ Architecture



```text

&#x20;                   ┌──────────────────────┐

&#x20;                   │        User          │

&#x20;                   │ Natural Language     │

&#x20;                   │      Question        │

&#x20;                   └──────────┬───────────┘

&#x20;                              │

&#x20;                              ▼

&#x20;                   ┌──────────────────────┐

&#x20;                   │   React Frontend     │

&#x20;                   │  TypeScript + Vite   │

&#x20;                   └──────────┬───────────┘

&#x20;                              │ HTTP POST

&#x20;                              ▼

&#x20;                   ┌──────────────────────┐

&#x20;                   │    FastAPI Backend   │

&#x20;                   │       /ask API       │

&#x20;                   └──────────┬───────────┘

&#x20;                              │

&#x20;                    ┌─────────┴─────────┐

&#x20;                    ▼                   ▼

&#x20;            ┌───────────────┐   ┌────────────────┐

&#x20;            │ Google Gemini │   │ SQLite Database│

&#x20;            │  SQL Generator│   │     Schema     │

&#x20;            └───────┬───────┘   └───────┬────────┘

&#x20;                    │                   │

&#x20;                    └─────────┬─────────┘

&#x20;                              ▼

&#x20;                   ┌──────────────────────┐

&#x20;                   │   SQL Safety Check   │

&#x20;                   │  SELECT queries only │

&#x20;                   └──────────┬───────────┘

&#x20;                              │

&#x20;                              ▼

&#x20;                   ┌──────────────────────┐

&#x20;                   │    Query Results     │

&#x20;                   └──────────┬───────────┘

&#x20;                              │

&#x20;                              ▼

&#x20;                   ┌──────────────────────┐

&#x20;                   │   React Frontend     │

&#x20;                   │  Results Table       │

&#x20;                   └──────────────────────┘

```



\---



\## 👩‍💻 How the Project Works



The application follows these steps:



\### 1. User enters a question



The user enters a natural-language question in the React frontend.



Example:



```text

Show me all students older than 20

```



\### 2. Frontend sends the question



React sends the question to the FastAPI backend through:



```text

POST /ask

```



\### 3. Backend reads the database schema



The backend inspects the SQLite database and identifies the available tables and columns.



The current database contains:



\* `students`

\* `departments`

\* `teachers`

\* `courses`

\* `enrollments`



\### 4. Gemini generates SQL



The database schema and user question are sent to Google Gemini.



Gemini is instructed to generate a valid SQLite `SELECT` query.



Example:



```sql

SELECT \* FROM students WHERE age > 20;

```



\### 5. SQL safety validation



Before execution, the generated SQL is checked.



The application only allows `SELECT` queries and rejects potentially dangerous operations such as:



```text

INSERT

UPDATE

DELETE

DROP

ALTER

CREATE

REPLACE

TRUNCATE

ATTACH

DETACH

PRAGMA

```



\### 6. SQL is executed



The validated query is executed against the SQLite database.



\### 7. Results are displayed



The backend returns the generated SQL and query results to the React frontend.



The frontend displays the results in a table.



\---



\## 🗄️ Database



The project uses SQLite with the following relational structure:



```text

departments

&#x20;    │

&#x20;    ├──────────────┐

&#x20;    ▼              ▼

students         teachers

&#x20;    │              │

&#x20;    │              ▼

&#x20;    │           courses

&#x20;    │              │

&#x20;    └──────┐       │

&#x20;           ▼       ▼

&#x20;        enrollments

```



\### Tables



| Table         | Description                    |

| ------------- | ------------------------------ |

| `students`    | Stores student information     |

| `departments` | Stores department information  |

| `teachers`    | Stores teacher information     |

| `courses`     | Stores course information      |

| `enrollments` | Connects students with courses |



The database initialization script generates sample data including students, teachers, departments, courses, and enrollments.



\---



\## 💡 Example Questions



Users can ask questions such as:



```text

Show me all students

```



```text

Show me students older than 20

```



```text

List all departments

```



```text

Show all teachers

```



```text

List all courses

```



```text

Show the courses taught by each teacher

```



```text

Show students and their departments

```



```text

How many students are there?

```



```text

Show students enrolled in courses

```



\---



\## 📁 Project Structure



```text

text-to-sql-ai/

│

├── backend/

│   ├── app/

│   │   └── main.py

│   │

│   ├── database.py

│   ├── .env.example

│   └── .gitignore

│

├── frontend/

│   ├── public/

│   ├── src/

│   │   ├── App.tsx

│   │   ├── App.css

│   │   ├── index.css

│   │   └── main.tsx

│   │

│   ├── package.json

│   └── vite.config.ts

│

└── README.md

```



\---



\## ⚙️ Installation



\### 1. Clone the repository



```bash

git clone https://github.com/MINZASUNEER/ai-text-to-sql-assistant.git

```



Move into the project:



```bash

cd ai-text-to-sql-assistant

```



\---



\## 🐍 Backend Setup



Move into the backend directory:



```bash

cd backend

```



Create a Python virtual environment:



```bash

python -m venv venv

```



Activate it on Windows:



```powershell

.\\venv\\Scripts\\Activate.ps1

```



Install the required packages:



```bash

pip install fastapi uvicorn python-dotenv google-genai pydantic

```



\---



\## 🔑 Environment Variables



Create a file named:



```text

backend/.env

```



Add your Google Gemini API key:



```text

GEMINI\_API\_KEY=your\_gemini\_api\_key\_here

```



\*\*Never commit your real API key to GitHub.\*\*



The `.env` file is excluded through `.gitignore`.



\---



\## 🗄️ Initialize the Database



From the `backend` directory, run:



```bash

python database.py

```



This creates the SQLite database and populates it with sample data.



\---



\## ▶️ Run the Backend



From the `backend` directory:



```bash

uvicorn app.main:app --reload

```



The backend will run at:



```text

http://127.0.0.1:8000

```



\### Swagger API Documentation



Open:



```text

http://127.0.0.1:8000/docs

```



\---



\## ⚛️ Frontend Setup



Open a second terminal.



Move into the frontend:



```bash

cd frontend

```



Install dependencies:



```bash

npm install

```



Start the development server:



```bash

npm run dev

```



The frontend will normally be available at:



```text

http://localhost:5173

```



\---



\## 🔄 API



\### `GET /`



Checks whether the backend is running.



Example response:



```json

{

&#x20; "message": "AI Text-to-SQL Assistant is running!"

}

```



\### `POST /ask`



Converts a natural-language question into SQL and executes the query.



Request:



```json

{

&#x20; "question": "Show me all students"

}

```



Response:



```json

{

&#x20; "question": "Show me all students",

&#x20; "sql": "SELECT \* FROM students;",

&#x20; "results": \[],

&#x20; "error": null

}

```



\---



\## 📸 Screenshots



Screenshots of the application will be added here.



\### Main Interface



\*Add application screenshot here.\*



\### Generated SQL



\*Add screenshot showing the AI-generated SQL here.\*



\### Query Results



\*Add screenshot showing the database results here.\*



\### Swagger API



\*Add screenshot of the FastAPI Swagger documentation here.\*



\---



\## 🔐 Security



The project includes basic SQL safety controls.



The AI is instructed to generate only `SELECT` queries.



Before execution, generated SQL is checked against a list of potentially dangerous SQL commands.



API credentials are stored using environment variables rather than hard-coded into the source code.



\---



\## 🚀 Future Improvements



Planned improvements include:



\* 🌐 Production deployment

\* 🔑 User authentication

\* 🗃️ Support for additional database systems

\* 📈 Data visualization and charts

\* 🧠 Improved SQL generation accuracy

\* 💬 Query history

\* 📋 SQL copy-to-clipboard functionality

\* 🌓 Dark mode

\* ⚡ Streaming AI responses

\* 🛡️ More advanced SQL validation

\* 📊 Export query results



\---



\## 🎯 Project Goal



The goal of this project is to make databases easier to interact with by allowing users to communicate with them using natural language instead of requiring SQL knowledge.



It demonstrates the integration of:



\*\*Generative AI + Natural Language Processing + REST APIs + Databases + Modern Web Development\*\*



\---



\## 👩‍💻 Author



\*\*Fathima Minza Suneer\*\*



Computer Science Engineering Student



GitHub: \[MINZASUNEER](https://github.com/MINZASUNEER)



\---



\## ⭐ If you find this project useful



Feel free to explore the repository, try the application, and provide feedback.



