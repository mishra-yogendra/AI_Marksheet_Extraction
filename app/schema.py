from typing import Optional, List
from pydantic import BaseModel

class Subject(BaseModel):
    subject: Optional[str]
    max_marks: Optional[str]
    obtained_marks: Optional[str]
    grade: Optional[str]
    confidence: float

class MarksheetResponse(BaseModel):
    candidate: dict
    subjects: List[Subject]
    overall: dict
