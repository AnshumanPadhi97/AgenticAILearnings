from types import SimpleNamespace
from sqlalchemy import create_engine, text
from llama_index.core import SQLDatabase
from llama_index.core.query_engine import NLSQLTableQueryEngine
from ollama import Client
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import re

DATABASE_URL = "postgresql://postgres:password@localhost:5432/postgres"
LOCAL_EMBEDDING_MODEL_PATH = "./granite-embedding-125m-english"
OLLAMA_API_HOST = "http://localhost:11434"
SCHEMA_NAME = "ecommerce"
TABLES = ["products", "customers", "orders", "order_items"]

USER_QUESTION = "which categories are most sold and least sold. give me a table of comparison"

SYSTEM_PROMPT = (
    "You are an expert SQL assistant. "
    "When writing SQL queries, always fully qualify all table names with their schema names, e.g., ecommerce.customers. "
    "Answer concisely using SQL where possible."
)

# Initialize engine and SQLDatabase
engine = create_engine(DATABASE_URL)

sql_database = SQLDatabase(
    engine,
    schema=SCHEMA_NAME,
    include_tables=TABLES
)


class OllamaLLM:
    @property
    def metadata(self):
        return SimpleNamespace(context_window=2048, num_output=256)

    def __init__(self, model="gemma3:4b", system_prompt=None, host=OLLAMA_API_HOST):
        self.model = model
        self.system_prompt = system_prompt
        self.client = Client(host=host)

    def __call__(self, prompt, **kwargs):
        prompt_str = str(prompt)
        messages = []
        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})
        messages.append({"role": "user", "content": prompt_str})
        response = self.client.chat(
            model=self.model,
            messages=messages,
        )
        return response['message']['content']

    def predict(self, prompt, **kwargs):
        return self.__call__(prompt, **kwargs)


# Initialize models
llm = OllamaLLM(model="gemma3:4b", system_prompt=SYSTEM_PROMPT, host=OLLAMA_API_HOST)
embed_model = HuggingFaceEmbedding(model_name=LOCAL_EMBEDDING_MODEL_PATH)

query_engine = NLSQLTableQueryEngine(
    sql_database=sql_database,
    tables=TABLES,
    llm=llm,
    embed_model=embed_model,
)

schema_description = ""
for table_name in TABLES:
    table_info = sql_database.get_single_table_info(table_name)
    schema_description += f"Table {table_name}:\n{table_info}\n\n"

full_prompt = (
    f"Database schema:\n{schema_description}\n"
    f"Based on this schema, write a SQL query for the following request:\n"
    f"{USER_QUESTION}\n"
    f"Please fully qualify all table names with the schema name, e.g., {SCHEMA_NAME}.customers."
)

llm_response = llm(full_prompt)

sql_pattern = re.compile(r"(SELECT[\s\S]*?;)", re.IGNORECASE)
match = sql_pattern.search(llm_response)

def add_schema_prefix(sql, tables, schema=SCHEMA_NAME):
    for tbl in tables:
        pattern = re.compile(rf"(?<!\b{re.escape(schema)}\.)\b{tbl}\b", re.IGNORECASE)
        sql = pattern.sub(f"{schema}.{tbl}", sql)
    return sql

if match:
    sql_query = match.group(1)
    sql_query = add_schema_prefix(sql_query, TABLES, SCHEMA_NAME)
    try:
        with engine.connect() as conn:
            result = conn.execute(text(sql_query))
            rows = result.fetchall()
            columns = result.keys()
            if rows:
                print("\t".join(columns))
                for row in rows:
                    print("\t".join(str(item) for item in row))
    except Exception as e:
        print(f"Error executing SQL query: {e}")
else:
    pass
