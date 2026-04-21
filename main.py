from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import json
from datetime import datetime
import gspread

app = FastAPI()

# ✅ CORS (allow frontend)
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


# ✅ DEBUG: Check ENV
@app.get("/debug-env")
def debug_env():
    creds = os.getenv("GOOGLE_CREDENTIALS")
    return {
        "exists": creds is not None,
        "length": len(creds) if creds else 0
    }


# ✅ Connect to Google Sheets
def get_sheet():
    try:
        creds_json = os.getenv("GOOGLE_CREDENTIALS")

        if not creds_json:
            print("❌ ENV NOT FOUND")
            return None

        print("✅ ENV FOUND")

        creds_dict = json.loads(creds_json)

        print("✅ JSON PARSED")

        gc = gspread.service_account_from_dict(creds_dict)

        print("✅ AUTH SUCCESS")

        sheet = gc.open("Analyt Waitlist").sheet1

        print("✅ SHEET CONNECTED")

        return sheet

    except Exception as e:
        print("❌ FULL ERROR:", str(e))
        return None


# ✅ Root
@app.get("/")
def home():
    return {"status": "API Running"}


# ✅ Subscribe API
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
        print("❌ SAVE ERROR:", str(e))
        return {"error": "Failed to save email"}