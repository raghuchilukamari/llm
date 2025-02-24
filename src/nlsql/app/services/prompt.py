from llama_index.core import PromptTemplate

class Prompts:
    NLSQL_TEMPLATE = '''
                    you are a helpful assistant that converts the input in natural language to sql query. 
                    Generate query will be used to query a database
                    
                    Rules:
                    - if query cannot be generated, say 'unable to find relevant data to generate sql query for the input' 
                    
                    only use tables listed below:
                    {schema}
                    
                    query: {query_str}
                    
                    '''
class PromptService:

    @staticmethod
    def get_prompt():

        prompt = PromptTemplate(Prompts.NLSQL_TEMPLATE)

        return prompt