import sqlite3
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


# --------------------------------------------------
# Paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "database.db"
CHROMA_PATH = BASE_DIR / "chroma_db"


# --------------------------------------------------
# Initialize Embedding Model + ChromaDB
# --------------------------------------------------

model = SentenceTransformer("all-MiniLM-L6-v2")

chroma_client = chromadb.PersistentClient(
    path=str(CHROMA_PATH)
)

collection = chroma_client.get_or_create_collection(
    name="schema_collection"
)


# --------------------------------------------------
# Index SQLite Schema into ChromaDB
# --------------------------------------------------

def index_schema():
    """Read SQLite schema, relationships and descriptions into ChromaDB."""

    connection = sqlite3.connect(str(DATABASE_PATH))

    try:
        cursor = connection.cursor()

        # Get all user tables
        cursor.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            AND name NOT LIKE 'sqlite_%'
        """)

        tables = [row[0] for row in cursor.fetchall()]

        # Remove old schema documents so the index stays fresh
        existing = collection.get()

        if existing and existing.get("ids"):
            collection.delete(ids=existing["ids"])

        for table_name in tables:

            # Get columns
            cursor.execute(f'PRAGMA table_info("{table_name}")')
            column_info = cursor.fetchall()

            columns = [column[1] for column in column_info]

            # Get foreign keys
            cursor.execute(f'PRAGMA foreign_key_list("{table_name}")')
            foreign_keys = cursor.fetchall()

            relationships = []

            for fk in foreign_keys:
                referenced_table = fk[2]
                from_column = fk[3]
                referenced_column = fk[4]

                relationships.append(
                    f"{table_name}.{from_column} -> "
                    f"{referenced_table}.{referenced_column}"
                )

            if relationships:
                relationship_text = (
                    "Relationships: "
                    + "; ".join(relationships)
                )
            else:
                relationship_text = "Relationships: none"

            schema_text = (
                f"Table: {table_name}\n"
                f"Columns: {', '.join(columns)}\n"
                f"{relationship_text}"
            )

            embedding = model.encode(schema_text).tolist()

            collection.upsert(
                ids=[table_name],
                documents=[schema_text],
                embeddings=[embedding]
            )

        print(
            f"Database schema successfully indexed into ChromaDB. "
            f"Tables indexed: {len(tables)}"
        )

    finally:
        connection.close()


# --------------------------------------------------
# Retrieve Relevant Schema
# --------------------------------------------------

def get_relevant_schema(query: str, top_k: int = 5) -> str:
    """Retrieve relevant tables and their relationships."""

    count = collection.count()

    if count == 0:
        index_schema()
        count = collection.count()

    n_results = min(top_k, count)

    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )

    documents = results.get("documents", [[]])[0]

    return "\n\n".join(documents)