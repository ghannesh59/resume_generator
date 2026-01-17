import pytest
from Services.user_service import UserService
from data.mohith_resume import (
    name as mohith_name, email as mohith_email, phone as mohith_phone,
    location as mohith_location, education as mohith_education,
    experience as mohith_experience, projects as mohith_projects,
    skills as mohith_skills, achievements as mohith_achievements,
    certifications as mohith_certifications
)
from data.viswa_resume import (
    name as viswa_name, email as viswa_email, phone as viswa_phone,
    location as viswa_location, education as viswa_education,
    experience as viswa_experience, projects as viswa_projects,
    skills as viswa_skills, achievements as viswa_achievements,
    certifications as viswa_certifications
)

from data.karthik_resume import (
    name as karthik_name, email as karthik_email, phone as karthik_phone,
    location as karthik_location, education as karthik_education,
    experience as karthik_experience, projects as karthik_projects,
    skills as karthik_skills, achievements as karthik_achievements,
    certifications as karthik_certifications
)

from data.varshith_resume import (
    name as varshith_name, email as varshith_email, phone as varshith_phone,
    location as varshith_location, education as varshith_education,
    experience as varshith_experience, projects as varshith_projects,
    skills as varshith_skills, achievements as varshith_achievements,
    certifications as varshith_certifications
)

@pytest.mark.usefixtures("user_service")
class TestUserDataImport:

    def test_basic_info_import_1(self):
        user_service = UserService()
        user_data = user_service.load_user_data("123e4567-e89b-12d3-a456-426614174000")
        assert user_data is not None
        assert user_data["name"] == mohith_name
        assert user_data["email"] == mohith_email
        assert user_data["phone"] == mohith_phone
        assert user_data["location"] == mohith_location
        assert user_data["education"] == mohith_education
        assert user_data["experience"] == mohith_experience
        assert user_data["projects"] == mohith_projects
        assert user_data["skills"] == mohith_skills
        assert user_data["achievements"] == mohith_achievements
        assert user_data["certifications"] == mohith_certifications
        print("--------------------------------")
        print(user_data)
        print("--------------------------------")

    def test_basic_info_import_2():
        user_service = UserService()
        user_data = user_service.load_user_data("f47ac10b-58cc-4372-a567-0e02b2c3d479")
        assert user_data is not None
        assert user_data["name"] == viswa_name
        assert user_data["email"] == viswa_email
        assert user_data["phone"] == viswa_phone
        assert user_data["location"] == viswa_location
        assert user_data["education"] == viswa_education
        assert user_data["experience"] == viswa_experience
        assert user_data["projects"] == viswa_projects
        assert user_data["skills"] == viswa_skills
        assert user_data["achievements"] == viswa_achievements
        assert user_data["certifications"] == viswa_certifications
        print("--------------------------------")
        print(user_data)
        print("--------------------------------")

    def test_basic_info_import_3():
        user_service = UserService()
        user_data = user_service.load_user_data("550e8400-e29b-41d4-a716-446655440000")
        assert user_data is not None
        assert user_data["name"] == karthik_name
        assert user_data["email"] == karthik_email
        assert user_data["phone"] == karthik_phone
        assert user_data["location"] == karthik_location
        assert user_data["education"] == karthik_education
        assert user_data["experience"] == karthik_experience
        assert user_data["projects"] == karthik_projects
        assert user_data["skills"] == karthik_skills
        assert user_data["achievements"] == karthik_achievements
        assert user_data["certifications"] == karthik_certifications
        print("--------------------------------")
        print(user_data)
        print("--------------------------------")

    def test_basic_info_import_4():
        user_service = UserService()
        user_data = user_service.load_user_data("6ba7b810-9dad-11d1-80b4-00c04fd430c8")
        assert user_data is not None
        assert user_data["name"] == varshith_name
        assert user_data["email"] == varshith_email
        assert user_data["phone"] == varshith_phone
        assert user_data["location"] == varshith_location
        assert user_data["education"] == varshith_education
        assert user_data["experience"] == varshith_experience
        assert user_data["projects"] == varshith_projects
        assert user_data["skills"] == varshith_skills
        assert user_data["achievements"] == varshith_achievements
        assert user_data["certifications"] == varshith_certifications
        print("--------------------------------")
        print(user_data)
        print("--------------------------------")