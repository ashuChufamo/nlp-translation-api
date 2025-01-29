from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI
import pickle

app = FastAPI()

# Load your model
with open("tmodel_epoch-100.pkl", "rb") as f:
    model = pickle.load(f)

class MsgPayload(BaseModel):
    msg_id: Optional[int]
    msg_name: str

class TranslationRequest(BaseModel):
    text: str

@app.post("/translate/")
def translate(request: TranslationRequest):
    # Use your model to translate text
    translated_text = model.translate(request.text)
    return {"translated_text": translated_text}

@app.get("/")
def read_root():
    return {"message": "Welcome to the translation API"}
