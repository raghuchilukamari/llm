from langchain.text_splitter import (NLTKTextSplitter, SpacyTextSplitter, TokenTextSplitter,
                                     CharacterTextSplitter, RecursiveCharacterTextSplitter)

from langchain_community.document_loaders import PyPDFLoader, TextLoader, SeleniumURLLoader
from typing import List


class FileSplitter:
    def __init__(self, document_path: str):
        self.document_path = document_path

    def textfilesplitter(self, splitter_type: str = 'token') -> List[str]:
        # with open(self.document_path, encoding='unicode_escape') as f:
        #     file = f.read()

        loader = TextLoader(self.document_path)
        file = loader.load()

        if splitter_type == 'nltk':
            text_splitter = NLTKTextSplitter(chunk_size=500, chunk_overlap=20)
        elif splitter_type == 'spacy':
            text_splitter = SpacyTextSplitter(chunk_size=500, chunk_overlap=20)
        else:  # Default to 'token'
            text_splitter = TokenTextSplitter(chunk_size=500, chunk_overlap=20)

        texts = text_splitter.split_text(file)
        return texts

    def pdffilesplitter(self, splitter_type: str = 'recursive') -> List[str]:
        loader = PyPDFLoader(self.document_path)
        pages = loader.load_and_split()

        if splitter_type == 'char':
            text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
        else:  # Default to 'recursive'
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20, length_function=len)

        texts = text_splitter.split_documents(pages)
        return texts

    def urlloader(self, urls: List[str]) -> List[str]:
        loader = SeleniumURLLoader(urls=urls, browser="chrome")
        data = loader.load()
        return data

# Example usage:
if __name__ == "__main__":
    splitter = FileSplitter("/Users/rc/workspaces/llm/data/Winnie_the_Pooh_3_Pages.pdf")
    text_from_pdf = splitter.pdffilesplitter(splitter_type='char')
    print("Text from PDF:", text_from_pdf)


