import json

class Resume:
    def __init__(self, summary=None, skills=None, education=None, experiences=None, achievements=None, certifications=None):
        self.summary = summary
        self.skills = skills
        self.education = education
        self.experiences = experiences
        self.achievements = achievements
        self.certifications = certifications

    def to_json(self):
        return {
            'summary': self.summary,
            'skills': self.skills,
            'education': self.education,
            'experiences': self.experiences,
            'achievements': self.achievements,
            'certifications': self.certifications
        }

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        return cls(**data)

    def __str__(self):
        return f"Summary: {self.summary} \nSkills: {self.skills} \nEducation: {self.education} \nExperiences: {self.experiences} "
