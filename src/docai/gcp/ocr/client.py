from utils import *
from extract import OCRExtractionHandler

from google.cloud import documentai as docai


class OCRClient:
    def __init__(self, parser_type, api_loc):
        self._parser = parser_type
        self.api_loc = api_loc
        self.prj_id = os.getenv('PROJECT_ID')
        self.doc_ocr_disp_nm = os.getenv('DOC_OCR_NM')
        self.inv_ocr_disp_nm = os.getenv('INV_OCR_NM')
        self._update_handler()

    @property
    def parser(self):
        return self._parser

    @parser.setter
    def parser(self, value):
        self._parser = value
        self._update_handler()

    def _update_handler(self):
        self.handler = OCRExtractionHandler(self.parser)
        self.processor = DocumentAIProcessor(self.api_loc, self.prj_id)

    def parse(self, file_path):
        if self.parser == "document":
            return self._ocr(file_path, self.doc_ocr_disp_nm)
        elif self.parser == "invoice":
            return self._ocr(file_path, self.inv_ocr_disp_nm)
        else:
            raise ValueError("Invalid extraction method")

    def _ocr(self, file_path: str, ocr_type: str, ) -> docai.Document:

        client = self.processor.client
        processor = self.processor.get_processor(ocr_type)

        with open(file_path, 'rb') as file:
            document_context = file.read()

        document = docai.RawDocument(content=document_context, mime_type='application/pdf')
        request = docai.ProcessRequest(raw_document=document, name=processor.name)

        response = client.process_document(request=request)

        return response.document


if __name__ == "__main__":
    doc_path = '/data/Winnie_the_Pooh_3_Pages.pdf'
    inv_path = '/data/inv.pdf'

    ocr = OCRClient("document",'eu')
    res = ocr.parse(doc_path)

    print(type(res))
    print(res.text)

    # ocr = OCRClient("invoice", 'us')
    # inv = ocr.parse(inv_path)
    # print(ocr.handler.parser)
    # ocr.handler.perform_extraction(inv)
