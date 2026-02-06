Resume Generator is an AI-powered Python/Flask REST API that dynamically generates tailored PDF resumes based on a job description. Given a user's base resume data and a target job posting, it uses large language models (Claude, OpenAI, or Groq) to rewrite the user's skills, experiences, and professional summary to closely match the job requirements, then renders a polished PDF resume and uploads it to AWS S3.
The core idea: instead of manually tweaking your resume for every application, you POST a job description to the API, and it returns a professionally formatted, ATS-friendly PDF that emphasizes the most relevant aspects of your background.
How it works

You send a POST request with the job description, company name, and your user key
The API loads your base resume data (education, experience, skills, etc.)
It fires off prompts to an LLM to:

Rewrite your skills to match what the job is looking for
Rephrase your experience bullets with relevant keywords and metrics
Generate a professional summary tying it all together


ReportLab builds a formatted PDF (Garamond font, proper sections, clickable links)
PDF gets uploaded to S3 and you get back a presigned URL

Skills and experiences are generated in parallel using ThreadPoolExecutor since they don't depend on each other. Summary runs after both are done because it needs them as input.

<img width="862" height="633" alt="Screenshot 2026-02-06 at 3 20 13 PM" src="https://github.com/user-attachments/assets/4200a7c6-c469-43fc-8917-fbf95b678151" />


<img width="862" height="524" alt="Screenshot 2026-02-06 at 3 21 06 PM" src="https://github.com/user-attachments/assets/39635d2e-af15-406e-8527-b4aa56cab3eb" />


