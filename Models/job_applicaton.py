import datetime

class JobApplication:
    def __init__(self, job, resume, user):
        self.job = job
        self.resume = resume
        self.user = user
        self.date = datetime.datetime.now()
    
    def to_dict(self):
        return {
            'job_id': self.job.id,
            'resume_id': self.resume.id,
            'user_id': self.user.id,
            'application_date': self.date.isoformat(),
        }
    
    @classmethod
    def from_dict(cls, data, job, resume, user):
        instance = cls(job, resume, user)
        if 'application_date' in data:
            instance.date = datetime.datetime.fromisoformat(data['application_date'])
        return instance
        