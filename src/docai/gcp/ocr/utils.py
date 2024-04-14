import os
from dotenv import load_dotenv
from typing import Iterator, MutableSequence, Optional, Sequence, Tuple
from google.cloud import documentai as docai

load_dotenv()


class DocumentAIProcessor:
    def __init__(self, api_loc: str, project_id: str):
        self.api_loc = api_loc
        self.project_id = project_id
        self.client, self.parent = self._get_client_parent()
        self.processor_types = self._fetch_processor_types()
        self.processor_list = self._list_processors()

    def _get_client(self) -> docai.DocumentProcessorServiceClient:
        client_options = {'api_endpoint': f'{self.api_loc}-documentai.googleapis.com'}
        return docai.DocumentProcessorServiceClient(client_options=client_options)

    def _get_parent(self, client: docai.DocumentProcessorServiceClient) -> str:
        return client.common_location_path(self.project_id, self.api_loc)

    def _get_client_parent(self) -> Tuple[docai.DocumentProcessorServiceClient, str]:
        client = self._get_client()
        parent = self._get_parent(client)
        return client, parent

    def _fetch_processor_types(self) -> MutableSequence[docai.ProcessorType]:
        response = self.client.fetch_processor_types(parent=self.parent)
        return response.processor_types

    def _list_processors(self) -> MutableSequence[docai.Processor]:
        client, parent = self._get_client_parent()
        response = client.list_processors(parent=parent)
        return list(response.processors)

    def get_processor(self, display_name: str,
                      processors: Optional[Sequence[docai.Processor]] = None,
                      ) -> Optional[docai.Processor]:

        if processors is None:
            processors = self._list_processors()
            for processor in processors:
                if processor.display_name == display_name:
                    return processor

        return None

    def disable_processor(self, processor: docai.Processor):
        self.client.disable_processor(processor)
