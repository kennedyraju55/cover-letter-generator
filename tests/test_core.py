"""Tests for Cover Letter Generator core module."""

import pytest
from cover_letter_gen.core import (
    build_prompt,
    read_file,
    load_config,
    get_tones,
    extract_skills,
    match_skills,
    save_revision,
    list_revisions,
    _deep_merge,
    TONES,
)


@pytest.fixture
def sample_resume():
    return "Software Engineer with 5 years experience in Python, machine learning, AWS, and cloud platforms. Led team of 5."

@pytest.fixture
def sample_jd():
    return "Looking for a Senior Engineer. Requirements: Python, ML, AWS, Docker, Kubernetes. Benefits: remote work."


class TestBuildPrompt:
    def test_prompt_contains_company(self, sample_resume, sample_jd):
        prompt = build_prompt(sample_resume, sample_jd, "Google", "professional")
        assert "Google" in prompt

    def test_prompt_contains_resume(self, sample_resume, sample_jd):
        prompt = build_prompt(sample_resume, sample_jd, "Google", "professional")
        assert "5 years" in prompt

    def test_prompt_contains_tone(self, sample_resume, sample_jd):
        prompt = build_prompt(sample_resume, sample_jd, "Google", "enthusiastic")
        assert "enthusiastic" in prompt

    def test_prompt_contains_name(self, sample_resume, sample_jd):
        prompt = build_prompt(sample_resume, sample_jd, "Google", "professional", name="Jane Doe")
        assert "Jane Doe" in prompt


class TestReadFile:
    def test_reads_existing_file(self, tmp_path):
        f = tmp_path / "resume.txt"
        f.write_text("My resume content")
        result = read_file(str(f), "Resume")
        assert result == "My resume content"

    def test_nonexistent_file_raises(self):
        with pytest.raises(FileNotFoundError):
            read_file("nonexistent_resume.txt", "Resume")


class TestSkillMatching:
    def test_extract_skills(self, sample_resume):
        skills = extract_skills(sample_resume)
        assert "python" in skills["technical"]

    def test_match_skills(self, sample_resume, sample_jd):
        match = match_skills(sample_resume, sample_jd)
        assert match["match_percentage"] >= 0
        assert "python" in match["matched"]["technical"]

    def test_missing_skills(self, sample_resume, sample_jd):
        match = match_skills(sample_resume, sample_jd)
        assert "docker" in match["missing"]["technical"] or "kubernetes" in match["missing"]["technical"]


class TestConfig:
    def test_default_config(self):
        config = load_config()
        assert config["llm"]["temperature"] == 0.7

    def test_tones_exist(self):
        assert len(get_tones()) >= 4

    def test_deep_merge(self):
        base = {"a": {"b": 1}}
        _deep_merge(base, {"a": {"b": 2}})
        assert base["a"]["b"] == 2


class TestRevisions:
    def test_save_revision(self, tmp_path):
        config = {"revision": {"revision_dir": str(tmp_path / "revs")}}
        path = save_revision("content", "TestCo", 1, config)
        from pathlib import Path
        assert Path(path).exists()

    def test_list_empty_revisions(self, tmp_path):
        config = {"revision": {"revision_dir": str(tmp_path / "empty")}}
        assert list_revisions(config=config) == []
