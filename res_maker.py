import configparser
import json
import os
import shutil
from datetime import datetime
import time
from dotenv import load_dotenv
import logging
from Models.job import Job
from Models.user import User
from Services.resume_service import resume_service

load_dotenv()

# from Executor.ThreadPoolExecutorSingleton import ThreadPoolExecutorSingleton
# from prompts import get_experiences, get_skills, get_summary
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics, ttfonts
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
import anthropic

# from services.resume_service import resume_service

PAGE_WIDTH, PAGE_HEIGHT = A4
FULL_COLUMN_WIDTH = (PAGE_WIDTH - 1 * inch)
TITLE_COLUMN_WIDTH = FULL_COLUMN_WIDTH * 0.7
DURATION_COLUMN_WIDTH = FULL_COLUMN_WIDTH * 0.3
PROJECT_TITLE_COLUMN_WIDTH = FULL_COLUMN_WIDTH * 0.3
PROJECT_DESCRIPTION_COLUMN_WIDTH = FULL_COLUMN_WIDTH * 0.7
GARAMOND_REGULAR_FONT_PATH = './res/fonts/EBGaramond-Regular.ttf'
GARAMOND_REGULAR = 'Garamond_Regular'
GARAMOND_BOLD_FONT_PATH = './res/fonts/EBGaramond-Bold.ttf'
GARAMOND_BOLD = 'Garamond_Bold'
GARAMOND_SEMIBOLD_FONT_PATH = './res/fonts/EBGaramond-SemiBold.ttf'
GARAMOND_SEMIBOLD = 'Garamond_Semibold'

pdfmetrics.registerFont(ttfonts.TTFont(GARAMOND_REGULAR, GARAMOND_REGULAR_FONT_PATH))
pdfmetrics.registerFont(ttfonts.TTFont(GARAMOND_BOLD, GARAMOND_BOLD_FONT_PATH))
pdfmetrics.registerFont(ttfonts.TTFont(GARAMOND_SEMIBOLD, GARAMOND_SEMIBOLD_FONT_PATH))

NAME_PARAGRAPH_STYLE = ParagraphStyle('name_paragraph', fontName=GARAMOND_SEMIBOLD, fontSize=24, alignment=1)
CONTACT_PARAGRAPH_STYLE = ParagraphStyle('contact_paragraph', fontName=GARAMOND_REGULAR, fontSize=12, alignment=1)
SECTION_PARAGRAPH_STYLE = ParagraphStyle('section_paragraph', fontName=GARAMOND_SEMIBOLD, fontSize=13,
                                         textTransform='uppercase')
COMPANY_HEADING_PARAGRAPH_STYLE = ParagraphStyle('company_heading_paragraph', fontName=GARAMOND_SEMIBOLD, fontSize=13)
COMPANY_TITLE_PARAGRAPH_STYLE = ParagraphStyle('company_title_paragraph', fontName=GARAMOND_REGULAR, fontSize=12)
COMPANY_DURATION_PARAGRAPH_STYLE = ParagraphStyle('company_duration_paragraph', fontName=GARAMOND_SEMIBOLD, fontSize=13,
                                                  alignment=2)
COMPANY_LOCATION_PARAGRAPH_STYLE = ParagraphStyle('company_location_paragraph', fontName=GARAMOND_REGULAR, fontSize=12,
                                                  alignment=2)
JOB_DETAILS_PARAGRAPH_STYLE = ParagraphStyle('job_details_paragraph', leftIndent=12, fontName=GARAMOND_REGULAR,
                                             fontSize=12, leading=14)

# Custom filter to exclude OpenAI API logs
class ExcludeOpenAIFilter(logging.Filter):
    def filter(self, record):
        return not (record.getMessage().startswith('HTTP Request:') and 'api.openai.com' in record.getMessage())

# Setup logging
log_dir = '/tmp/logs'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_file = os.path.join(log_dir, 'resume_generation_mohith.log')

logging.basicConfig(level=logging.INFO)

file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

file_handler.addFilter(ExcludeOpenAIFilter())

root_logger = logging.getLogger()
root_logger.addHandler(file_handler)

