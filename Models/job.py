class Job:
    def __init__(self, description, role, location, company_name):
        self.description = description
        self.role = role
        self.location = location
        self.company_name = company_name

    def __str__(self):
        return f"{self.role} in {self.location}"

    def __repr__(self):
        return f"Job(description='{self.description[:20]}...', role='{self.role}', location='{self.location}')"
    
    def to_json(self):
        return {
            "description": self.description,
            "role": self.role,
            "location": self.location
        }