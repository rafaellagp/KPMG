import os
import openai
from algoliasearch.search_client import SearchClient
from dotenv import load_dotenv

load_dotenv(".env")

app_id = os.getenv("APP_ID")
api_key = os.getenv("API_ADMIN_KEY")
db_name = os.getenv("DB_NAME")

client = SearchClient.create(app_id=app_id, api_key=api_key)
index = client.init_index(db_name)
results = index.search("",{
'filters': 'inProgress=1'
})

object_dict = results["hits"][0]
object_id = object_dict["objectID"]
object_full_text = object_dict["full_text"]

chatGPT_api_key = os.getenv("API_KEY_OPENAI")
# Set the API key
openai.api_key = chatGPT_api_key

def get_summary_long_file():

    text_to_summarize = object_full_text
    # Set the model to use
    model_engine = "text-davinci-003"

    # Set the maximum context length (in tokens) allowed by the model
    max_context_length = 2048

    # Split the text into chunks of the maximum allowed context length
    text = text_to_summarize
    text_chunks = [text[i:i+max_context_length] for i in range(0, len(text), max_context_length)]

    # Send each chunk of text to the model and store the results
    results = []
    for chunk in text_chunks:
        response = openai.Completion.create(
            engine=model_engine,
            prompt=chunk,
            max_tokens=1024,
            temperature=0.5,
        )
        results.append(response["choices"][0]["text"])

    # Concatenate the results into a single string
    result_text = "".join(results)

    # Prompt
    prompt = f"Résume ce document en français: {result_text}"

    # Use the model to generate a summary of the text
    summary_response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        temperature=0.5,
    )

    summary = summary_response["choices"][0]["text"]
    index.partial_update_object({"objectID":object_id, "summary":summary})
    print("Summary saved to database")

get_summary_long_file()