from Models.resume import Resume

class User:
    def __init__(self, first_name, last_name, phone, email, location, relocation=False, resume=None, linkedin_url=None, github_url=None):
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.email = email
        self.location = location
        self.resume = resume if resume is not None else Resume(summary="", skills=[], education=[], experiences=[])
        self.relocation = relocation
        self.linkedin_url = linkedin_url
        self.github_url = github_url

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    # def __str__(self):
    #     return f"{self.full_name} - {self.email}"

    def __repr__(self):
        return (f"User(first_name='{self.first_name}', last_name='{self.last_name}', "
                f"phone='{self.phone}', email='{self.email}', location='{self.location}', "
                f"resume={self.resume})")

    def to_json(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone": self.phone,
            "email": self.email,
            "location": self.location,
            "linkedin_url": self.linkedin_url,
            "github_url": self.github_url,
            "resume": self.resume.to_json() if self.resume else None,
        }

    @classmethod
    def from_dict(cls, data):
        resume_data = data.pop('resume', None)
        user = cls(**data)
        if resume_data:
            user.resume = Resume.from_json(resume_data)
        return user