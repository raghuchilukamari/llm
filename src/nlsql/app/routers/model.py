from fastapi import APIRouter
from ..schema.requests import SingleRequestModel
from llama_index.llms.openai import OpenAI
from ..services.init_vectordb import VectorDBRetriever
from llama_index.core.query_engine import NLSQLTableQueryEngine
from ..services.prompt import PromptService, Prompts
from llama_index.core.indices.struct_store.sql_query import (
    SQLTableRetrieverQueryEngine,
)
from llama_index.core.objects import (
    SQLTableNodeMapping,
    ObjectIndex,
    SQLTableSchema,
)
from llama_index.core import VectorStoreIndex



def get_router(client):
    router = APIRouter()

    @router.post("/generate/")
    async def generate_sql(request: SingleRequestModel):
        try:
            query = request.input

            llm = OpenAI(model='gpt-3.5-turbo')
            sql_database, tables = VectorDBRetriever.getDb()
            prompt = PromptService.get_prompt()

            table_node_mapping = SQLTableNodeMapping(sql_database)
            table_schema_objs = [(SQLTableSchema(table_name=table)) for table in tables]

            obj_index = ObjectIndex.from_objects(
                table_schema_objs,
                table_node_mapping,
                VectorStoreIndex,
            )

            query_engine = SQLTableRetrieverQueryEngine(
                    sql_database, obj_index.as_retriever(similarity_top_k=1), llm=llm, text_to_sql_prompt=prompt
                )

            response = query_engine.query(query)

            return response

        except Exception as e:
            print(e)

    return router