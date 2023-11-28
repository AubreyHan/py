from google.cloud import translate

def batch_translate_text_with_model(
    input_uri: str = "gs://YOUR_BUCKET_ID/path/to/your/file.txt",
    output_uri: str = "gs://YOUR_BUCKET_ID/path/to/save/results/",
    project_id: str = "YOUR_PROJECT_ID",
    model_id: str = "YOUR_MODEL_ID",
) -> translate.TranslationServiceClient:
    """Batch translate text using Translation model.
    Model can be AutoML or General[built-in] model.

    Args:
        input_uri: The input file to translate.
        output_uri: The output file to save the translation results.
        project_id: The ID of the GCP project that owns the model.
        model_id: The model ID.

    Returns:
        The response from the batch translation API.
    """

    client = translate.TranslationServiceClient()

    # Supported file types: https://cloud.google.com/translate/docs/supported-formats
    gcs_source = {"input_uri": input_uri}
    location = "us-central1"

    input_configs_element = {
        "gcs_source": gcs_source,
        "mime_type": "text/plain",  # Can be "text/plain" or "text/html".
    }
    gcs_destination = {"output_uri_prefix": output_uri}
    output_config = {"gcs_destination": gcs_destination}
    parent = f"projects/{project_id}/locations/{location}"

    model_path = "projects/{}/locations/{}/models/{}".format(
        project_id, location, model_id  # The location of AutoML model.
    )

    # Supported language codes: https://cloud.google.com/translate/docs/languages
    models = {"ja": model_path}  # takes a target lang as key.

    operation = client.batch_translate_text(
        request={
            "parent": parent,
            "source_language_code": "de",
            "target_language_codes": ["zh"],  # Up to 10 language codes here.
            "input_configs": [input_configs_element],
            "output_config": output_config,
           
        }
    )

    print("Waiting for operation to complete...")
    response = operation.result()

    # Display the translation for each input text provided.
    print(f"Total Characters: {response.total_characters}")
    print(f"Translated Characters: {response.translated_characters}")

    return response


batch_translate_text_with_model(["gs://hy-tran-001/DE-155073-A.txt"], "gs://hy-temp-001/", "hy-ai-demo")