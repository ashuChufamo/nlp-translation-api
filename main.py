from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI
import pickle
import os
import torch

app = FastAPI()

# Load your model
model_path = os.path.join(os.path.dirname(__file__), "tmodel_epoch-100.pkl")
with open(model_path, "rb") as f:
    model = pickle.load(f)

# Ensure the model is in evaluation mode
model.eval()

class MsgPayload(BaseModel):
    msg_id: Optional[int]
    msg_name: str

class TranslationRequest(BaseModel):
    text: str

messages_list: dict[int, MsgPayload] = {}

@app.post("/translate/")
def translate(request: TranslationRequest):
    # Use your model to translate text
    translated_text = model.translate(request.text)
    return {"translated_text": translated_text}

@app.get("/")
def read_root():
    return {"message": "Welcome to the translation API"}

# About page route
@app.get("/about")
def about() -> dict[str, str]:
    return {"message": "This is the about page."}

# Route to add a message
@app.post("/messages/{msg_name}/")
def add_msg(msg_name: str) -> dict[str, MsgPayload]:
    # Generate an ID for the item based on the highest ID in the messages_list
    msg_id = max(messages_list.keys()) + 1 if messages_list else 0
    messages_list[msg_id] = MsgPayload(msg_id=msg_id, msg_name=msg_name)

    return {"message": messages_list[msg_id]}

# Route to list all messages
@app.get("/messages")
def message_items() -> dict[str, dict[int, MsgPayload]]:
    return {"messages:": messages_list}