def appendSectionTableStyle(table_styles, running_row_index):
    table_styles.append(('TOPPADDING', (0, running_row_index), (1, running_row_index), 5))
    table_styles.append(('BOTTOMPADDING', (0, running_row_index), (1, running_row_index), 5))
    table_styles.append(('LINEBELOW', (0, running_row_index), (-1, running_row_index), 1, colors.black))

def _generate_resume(
        file_path, json_file_path,
        author, email, phone, debug, location,
        skills, experience, summary, education, linkedin_url, github_url,
        achievements, certifications
):
    doc = SimpleDocTemplate(file_path, pagesize=A4, showBoundary=0, leftMargin=0.2 * inch, rightMargin=0.2 * inch,
                            topMargin=0.1 * inch, bottomMargin=0.1 * inch, title=f"Resume of {author}", author=author
                            )
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    table_data = []
    table_styles = []
    running_row_index = 0

    # if debug == 'true':
    #     table_styles.append(('GRID', (0, 0), (-1, -1), 0, colors.black))

    table_styles.append(('ALIGN', (0, 0), (0, -1), 'LEFT'))
    table_styles.append(('ALIGN', (1, 0), (1, -1), 'RIGHT'))
    table_styles.append(('LEFTPADDING', (0, 0), (-1, -1), 0))
    table_styles.append(('RIGHTPADDING', (0, 0), (-1, -1), 0))

    table_data.append([Paragraph(author, NAME_PARAGRAPH_STYLE)])
    table_styles.append(('SPAN', (0, running_row_index), (1, running_row_index)))
    table_styles.append(('BOTTOMPADDING', (0, running_row_index), (1, running_row_index), 18))  # Increased padding
    running_row_index += 1

    linkedin_url = linkedin_url
    linkedin_display = "LinkedIn"

    github_url = github_url
    github_display = "github"

    contact_line = (
        f'{email} | {phone} | '
        f'<a href="{linkedin_url}" color="blue">{linkedin_display}</a> | '
        f'<a href="{github_url}" color="blue">{github_display}</a> | '
        f'{location} (Ready to Relocate)'
    )
    table_data.append([Paragraph(contact_line, CONTACT_PARAGRAPH_STYLE)])
    table_styles.append(('SPAN', (0, running_row_index), (1, running_row_index)))
    table_styles.append(('BOTTOMPADDING', (0, running_row_index), (1, running_row_index), 1))
    running_row_index += 1


    table_data.append([Paragraph("Summary", SECTION_PARAGRAPH_STYLE)])
    appendSectionTableStyle(table_styles, running_row_index)
    running_row_index += 1

    # Add summary content
    # summary = generate_summary('', '', job_description)
    print(summary)
    table_data.append([Paragraph(summary['summary'], JOB_DETAILS_PARAGRAPH_STYLE)])
    table_styles.append(('SPAN', (0, running_row_index), (1, running_row_index)))
    running_row_index += 1


    table_data.append([Paragraph("Experience", SECTION_PARAGRAPH_STYLE)])
    appendSectionTableStyle(table_styles, running_row_index)
    running_row_index += 1

    # Append experience
    for job_experience in experience:
        print(job_experience)
        table_data.append([
            Paragraph(job_experience['company'], COMPANY_HEADING_PARAGRAPH_STYLE),
            Paragraph(job_experience['duration'], COMPANY_DURATION_PARAGRAPH_STYLE),
        ])
        table_styles.append(('TOPPADDING', (0, running_row_index), (1, running_row_index), 5))
        running_row_index += 1

        table_data.append([
            Paragraph(job_experience['title'], COMPANY_TITLE_PARAGRAPH_STYLE),
            Paragraph(job_experience['location'], COMPANY_LOCATION_PARAGRAPH_STYLE),
        ])
        table_styles.append(('TOPPADDING', (0, running_row_index), (1, running_row_index), 1))
        running_row_index += 1

        for line in job_experience["description"]:
            table_data.append([Paragraph(line, bulletText='•', style=JOB_DETAILS_PARAGRAPH_STYLE)])
            table_styles.append(('TOPPADDING', (0, running_row_index), (1, running_row_index), 1))
            table_styles.append(('BOTTOMPADDING', (0, running_row_index), (1, running_row_index), 0))
            table_styles.append(('SPAN', (0, running_row_index), (1, running_row_index)))
            running_row_index += 1

    # Append education heading
    table_data.append([Paragraph("Education", SECTION_PARAGRAPH_STYLE)])
    appendSectionTableStyle(table_styles, running_row_index)
    running_row_index += 1

    # Append education
    for education in education:
        table_data.append([
            Paragraph(education['university'], COMPANY_HEADING_PARAGRAPH_STYLE),
            Paragraph(education['year'], COMPANY_DURATION_PARAGRAPH_STYLE),
        ])
        table_styles.append(('TOPPADDING', (0, running_row_index), (1, running_row_index), 2))
        running_row_index += 1

        table_data.append([
            Paragraph(education['degree'], COMPANY_TITLE_PARAGRAPH_STYLE),
            Paragraph(education['location'], COMPANY_LOCATION_PARAGRAPH_STYLE),
        ])
        table_styles.append(('TOPPADDING', (0, running_row_index), (1, running_row_index), 1))
        running_row_index += 1
    
    table_data.append([Paragraph("Skills", SECTION_PARAGRAPH_STYLE)])
    appendSectionTableStyle(table_styles, running_row_index)
    running_row_index += 1

    # print(skills)
    for skill in skills['skills']:
        parts = skill.split(': ', 1)
        if len(parts) == 2:
            heading, skills_list = parts
            table_data.append([Paragraph(f"<b>{heading}</b>: {skills_list}", style=JOB_DETAILS_PARAGRAPH_STYLE)])
        else:
            table_data.append([Paragraph(skill, style=JOB_DETAILS_PARAGRAPH_STYLE)])
        table_styles.append(('TOPPADDING', (0, running_row_index), (1, running_row_index), 1))
        table_styles.append(('BOTTOMPADDING', (0, running_row_index), (1, running_row_index), 0))
        table_styles.append(('SPAN', (0, running_row_index), (1, running_row_index)))
        running_row_index += 1

    if achievements:
        table_data.append([Paragraph("Achievements", SECTION_PARAGRAPH_STYLE)])
        appendSectionTableStyle(table_styles, running_row_index)
        running_row_index += 1

        for achievement in achievements:
            parts = achievement.split(': ', 1)
            if len(parts) == 2:
                heading, skills_list = parts
                table_data.append([Paragraph(f"<b>{heading}</b>: {skills_list}", style=JOB_DETAILS_PARAGRAPH_STYLE)])
            else:
                table_data.append([Paragraph(achievement, style=JOB_DETAILS_PARAGRAPH_STYLE)])
            table_styles.append(('TOPPADDING', (0, running_row_index), (1, running_row_index), 1))
            table_styles.append(('BOTTOMPADDING', (0, running_row_index), (1, running_row_index), 0))
            table_styles.append(('SPAN', (0, running_row_index), (1, running_row_index)))
            running_row_index += 1
    
    if certifications:
        table_data.append([Paragraph("Certifications", SECTION_PARAGRAPH_STYLE)])
        appendSectionTableStyle(table_styles, running_row_index)
        running_row_index += 1

    for certification in certifications:
        parts = certification.split(': ', 1)
        if len(parts) == 2:
            heading, skills_list = parts
            table_data.append([Paragraph(f"<b>{heading}</b>: {skills_list}", style=JOB_DETAILS_PARAGRAPH_STYLE)])
        else:
            table_data.append([Paragraph(certification, style=JOB_DETAILS_PARAGRAPH_STYLE)])
        table_styles.append(('TOPPADDING', (0, running_row_index), (1, running_row_index), 1))
        table_styles.append(('BOTTOMPADDING', (0, running_row_index), (1, running_row_index), 0))
        table_styles.append(('SPAN', (0, running_row_index), (1, running_row_index)))
        running_row_index += 1

    table_style = TableStyle(table_styles)

    table = Table(table_data, colWidths=[FULL_COLUMN_WIDTH * 0.7, FULL_COLUMN_WIDTH * 0.3], spaceBefore=0, spaceAfter=0)
    table.setStyle(table_style)

    elements = [table]

    doc.build(elements)


