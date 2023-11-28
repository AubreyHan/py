import vertexai
from vertexai.preview.language_models import TextGenerationModel
from google.cloud import storage
import time

import vertexai
from vertexai.preview.language_models import TextGenerationModel

def gcs_ai_translation(source_bucket, target_bucket):
    storage_client = storage.Client()
    blobs = storage_client.list_blobs(source_bucket)

    for blob in blobs:
        print (blob)
        with blob.open("r") as f:
            text="Please translate following Japanese text into Chinese: "+f.read()
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
            #print(f"Response from Model: {response.text}")

            bucket = storage_client.bucket(target_bucket)
            target_blob = bucket.blob(blob.name)
            with target_blob.open("w") as w:
                    w.write(response.text)
            print (target_blob)
            #time.sleep(60)
            






gcs_ai_translation("hy-tran-001", "hy-tran-out")