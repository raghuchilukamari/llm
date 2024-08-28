from qa_base import QABotBase
from typing import List
from src.utils.filesplitters import FileSplitter
from langchain_openai.embeddings import OpenAIEmbeddings
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI


class QABot(QABotBase):

    def read_document(self, file: str) -> List[str]:
        splitter = FileSplitter(file)
        return splitter.pdffilesplitter(splitter_type='recursive')

    def embed(self, documents: List[str]) -> List[str]:
        embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
        docs = [doc.page_content for doc in documents]
        document_embeddings = embeddings.embed_documents(docs)

        return document_embeddings

    def retrieve(self, query: str, doc_embeddings, documents) -> str:
        embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
        query_embedding = embeddings.embed_query(query)
        similarity_scores = cosine_similarity([query_embedding], doc_embeddings)[0]
        most_similar_index = np.argmax(similarity_scores)
        most_similar_document = documents[most_similar_index]
        chunks_formatted = "\n\n".join(most_similar_document.page_content)

        return chunks_formatted

    def generate_answer(self, query: str, retrieved_chunks) -> str:
        prompt_template = """You are an exceptional support chatbot that gently answer questions.
            You know the following context information.
            {document}
            Using only provide context answer the following question.. Do not invent anything.
            Question: {query}
            Answer:"""

        prompt = PromptTemplate(
            input_variables=["document", "query"],
            template=prompt_template,
        )
        prompt_formatted = prompt.format(document=retrieved_chunks, query=query)
        llm = OpenAI(model="gpt-3.5-turbo-instruct", temperature=0)
        answer = llm.invoke(prompt_formatted)

        return  answer

    def run_qa_process(self, document_path: str, query: str = None) -> str:

        docs = self.read_document(document_path)
        doc_embeddings = self.embed(docs)
        retrieved_chunks = self.retrieve(query,doc_embeddings, docs)
        answer = self.generate_answer(query, retrieved_chunks)
        return answer

    def prepare_prompt(self, question: str) -> str:
        return f"Question: {question}\n"


# Example usage:
if __name__ == "__main__":

    bot = QABot()
    document_path = "/Users/rc/workspaces/llm/data/AutoPolicy.pdf"
    query = "Cancellation Policy"
    answer = bot.run_qa_process(document_path, query)
    print(answer)

    # for doc in answer:
    #     print(doc)
    # print("Answer:", answer)

    # print(type(bot.read_document('/Users/rc/workspaces/llm/data/Winnie_the_Pooh_3_Pages.pdf')))