def move_file(source, destination_dir):
    file_name, file_extension = os.path.splitext(os.path.basename(source))

    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    destination = os.path.join(destination_dir, file_name + file_extension)

    counter = 1
    while os.path.exists(destination):
        new_file_name = f"{file_name}_{counter}{file_extension}"
        destination = os.path.join(destination_dir, new_file_name)
        counter += 1

    shutil.move(source, destination)

def make_resume(ai_client='claude', job: Job = None, user: User = None):
    author = 'Mohith Kailash' if user.full_name is None else user.full_name
    email = 'mohithkailash13@gmail.com' if user.email is None else user.email
    phone = '(951) 569-8009' if user.phone is None else user.phone
    location = 'San Francisco, CA' if user.location is None else user.location
    linkedin_url = 'https://www.linkedin.com/in/mohithkailash/' if user.linkedin_url is None else user.linkedin_url
    github_url = 'https://github.com/mohithkailash' if user.github_url is None else user.github_url
    company_name = 'No name' if job.company_name is None else job.company_name
    role = "Software Engineer" if job.role is None else job.role

    timestamp = int(time.time())
    OUTPUT_PDF_PATH = f"/tmp/{author.lower().replace(' ', '_')}_{timestamp}_resume.pdf"
    JSON_PATH = "./resume_data.json"

    
    
    experience = user.resume.experiences
    skills = user.resume.skills
    summary = user.resume.summary
    education = user.resume.education
    achievements = user.resume.achievements
    certifications = user.resume.certifications
    debug = False
    
    _generate_resume(
        OUTPUT_PDF_PATH,
        JSON_PATH,
        author,
        email,
        phone,
        debug,
        location,
        skills,
        experience,
        summary,
        education,
        linkedin_url,
        github_url,
        achievements,
        certifications
        )


    # moving_path = '/Users/sriramvemparala/Desktop/Resumes/mohith_resumes' + '/' + company_name + '/' + formatted_date + '/' + role
    # moving_path = './resumes'+'/' + author.lower().replace(' ', '_')
    # txt_file_path = moving_path + '/' + 'desc.txt'
    # move_file(OUTPUT_PDF_PATH, moving_path)
    # with open(txt_file_path, 'w') as file:
    #     file.write(job.description)

    print(OUTPUT_PDF_PATH)
    return OUTPUT_PDF_PATH

