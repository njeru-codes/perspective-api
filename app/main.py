from fastapi import FastAPI
from pydantic import BaseModel
import json,os
from googleapiclient import discovery
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.environ.get('GOOGLE_API_KEY')

app = FastAPI()

class Text(BaseModel):
    text: str




def is_toxic(text):
    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=API_KEY,
        discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
        static_discovery=False,
    )

    analyze_request = {
        'comment': {'text': str(text)},
        'requestedAttributes': {'TOXICITY': {}}
    }

    response = client.comments().analyze(body=analyze_request).execute()
    toxicity = response['attributeScores']['TOXICITY']['summaryScore']['value']
    return toxicity > 0.5




@app.post('/')
async def profanity_check(text: Text):
    return  {
        "profanity":is_toxic(text.text)
    }