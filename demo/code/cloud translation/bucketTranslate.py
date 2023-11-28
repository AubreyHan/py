from google.cloud import translate
from google.cloud import storage

def batch_translate_text(
    input_uri: str = "gs://YOUR_BUCKET_ID/path/to/your/file.txt",
    output_uri: str = "gs://YOUR_BUCKET_ID/path/to/save/results/",
    project_id: str = "YOUR_PROJECT_ID",
    lang_code: str = "blob code",
    timeout: int = 600,
) -> translate.TranslateTextResponse:
    """Translates a batch of texts on GCS and stores the result in a GCS location.

    Args:
        input_uri: The input URI of the texts to be translated.
        output_uri: The output URI of the translated texts.
        project_id: The ID of the project that owns the destination bucket.
        timeout: The timeout for this batch translation operation.

    Returns:
        The translated texts.
    """

    client = translate.TranslationServiceClient()

    location = "us-central1"
    # Supported file types: https://cloud.google.com/translate/docs/supported-formats
    gcs_source = {"input_uri": input_uri}

    input_configs_element = {
        "gcs_source": gcs_source,
        "mime_type": "text/plain",  # Can be "text/plain" or "text/html".
    }
    gcs_destination = {"output_uri_prefix": output_uri}
    output_config = {"gcs_destination": gcs_destination}
    parent = f"projects/{project_id}/locations/{location}"

    print (parent)

    # Supported language codes: https://cloud.google.com/translate/docs/languages
    operation = client.batch_translate_text(
        request={
            "parent": parent,
            "source_language_code": lang_code,
            "target_language_codes": ["zh"],
            "input_configs": [input_configs_element],
            "output_config": output_config,
        }
    )

    print("Waiting for operation to complete...")
    response = operation.result(timeout)

    print(f"Total Characters: {response.total_characters}")
    print(f"Translated Characters: {response.translated_characters}")

    return response


def move_blob(bucket_name, blob_name, destination_bucket_name, destination_blob_name,):
    """Moves a blob from one bucket to another with a new name."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The ID of your GCS object
    # blob_name = "your-object-name"
    # The ID of the bucket to move the object to
    # destination_bucket_name = "destination-bucket-name"
    # The ID of your new GCS object (optional)
    # destination_blob_name = "destination-object-name"

    storage_client = storage.Client()

    source_bucket = storage_client.bucket(bucket_name)
    source_blob = source_bucket.blob(blob_name)
    destination_bucket = storage_client.bucket(destination_bucket_name)

    # Optional: set a generation-match precondition to avoid potential race conditions
    # and data corruptions. The request is aborted if the object's
    # generation number does not match your precondition. For a destination
    # object that does not yet exist, set the if_generation_match precondition to 0.
    # If the destination object already exists in your bucket, set instead a
    # generation-match precondition using its generation number.
    # There is also an `if_source_generation_match` parameter, which is not used in this example.
    # destination_generation_match_precondition = 0

    blob_copy = source_bucket.copy_blob(
        source_blob, destination_bucket, destination_blob_name,
    )
    source_bucket.delete_blob(blob_name)

    print(
        "Blob {} in bucket {} moved to blob {} in bucket {}.".format(
            source_blob.name,
            source_bucket.name,
            blob_copy.name,
            destination_bucket.name,
        )
    )




















def bucket_translate(source_bucket_name, target_bucket_name):
    """Lists all the blobs in the bucket."""
    # bucket_name = "your-bucket-name"

    storage_client = storage.Client()

    # Note: Client.list_blobs requires at least package version 1.17.0.
    blobs = storage_client.list_blobs(source_bucket_name)

    # Note: The call returns a response only when the iterator is consumed.
    for blob in blobs:
        blob_name="gs://"+source_bucket_name+"/"+blob.name
        blob_code=blob.name[0:2]
        blob_code_dic={"DE":"de", "JP":"ja", "KR":"ko", "US":"en"}
        print (blob_code_dic[blob_code])
        batch_translate_text(blob_name, "gs://hy-temp-001/", "hy-ai-demo", blob_code_dic[blob_code])
        
        translate_blobs = storage_client.list_blobs("hy-temp-001")
        for blob in translate_blobs:
            move_blob("hy-temp-001", blob.name, "hy-tran-out", blob.name)
                             


        
    
   

bucket_translate("hy-tran-001", "hy-tran-out")