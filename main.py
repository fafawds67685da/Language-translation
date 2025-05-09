from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Indian Language Translator API")

class TextIn(BaseModel):
    text: str

# Supported language to model map
language_models = {
    "hindi": "Helsinki-NLP/opus-mt-en-hi",
    "malayalam": "Helsinki-NLP/opus-mt-en-ml",
    "marathi": "Helsinki-NLP/opus-mt-en-mr",
    "urdu": "Helsinki-NLP/opus-mt-en-ur",
}

# Preload models for faster access
translators = {
    lang: pipeline("translation", model=model)
    for lang, model in language_models.items()
}

@app.get("/")
def read_root():
    return {"message": "Translator API is running"}

@app.post("/translate/{lang}")
async def translate_text_endpoint(lang: str, text_in: TextIn):
    # Check if the requested language is supported
    translator = translators.get(lang)
    if not translator:
        logger.error(f"Model for '{lang}' could not be loaded or is unsupported.")
        raise HTTPException(status_code=400, detail=f"Model for '{lang}' could not be loaded or is unsupported.")
    
    # Handle long text input and truncate if it exceeds the max length (512 tokens)
    input_text = text_in.text
    max_input_length = 512  # Token limit for the models
    
    # Tokenize the input text and check if it's too long
    if len(input_text.split()) > max_input_length:
        logger.info(f"Input text is too long, truncating to {max_input_length} tokens.")
        input_text = ' '.join(input_text.split()[:max_input_length])  # Truncate text

    try:
        # Perform translation
        translated = translator(input_text, max_length=512)
        return {
            "language": lang.capitalize(),
            "translated_text": translated[0]['translation_text']
        }
    except Exception as e:
        # Log the error if translation fails
        logger.error(f"Translation failed for '{lang}' with error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Translation failed for '{lang}'.")
