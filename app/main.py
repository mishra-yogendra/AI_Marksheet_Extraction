import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from app.ocr import extract_text
from app.llm import extract_structured_data

app = FastAPI(title="Marksheet Extraction API (EasyOCR)")

@app.post("/extract")
async def extract_marksheet(file: UploadFile = File(...)):
    try:
        if not file.filename.lower().endswith((".png", ".jpg", ".jpeg")):
            raise HTTPException(status_code=400, detail="Only image files supported")

        contents = await file.read()
        if len(contents) > 10 * 1024 * 1024:
            raise HTTPException(status_code=413, detail="File too large")

        temp_path = f"temp_{file.filename}"
        with open(temp_path, "wb") as f:
            f.write(contents)

        ocr_text = extract_text(temp_path)
        if not ocr_text:
            os.remove(temp_path)
            raise HTTPException(status_code=422, detail="OCR failed")

        result = extract_structured_data(ocr_text)
        os.remove(temp_path)

        return result

    except Exception as e:
        return {
            "error": "Internal Server Error",
            "message": str(e)
        }
