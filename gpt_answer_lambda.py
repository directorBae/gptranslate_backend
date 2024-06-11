from http import HTTPStatus
from dotenv import load_dotenv
import os
from openai import OpenAI

SYSTEM_PROMPT = """You are a helpful translator. You should translate the following text to the requested language.
And you shouldn't provide any other descriptions or information about the text. You MUST give ONLY translated text."""
PROMPT = "Translate the following text to "

def fetchAPI(api_key, lang, source_text):
    try:
        client = OpenAI()
        prompt = PROMPT + lang + ": " + source_text

        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ]
        )
        
        return {"status": HTTPStatus.OK, "data": completion.choices[0].message.content}
    
    except Exception as e:
        return {"status": HTTPStatus.INTERNAL_SERVER_ERROR, "message": str(e)}

if __name__ == "__main__":
    # Load environment variables
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    val = fetchAPI(api_key, "Spanish", "Hello, how are you?")

    print(val)