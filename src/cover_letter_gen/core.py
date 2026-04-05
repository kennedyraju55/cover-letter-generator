"""Core business logic for Cover Letter Generator."""

import logging
import os
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Optional

import yaml

logger = logging.getLogger(__name__)

DEFAULT_CONFIG = {
    "llm": {"temperature": 0.7, "max_tokens": 2048},
    "cover_letter": {
        "max_words": 400,
        "tones": ["professional", "enthusiastic", "confident", "conversational"],
        "default_tone": "professional",
    },
    "revision": {"max_revisions": 5, "revision_dir": "revisions"},
    "export": {"output_dir": "output"},
}

TONES = {
    "professional": {"name": "Professional", "description": "Formal, polished, and business-appropriate", "icon": "👔"},
    "enthusiastic": {"name": "Enthusiastic", "description": "Energetic, passionate, and eager", "icon": "🔥"},
    "confident": {"name": "Confident", "description": "Bold, assertive, and achievement-focused", "icon": "💪"},
    "conversational": {"name": "Conversational", "description": "Friendly, approachable, and natural", "icon": "💬"},
}

SKILL_CATEGORIES = {
    "technical": ["python", "java", "javascript", "typescript", "react", "node", "aws", "azure", "gcp",
                   "docker", "kubernetes", "sql", "nosql", "machine learning", "ai", "ml", "data science",
                   "devops", "ci/cd", "api", "rest", "graphql", "microservices", "cloud"],
    "soft": ["leadership", "communication", "teamwork", "problem-solving", "analytical", "project management",
             "agile", "scrum", "mentoring", "collaboration", "presentation", "negotiation"],
    "domain": ["fintech", "healthcare", "e-commerce", "saas", "b2b", "b2c", "enterprise", "startup",
                "cybersecurity", "blockchain", "iot"],
}


def load_config(config_path: Optional[str] = None) -> dict:
    config = DEFAULT_CONFIG.copy()
    if config_path and os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            user_config = yaml.safe_load(f) or {}
        _deep_merge(config, user_config)
    return config


def _deep_merge(base: dict, override: dict) -> None:
    for key, value in override.items():
        if key in base and isinstance(base[key], dict) and isinstance(value, dict):
            _deep_merge(base[key], value)
        else:
            base[key] = value


def get_tones() -> dict:
    return TONES


def read_file(filepath: str, label: str = "File") -> str:
    """Read content from a text file."""
    path = Path(filepath)
    if not path.exists():
        logger.error("%s file not found: %s", label, filepath)
        raise FileNotFoundError(f"{label} file not found: {filepath}")
    content = path.read_text(encoding="utf-8")
    logger.info("Read %d chars from %s", len(content), filepath)
    return content


def extract_skills(text: str) -> dict:
    """Extract skills from text and categorize them."""
    text_lower = text.lower()
    found = {"technical": [], "soft": [], "domain": []}
    for category, skills in SKILL_CATEGORIES.items():
        for skill in skills:
            if skill in text_lower:
                found[category].append(skill)
    return found


def match_skills(resume_text: str, jd_text: str) -> dict:
    """Create a skill matching matrix between resume and job description."""
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)

    matched = {}
    missing = {}
    extra = {}

    for category in SKILL_CATEGORIES:
        r_set = set(resume_skills[category])
        j_set = set(jd_skills[category])
        matched[category] = sorted(r_set & j_set)
        missing[category] = sorted(j_set - r_set)
        extra[category] = sorted(r_set - j_set)

    total_jd = sum(len(jd_skills[c]) for c in SKILL_CATEGORIES)
    total_matched = sum(len(matched[c]) for c in SKILL_CATEGORIES)
    match_pct = round((total_matched / total_jd * 100) if total_jd > 0 else 0, 1)

    return {
        "matched": matched,
        "missing": missing,
        "extra": extra,
        "match_percentage": match_pct,
        "resume_skills": resume_skills,
        "jd_skills": jd_skills,
    }


