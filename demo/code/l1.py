import vertexai
from vertexai.preview.language_models import TextGenerationModel
from google.cloud import storage

def blob_read(bucket_name, blob_name):
    """Write and read a blob from GCS using file-like IO"""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"

    # The ID of your new GCS object
    # blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
 

    # Mode can be specified as wb/rb for bytes mode.
    # See: https://docs.python.org/3/library/io.html


    with blob.open("r") as f:
        #print(f.read())
        text = "Please translate following text into Chinese: "+f.read()
        #print (text)
        vertexai.init(project="hy-ai-demo", location="us-central1")
        parameters = {
            "max_output_tokens": 8192,
            "temperature": 0.2,
            "top_p": 0.8,
            "top_k": 40
            }
        model = TextGenerationModel.from_pretrained("text-bison-32k")
        response = model.predict(
            text,
            **parameters
        )
        print(f"Response from Model: {response.text}")
    
    

blob_read("hy-tran-001", "DE-155073-A.txt")
