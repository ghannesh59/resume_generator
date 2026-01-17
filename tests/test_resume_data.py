import pytest
from data.varshith_resume import (
    name, email, phone, location, education, experience, 
    projects, skills, achievements, Certifications
)

def test_basic_info():
    assert isinstance(name, str)
    assert "@" in email  # Basic email format check
    assert phone.startswith("+1")  # US phone format check
    assert isinstance(location, str)

def test_education_structure():
    assert isinstance(education, list)
    for edu in education:
        assert isinstance(edu, dict)
        required_fields = {"degree", "university", "location", "year", "GPA"}
        assert all(field in edu for field in required_fields)
        assert isinstance(edu["GPA"], float)
        assert 0 <= edu["GPA"] <= 4.0

def test_experience_structure():
    assert isinstance(experience, list)
    for exp in experience:
        assert isinstance(exp, dict)
        required_fields = {"title", "company", "location", "duration", "description"}
        assert all(field in exp for field in required_fields)
        assert isinstance(exp["description"], list)

def test_projects_structure():
    assert isinstance(projects, list)
    for project in projects:
        assert isinstance(project, dict)
        required_fields = {"title", "technologies", "description"}
        assert all(field in project for field in required_fields)
        assert isinstance(project["technologies"], list)
        assert isinstance(project["description"], list)

def test_skills_format():
    assert isinstance(skills, list)
    for skill in skills:
        assert isinstance(skill, str)
        assert ":" in skill  # Check if skills follow "Category: Skills" format

def test_achievements_structure():
    assert isinstance(achievements, list)
    for achievement in achievements:
        assert isinstance(achievement, dict)
        assert len(achievement) == 1  # Each achievement should have one category
        for category, items in achievement.items():
            assert isinstance(items, list)

def test_certifications():
    assert isinstance(Certifications, list)
    for cert in Certifications:
        assert isinstance(cert, str) 