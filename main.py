from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import json
import os

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load credentials from ENV
scope = ["https://www.googleapis.com/auth/spreadsheets"]

creds_dict = json.loads(os.getenv("GOOGLE_CREDENTIALS"))
creds = Credentials.from_service_account_info(creds_dict, scopes=scope)

client = gspread.authorize(creds)
sheet = client.open("Analyt Waitlist").sheet1


class Email(BaseModel):
    email: str


@app.get("/")
def root():
    return {"status": "API Running"}


@app.post("/subscribe")
def subscribe(data: Email):
    sheet.append_row([
        data.email,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ])
    return {"message": "Saved to Sheets"}