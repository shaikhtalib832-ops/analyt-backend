from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import csv, os

app = FastAPI()

# Allow frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Email(BaseModel):
    email: str

FILE = "emails.csv"

@app.get("/")
def home():
    return {"status": "API Running"}

@app.post("/subscribe")
def subscribe(data: Email):
    exists = os.path.isfile(FILE)

    with open(FILE, "a", newline="") as f:
        writer = csv.writer(f)

        if not exists:
            writer.writerow(["email"])

        writer.writerow([data.email])

    return {"success": True}