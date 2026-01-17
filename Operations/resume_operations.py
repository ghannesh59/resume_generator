import json

from Operations.prompt_operations import skills_prompt, exp_prompt, summary_prompt


def get_skills(job_description):
    skills = get_skills_in_resume()
    prompt = skills_prompt.replace("{{CURRENT_SKILLS}}", str(skills))
    prompt = prompt.replace("{{JOB_DESCRIPTION}}", job_description)
    output_string = run_openAI_prompt(prompt)
    p = json.loads(output_string)
    return p

def get_experiences(exp, job_description):
    print(exp)
    prompt = exp_prompt.replace("{{ORIGINAL_EXPERIENCES}}", str(exp))
    prompt = prompt.replace("{{JOB_DESCRIPTION}}", job_description)
    output_string = run_openAI_prompt(prompt)
    p = json.loads(output_string.replace('```','').replace('json',''))
    print(p)
    return p


def get_summary(skills, experiences, job_description):
    prompt = summary_prompt.replace("{{SKILLS}}", str(skills)).replace("{{EXPERIENCES}}",
                                                                               str(experiences)).replace(
        "{{JOB_DESCRIPTION}}", job_description)
    p = run_prompt(prompt)

    return p

def load_resume_data():
    data = './data.json'
    with open(data) as f:
        return json.load(f)


def get_skills_in_resume():
    return load_resume_data()['skills']


def get_experience_in_resume():
    return load_resume_data()['experience']