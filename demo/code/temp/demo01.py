import vertexai
from vertexai.language_models import TextGenerationModel

vertexai.init(project="hy-ai-demo", location="us-central1")
parameters = {
    "max_output_tokens": 1024,
    "temperature": 0.2,
    "top_p": 0.8,
    "top_k": 40
}
model = TextGenerationModel.from_pretrained("text-bison-32k@002")
responses = model.predict_streaming(
    """请描述如何学习英语""",
    **parameters
)
results = []
for response in responses:
  print(response)
  results.append(str(response))