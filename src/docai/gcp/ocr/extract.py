from google.cloud import documentai as docai


def _extract_invoice_data(invoice):
    def print_entity(entity: docai.Document.Entity) -> None:
        # Fields detected. For a full list of fields for each processor see
        # the processor documentation:
        # https://cloud.google.com/document-ai/docs/processors-list
        key = entity.type_
        text_value = entity.text_anchor.content
        confidence = entity.confidence
        normalized_value = entity.normalized_value.text
        print(f"    * {repr(key)}: {repr(text_value)}({confidence:.1%} confident)")

        if normalized_value:
            print(f"    * Normalized Value: {repr(normalized_value)}")

    for entity in invoice.entities:
            print_entity(entity)
            # Print Nested Entities (if any)
            for prop in entity.properties:
                print_entity(prop)


class OCRExtractionHandler:
    def __init__(self, parser):
        self.parser = parser

    def perform_extraction(self, document):
        if self.parser == "invoice":
            return _extract_invoice_data(document)
        else:
            raise ValueError("Invalid extraction method")
