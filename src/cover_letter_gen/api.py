"""FastAPI REST API for Cover Letter Generator."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import uvicorn

from cover_letter_gen.core import (
    generate_cover_letter,
    extract_skills,
    match_skills,
    get_tones,
)

app = FastAPI(
    title="Cover Letter Generator API",
    description="REST API for Cover Letter Generator",
    version="1.0.0",
)


# ---------------------------------------------------------------------------
# Request / Response models
# ---------------------------------------------------------------------------

class CoverLetterRequest(BaseModel):
    resume: str = Field(..., description="Resume text")
    job_description: str = Field(..., description="Job description text")
    company: str = Field(..., description="Company name")
    tone: str = Field(..., description="Writing tone")
    name: Optional[str] = Field(None, description="Applicant name")


class ExtractSkillsRequest(BaseModel):
    text: str = Field(..., description="Text to extract skills from")


class MatchSkillsRequest(BaseModel):
    resume_text: str = Field(..., description="Resume text")
    jd_text: str = Field(..., description="Job description text")


class TextResponse(BaseModel):
    result: str


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "cover-letter-generator"}


@app.post("/generate-cover-letter", response_model=TextResponse)
async def api_generate_cover_letter(req: CoverLetterRequest):
    try:
        result = generate_cover_letter(
            resume=req.resume,
            job_description=req.job_description,
            company=req.company,
            tone=req.tone,
            name=req.name,
        )
        return TextResponse(result=result)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/extract-skills")
async def api_extract_skills(req: ExtractSkillsRequest):
    try:
        result = extract_skills(text=req.text)
        return result
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/match-skills")
async def api_match_skills(req: MatchSkillsRequest):
    try:
        result = match_skills(
            resume_text=req.resume_text,
            jd_text=req.jd_text,
        )
        return result
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/tones")
async def api_get_tones():
    try:
        return get_tones()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
