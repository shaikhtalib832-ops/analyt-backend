# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import json
from datetime import datetime

import gspread

app = FastAPI()

# ✅ Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Request model
class EmailRequest(BaseModel):
    email: str


# ✅ Connect to Google Sheets safely
def get_sheet():
    try:
        creds_json = os.getenv("GOOGLE_CREDENTIALS")

        if not creds_json:
            print("❌ GOOGLE_CREDENTIALS not found")
            return None

        creds_dict = json.loads(creds_json)

        gc = gspread.service_account_from_dict(creds_dict)

        sheet = gc.open("Analyt Waitlist").sheet1

        return sheet

    except Exception as e:
        print("❌ SHEETS CONNECTION ERROR:", e)
        return None


# ✅ Root (for testing)
@app.get("/")
def home():
    return {"status": "API Running"}


# ✅ Subscribe endpoint
@app.post("/subscribe")
def subscribe(data: EmailRequest):
    email = data.email

    sheet = get_sheet()

    if sheet is None:
        return {"error": "Google Sheets not connected"}

    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        sheet.append_row([email, timestamp])

        return {"message": "Saved successfully"}

    except Exception as e:
        print("❌ ERROR SAVING:", e)
        return {"error": "Failed to save email"}