# if __name__ == "__main__":
#     job_description = """

# The Growth Engineering team focuses on the Signup, Onboarding, Retention experiences for new BILL customers, as well as pricing, product packaging and monetization. The team works closely with the Sales and Marketing teams and optimize the first time experiences for our customers and drive towards directly impacting revenue, unit growth and feature engagement within the product. The team uses Angular/React and Elixir in their day to day development and are heavily focused on building and deploying high quality, high performance features that improve experiences for BILL customers.

# We’d love to chat if you have:

# 3+ years of development experience, or 2+ years of experience with masters in relevant field
# Experience working on large scale, complex applications using Elixir, AWS, Lambda and Event Driven Architecture.
# Experience working with REST API development and GraphQL
# Familiarity with databases (ElasticSearch, MySQL, Oracle or any Cloud DB)
# FrontEnd development using Angular/or React using TypeScript
# Expert level programming knowledge in JavaScript (ES6), including writing cross-browser code, writing testable code
# Web: HTML (5), CSS (3), BootStrap/Foundation
# Other: REST, NodeJS, Application scalability
# Knowledge of best practices & patterns for large scale applications in JavaScript
# Efficient DOM manipulation
# Test Driven Development (TDD) methodology, functional programming style. Playwright or Cypress testing experience a bonus. 

# """

#     config=None
#     debug=False 
#     author="Mohith Kailash"
#     email = "mohithkailash13@gmail.com"
#     phone = "(951)-569-8009"
#     location = "San Francisco, CA"
#     company_name = "Bill.com"
#     role = "Software Engineer"
#     ai_client='claude'
#     api_key = os.getenv(f'{ai_client.upper()}_API_KEY')
    
#     start_time = time.time()
#     make_resume(ai_client, )
#     end_time = time.time()
    
#     execution_time = end_time - start_time
#     logging.info(f'Making resume for {role} at {company_name} at {location} took {execution_time:.2f} seconds')