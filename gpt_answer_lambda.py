from openai import OpenAI
from http import HTTPStatus
import json

import os
from dotenv import load_dotenv

def lambda_handler(event, context):
    SYSTEM_PROMPT = """You are a helpful translator. You should translate the following text to the requested language.
    And you shouldn't provide any other descriptions or information about the text. You MUST give ONLY translated text."""
    PROMPT = "Translate the following text to "
    
    eventbody = json.loads(event["body"])
    
    api_key = eventbody["api_key"]
    lang = eventbody["lang"]
    source_text = eventbody["source_text"]

    try:
        client = OpenAI(api_key = api_key)
        prompt = PROMPT + lang + ": " + source_text
    
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ]
        )
        
        return {"statusCode": HTTPStatus.OK, "body": completion.choices[0].message.content}
    
    except Exception as e:
        return {"statusCode": HTTPStatus.INTERNAL_SERVER_ERROR, "message": str(e)}

if __name__ == "__main__":
    # Load environment variables
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    event = {
        "body": {
            "api_key": api_key,
            "lang": "Spanish",
            "source_text": "Hello, how are you?"
        }
    }

    val = lambda_handler(event, None)

    print(val)