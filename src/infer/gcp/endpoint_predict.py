from google.cloud import aiplatform
from google.cloud.aiplatform.gapic.schema import predict
from google.protobuf import json_format
from google.protobuf.struct_pb2 import Value


def predict_text_classification_single_label_endpoint(
    project: str,
    endpoint_id: str,
    content: str,
    location: str = "us-west1",
    api_endpoint: str = "us-west1-aiplatform.googleapis.com",
):
    # The AI Platform services require regional API endpoints.
    client_options = {"api_endpoint": api_endpoint}
    # Initialize client that will be used to create and send requests.
    # This client only needs to be created once, and can be reused for multiple requests.
    client = aiplatform.gapic.PredictionServiceClient(client_options=client_options)
    instance = predict.instance.TextSentimentPredictionInstance(
        content=content,
    ).to_value()
    instances = [instance]
    parameters_dict = {}
    parameters = json_format.ParseDict(parameters_dict, Value())
    endpoint = client.endpoint_path(
        project=project, location=location, endpoint=endpoint_id
    )
    response = client.predict(
        endpoint=endpoint, instances=instances, parameters=parameters
    )
    print("response")
    print(" deployed_model_id:", response.deployed_model_id)

    predictions = response.predictions
    for prediction in predictions:
        print(" prediction:", dict(prediction))



content = """
What is the sentiment of this news? Please choose an answer from {negative/neutral/positive}. $YMI http:\/\/stks.co\/Xyf Long setup. Closed above the 20MA. MACD cross. November catalyst.
"""

predict_text_classification_single_label_endpoint(project='471026294913',
                        endpoint_id='7052909695345885184',
                        content=content)
