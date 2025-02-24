from sqlalchemy import create_engine, inspect
from llama_index.core import SQLDatabase

class VectorDBRetriever:

    @classmethod
    def getDb(cls):
        connection_str = f"postgresql+psycopg://postgres@localhost:5432/postgres"
        engine = create_engine(connection_str)
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        db = SQLDatabase(engine, include_tables=tables)
        return db, tables