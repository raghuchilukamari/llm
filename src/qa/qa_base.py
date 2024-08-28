from abc import ABC, abstractmethod
from typing import List


class QABotBase(ABC):

    @abstractmethod
    def read_document(self, document: str) -> List[str]:
        pass

    @abstractmethod
    def embed(self, paragraphs: List[str]) -> List[str]:
        pass

    @abstractmethod
    def retrieve(self, paragraphs: List[str]) -> List[str]:
        pass

    @abstractmethod
    def generate_answer(self, prompt: str) -> str:
        pass