def build_prompt(
    resume: str,
    job_description: str,
    company: str,
    tone: str,
    name: Optional[str] = None,
    skill_match: Optional[dict] = None,
) -> str:
    """Build the cover letter generation prompt."""
    name_str = f"Applicant Name: {name}\n" if name else ""

    skill_section = ""
    if skill_match:
        matched_all = []
        for cat_skills in skill_match["matched"].values():
            matched_all.extend(cat_skills)
        missing_all = []
        for cat_skills in skill_match["missing"].values():
            missing_all.extend(cat_skills)
        if matched_all:
            skill_section += f"\nMatched Skills: {', '.join(matched_all)}\n"
        if missing_all:
            skill_section += f"Skills to Address Creatively: {', '.join(missing_all)}\n"
        skill_section += f"Overall Match: {skill_match['match_percentage']}%\n"

    return (
        f"Write a personalized cover letter for the following job application.\n\n"
        f"{name_str}"
        f"Company: {company}\n"
        f"Tone: {tone}\n"
        f"{skill_section}\n"
        f"## Resume/Background:\n{resume}\n\n"
        f"## Job Description:\n{job_description}\n\n"
        f"Requirements:\n"
        f"1. Match specific resume highlights to job requirements\n"
        f"2. Show knowledge of the company and its values\n"
        f"3. Highlight 2-3 most relevant achievements with metrics\n"
        f"4. Explain why this role is a perfect fit\n"
        f"5. Include a strong opening hook (not 'I am writing to apply...')\n"
        f"6. End with a confident call to action\n"
        f"7. Keep it under 400 words\n"
        f"8. Use proper business letter format\n"
        f"9. Tone should be {tone}\n"
    )


def generate_cover_letter(
    resume: str,
    job_description: str,
    company: str,
    tone: str,
    name: Optional[str] = None,
    skill_match: Optional[dict] = None,
    config: Optional[dict] = None,
) -> str:
    """Generate a cover letter using the LLM."""
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    from common.llm_client import chat

    cfg = config or DEFAULT_CONFIG
    system_prompt = (
        "You are a professional career coach and expert cover letter writer. "
        "You craft compelling, personalized cover letters that highlight the perfect "
        "match between a candidate's experience and a job's requirements. "
        "Your letters get interviews."
    )
    user_prompt = build_prompt(resume, job_description, company, tone, name, skill_match)
    messages = [{"role": "user", "content": user_prompt}]
    logger.info("Generating %s cover letter for %s", tone, company)
    return chat(
        messages,
        system_prompt=system_prompt,
        temperature=cfg["llm"]["temperature"],
        max_tokens=cfg["llm"]["max_tokens"],
    )


def save_revision(content: str, company: str, revision_num: int, config: Optional[dict] = None) -> str:
    """Save a revision of the cover letter."""
    cfg = config or DEFAULT_CONFIG
    rev_dir = Path(cfg["revision"]["revision_dir"])
    rev_dir.mkdir(parents=True, exist_ok=True)
    safe_company = company.lower().replace(" ", "_")
    filename = f"{safe_company}_v{revision_num}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    filepath = rev_dir / filename
    filepath.write_text(content, encoding="utf-8")
    logger.info("Saved revision %d to %s", revision_num, filepath)
    return str(filepath)


def list_revisions(company: Optional[str] = None, config: Optional[dict] = None) -> list[dict]:
    """List saved revisions."""
    cfg = config or DEFAULT_CONFIG
    rev_dir = Path(cfg["revision"]["revision_dir"])
    if not rev_dir.exists():
        return []
    pattern = f"{company.lower().replace(' ', '_')}*.md" if company else "*.md"
    revisions = []
    for f in sorted(rev_dir.glob(pattern), reverse=True):
        stat = f.stat()
        revisions.append({
            "filename": f.name,
            "path": str(f),
            "size": stat.st_size,
            "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
        })
    return revisions
