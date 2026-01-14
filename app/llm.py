import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def extract_structured_data(ocr_text: str) -> dict:
    prompt = f"""
Return ONLY valid JSON.
No explanation. No markdown.

Extract:
- Candidate name
- Parent name
- Roll number
- Registration number
- Date of birth
- Exam year
- Board or University
- Institution
- Subject-wise marks (subject, max marks, obtained marks, grade)
- Overall result

Each field must include a confidence score (0–1).
If missing, set value to null.

OCR TEXT:
{ocr_text}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    content = response.choices[0].message.content.strip()

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {
            "error": "Invalid JSON from LLM",
            "raw_output": content
        }
