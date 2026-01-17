import pytest
import json
from pathlib import Path

@pytest.fixture
def sample_resume_data():
    return {
        "name": "Krishna V Pabbisetty",
        "email": "krishnavpabbisetty@gmail.com",
        "phone": "+1(214)-885-9784",
        "location": "San Jose, CA",
        "LinkedIn": "https://www.linkedin.com/in/krishnavpabbisetty/",
        "GitHub": "https://github.com/KrishnaVPabbisetty",
        "relocation": True,
        "education": [
            {
                "degree": "Master of Science in Software Engineering",
                "university": "San Jose State University (SJSU)",
                "location": "San Jose, CA",
                "year": "Aug 2023 - May 2025",
                "GPA": 3.8,
                "relevant_coursework": [
                    "Distributed Systems",
                    "High Performance Computing",
                    "Software Systems Engineering",
                    "Data Mining"
                ]
            }
        ]
    }

@pytest.fixture
def sample_output_path(tmp_path):
    """Provides a temporary directory path for test outputs"""
    return tmp_path / "test_resume.pdf" 