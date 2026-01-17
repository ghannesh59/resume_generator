import time
from flask import Flask, request
from flasgger import Swagger
from Models.job import Job
from Models.resume import Resume
from Models.user import User
from Services.resume_service import ResumeService
from Services.user_service import UserService
from res_maker import make_resume
import os
import uuid
import boto3
from datetime import datetime, timedelta

app = Flask(__name__)
swagger = Swagger(app)

s3_client = boto3.client('s3')

# storage_client = storage.Client()
BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')

def delete_local_file(file_path):
    """
    Delete a local file given its path
    
    Args:
        file_path (str): Path to the file to be deleted
    """
    try:
        os.remove(file_path)
        print(f"Successfully deleted {file_path}")
    except Exception as e:
        print(f"Error deleting file {file_path}: {str(e)}")

@app.route('/', methods=['GET'])
def index():
    """
    Root endpoint
    ---
    responses:
      200:
        description: Welcome message
    """
    return {"message": "Welcome to Resume Generator API. Use /hello or /resume endpoints."}

@app.route('/hello', methods=['GET'])
def hello_world():
    """
    A simple hello world endpoint
    ---
    responses:
      200:
        description: Returns a greeting message
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Hello, World!"
    """

    skills = "{'skills': ['Programming Language: Python, SQL, JavaScript, TypeScript, Java, C++, Go', 'Frameworks and Databases: Flask, PostgreSQL, MongoDB, SQLAlchemy, Redis, Django, Node.js', 'Cloud Technologies: AWS Lambda, Docker, Kubernetes, CI/CD, Git, GitHub, GitLab', 'Other Technologies: RESTful APIs, Agile, Scrum, Unit Testing, Data Structures, Algorithms, Linux/Unix']}"
    experiences = "[{'title': 'Software Engineer 2', 'company': 'Quicksight.ai', 'location': 'Remote', 'duration': 'Jan 2024 - Present', 'description': ['Architected and implemented a Python-based AI-powered video search platform using Flask, integrating CLIP and Whisper models, resulting in a 40% improvement in search accuracy and speed', 'Developed responsive frontend components using React and TypeScript, implementing CI/CD pipelines with GitLab for automated testing and deployment, reducing release cycles by 25%', 'Designed and deployed scalable microservices on AWS using serverless technologies, leveraging Terraform for Infrastructure as Code, resulting in a 30% reduction in operational costs', 'Orchestrated containerized workloads using Kubernetes and Docker, implementing Agile methodologies to enhance team productivity and streamline development processes']}, {'title': 'Software Engineer', 'company': 'Zwive', 'location': 'Remote', 'duration': 'Aug 2023 - Dec 2023', 'description': ['Developed a full-stack marketplace application using Python (Flask) for the backend, React with TypeScript for the frontend, and MongoDB for data storage, resulting in a 30% increase in user engagement', 'Implemented AWS serverless architecture using Lambda and API Gateway, reducing server costs by 40% while improving scalability and performance', 'Utilized Terraform to manage and version control AWS infrastructure, enabling rapid iterations and reducing deployment time by 50%']}, {'title': 'Web Development Student Assistant', 'company': 'University of California, Riverside', 'location': 'Remote', 'duration': 'Oct 2021 – Aug 2022', 'description': ['Developed responsive and accessible web applications using React and TypeScript, integrating with Python-based APIs to display agricultural data for 500+ Californian farmers', 'Implemented data visualization components using D3.js and React, improving data interpretation and decision-making capabilities for users by 35%', 'Deployed and managed applications on AWS EKS, utilizing Terraform for infrastructure provisioning and GitLab CI/CD for automated deployments, reducing manual errors by 60%']}]"
    summary = "Seasoned Software Engineer with 3 years of experience, specializing in Python, Flask, and cloud technologies. Demonstrated expertise in architecting AI-powered platforms, developing full-stack applications, and implementing serverless microservices, resulting in significant improvements in search accuracy, user engagement, and operational efficiency. Proficient in AWS, Docker, Kubernetes, and CI/CD pipelines, with a track record of reducing costs and streamlining development processes across multiple projects."

    skills_dict = eval(skills)
    experiences_list = eval(experiences)
    return {"skills": skills_dict, "experiences": experiences_list, "summary": summary}

@app.route('/resume', methods=['POST'])
def resume():
    """
    Generate a resume and upload it to GCP bucket
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            job_description:
              type: string
              description: The job description to tailor the resume for
            company_name:
              type: string
              description: The company name
            location:
              type: string
              description: The job location
          required:
            - job_description
            - company_name
            - location
    responses:
      200:
        description: Returns the generated resume and its public URL
        schema:
          type: object
          properties:
            resume:
              type: string
              description: The generated resume content
            file_url:
              type: string
              description: Public URL to access the resume
      400:
        description: Missing required parameters or upload error
    """
    data = request.get_json()
    
    required_params = ['job_description', 'company_name', 'location','user_key']
    if not all(param in data for param in required_params):
        return {"error": "Missing required parameters"}, 400

    user_service = UserService()
    user_data = user_service.load_user_data(data['user_key'])

    resume = Resume(
        summary="",
        skills=user_data['skills'],
        experiences=user_data['experience'],
        education=user_data['education'],
        achievements=user_data['achievements'],
        certifications=user_data['certifications']
      )


    job = Job(
        description=data['job_description'],
        role="Software Engineer",
        location=data['location'],
        company_name=data['company_name']
    )


    user = User(
        first_name=user_data['name'].split(" ")[0],
        last_name=user_data['name'].split(" ")[-1],
        phone=user_data['phone'],
        email=user_data['email'],
        location=user_data['location'],
        resume=resume,
        linkedin_url=user_data['linkedin'],
        github_url=user_data['github']
      )
    ai_client = 'claude'
    resume_service = ResumeService()
    resume_data = resume_service.generate_info_from_resume(job=job, user=user, api_key = os.getenv(f'{ai_client.upper()}_API_KEY'), client_type=ai_client)

    user.resume.experiences = resume_data['experiences']
    user.resume.skills = resume_data['skills']
    user.resume.summary = resume_data['summary']

    # return {"user": user.to_json(), "job": job.to_json(), "resume_data": resume_data}
    
    resume_path = make_resume(
        job=job,
        user=user,
        ai_client='claude'
    )

    print('resume_path : ',resume_path)
    try:
        # Generate unique filename with .pdf extension
        filename = f"resume_{uuid.uuid4()}.pdf"
        
        
         # Upload PDF file to S3
        with open(resume_path, 'rb') as pdf_file:
            s3_client.upload_fileobj(
                pdf_file,
                BUCKET_NAME,
                filename,
                ExtraArgs={'ContentType': 'application/pdf'}
            )

        # Generate a presigned URL
        file_url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': BUCKET_NAME, 'Key': filename},
            ExpiresIn=3600
        )
        
        # Delete the local file after successful upload
        delete_local_file(resume_path)
        
        return {
            "resume": resume_path,
            "file_url": file_url
        }
    
    except Exception as e:
        print(f"Upload error: {str(e)}")  # Add detailed logging
        return {"error": f"Failed to upload file: {str(e)}"}, 400

if __name__ == '__main__':
    app.run(debug=True)