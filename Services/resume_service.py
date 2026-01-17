# services/resume_service.py
import json
from concurrent.futures import ThreadPoolExecutor

from Models.job import Job
from Models.user import User
import Operations.prompt_operations
from Services.ai_client_service import ai_client_service
# from .resume_maker_service import resume_maker_service


class ResumeService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ResumeService, cls).__new__(cls)
            cls._instance._load_prompts()
        return cls._instance

    def _load_prompts(self):
        # Load prompts from a file or define them here
        self.summary_prompt = Operations.prompt_operations.summary_prompt
        self.exp_prompt = Operations.prompt_operations.exp_prompt
        self.skills_prompt = Operations.prompt_operations.skills_prompt

    def get_skills(self, job_description, client_type, api_key, skills):
        prompt = self.skills_prompt.replace("{{JOB_DESCRIPTION}}", job_description).replace("{{CURRENT_SKILLS}}",
                                                                                            str(skills))
        return ai_client_service.run_prompt(prompt, client_type, api_key)

    def get_experiences(self, exp, job_description, client_type, api_key):
        prompt = self.exp_prompt.replace("{{ORIGINAL_EXPERIENCES}}", str(exp)).replace("{{JOB_DESCRIPTION}}",
                                                                                       job_description)
        return ai_client_service.run_prompt(prompt, client_type, api_key)

    def get_summary(self, skills, experiences, job_description, client_type, api_key):
        prompt = self.summary_prompt.replace("{{SKILLS}}", str(skills)).replace("{{EXPERIENCES}}",
                                                                                str(experiences)).replace(
            "{{JOB_DESCRIPTION}}", job_description)
        return ai_client_service.run_prompt(prompt, client_type, api_key)
    
    def generate_info_from_resume(self, user: User, job: Job, api_key: str, client_type: str):
        with ThreadPoolExecutor(max_workers=2) as executor:
            print(job)
            skills_future = executor.submit(
                self.get_skills, job.description, client_type, api_key, user.resume.skills
            )
            
            experiences_future = executor.submit(
                self.get_experiences, user.resume.experiences, job.description, client_type, api_key
            )
            
            skills, cost1, input_tokens1, output_tokens1 = skills_future.result()
            experiences, cost2, input_tokens2, output_tokens2 = experiences_future.result()

        summary, cost3, input_tokens3, output_tokens3 = self.get_summary(
            skills, experiences, job.description, client_type, api_key
        )

        return {
            "skills": skills, 
            "experiences": experiences, 
            "summary": summary, 
            "cost": cost1 + cost2 + cost3,
            "input_tokens": input_tokens1 + input_tokens2 + input_tokens3,
            "output_tokens": output_tokens1 + output_tokens2 + output_tokens3
        }

    # def generate_info_from_resume(self, job_description, client_type, api_key):
    #     with open('./mohith_resume.json', 'r') as f:
    #         data = json.load(f)

    #     skills = self.get_skills(job_description, client_type, api_key, data['skills'])
    #     experiences = data['experience']
    #     changed_exp = [self.get_experiences(exp, job_description, client_type, api_key) for exp in experiences]
    #     summary = self.get_summary(skills, changed_exp, job_description, client_type, api_key)

    #     return skills, changed_exp, summary

    # def make_resume(self, user, job, client_type, api_key):
    #     skills, experiences, summary = self.generate_info_from_resume(job=job,
    #                                                                   client_type=client_type, api_key=api_key)
    #     self._generate_resume(user.author,
    #                           user.name,
    #                           user.location,
    #                           user.phone,
    #                           user.linkedIn,
    #                           user.github,
    #                           user.relocation,
    #                           skills,
    #                           experiences,
    #                           summary,
    #                           job.job_description,
    #                           client_type,
    #                           api_key
    #                           )
    #     pass
    

    # def _generate_resume(self, author, name, location, phone, linkedIn, github, relocation, skills, experiences,summary,
    #                      job_description):
    #     user = {
    #         'author': author,
    #         'name': name,
    #         'location': location,
    #         'phone': phone,
    #         'linkedIn': linkedIn,
    #         'github': github,
    #         'relocation': relocation,
    #         'job': {
    #             job_description: job_description,
    #             'role': 'SDE',
    #             'company': ''
    #         }
    #     }
    #     resume_maker_service.mak_resume(job_description=job_description, user_info=user,
    #                                      output_path=f'{author.lower().replace(' ', '_')}_resume.pdf', skills=skills,
    #                                      experiences=experiences, summary=summary)


resume_service = ResumeService()
