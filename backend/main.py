
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from extractor import extract_timestamps


app = FastAPI(title="Network Log Analyzer API")

# Allow the React development server to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "Network Log Analyzer API is running"}


@app.post("/extract")
async def extract(file: UploadFile = File(...)):

    # Only accept .txt files
    if not file.filename or not file.filename.lower().endswith(".txt"):
        raise HTTPException(
            status_code=400,
            detail="Please upload a .txt file."
        )

    # Limit uploaded files to 5 MB
    content = await file.read(5 * 1024 * 1024 + 1)

    if len(content) > 5 * 1024 * 1024:
        raise HTTPException(
            status_code=413,
            detail="File must be smaller than 5 MB."
        )

    # Convert file bytes into text
    try:
        log_text = content.decode("utf-8-sig")
    except UnicodeDecodeError:
        raise HTTPException(
            status_code=400,
            detail="File must contain UTF-8 encoded text."
        )

    if not log_text.strip():
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is empty."
        )

    # Call our existing Python extractor
    timestamps = extract_timestamps(log_text)

    return {
        "timestamps": timestamps,
        "count": len(timestamps),
        "message": (
            "Timestamps extracted successfully."
            if timestamps
            else "No relevant network timestamps were identified."
        )
    }
