import pytest
from pathlib import Path
from res_maker import make_resume
from Models.job import Job
from Models.resume import Resume
from Models.user import User

def test_make_resume(sample_output_path):
    """Test resume generation with sample data"""
    # Create Job object
    job = Job(
        description="Wells Fargo is seeking a Software Engineer...",  # truncated for brevity
        location="San Francisco, CA",
        role="Software Engineer",
        company_name="Wells Fargo"
    )

    # Create Resume object with all the data
    resume = Resume(
        skills=[
            "Programming Language: Java, Python, JavaScript, SQL, Apex",
            "Frameworks and Databases: Salesforce, nCino, Spring, MongoDB, PostgreSQL",
            "Cloud Technologies: AWS Lambda, Azure, Docker",
            "Other Technologies: Agile, Scrum, Git, JIRA, Data Structures, Algorithms, Software Design"
        ],
        experiences=[
            {
                "company": "Pricing Minds, LLC",
                "description": [
                    "Designed and implemented efficient data migration solutions using Salesforce platform, resulting in a 30% improvement in data processing speed for enterprise clients",
                    "Developed and configured complex integrations using Apache Camel and Salesforce APIs, enhancing system interoperability and reducing manual data entry by 40%",
                    "Utilized Agile methodologies to deliver user stories and POCs, presenting demos to stakeholders and achieving a 95% client satisfaction rate",
                    "Collaborated with cross-functional teams to identify opportunities for service quality improvements, resulting in a 20% reduction in system downtime"
                ],
                "duration": "May 2023 - Present",
                "location": "San Jose, CA",
                "title": "Software Development Engineer"
            },
            {
                "company": "Eunimart Multichannel Pvt Ltd",
                "description": [
                    "Led the development of a Salesforce-integrated AI assistant, reducing customer inquiry response time by 25% and improving overall user satisfaction",
                    "Designed and implemented a scalable web crawler architecture, processing over 500 data entries per second, to support data-driven decision making in Salesforce",
                    "Developed and deployed attention models for product prediction, integrating with Salesforce platform to enhance marketplace competition research capabilities",
                    "Spearheaded the implementation of an image optimization feature, reducing expenses for SMEs by 1.5x and streamlining product catalog management in Salesforce",
                    "Engineered cloud computing integrations using webhooks and Flask APIs, improving system reliability and reducing data synchronization issues by 35%",
                    "Mentored 2 interns, participated in recruitment processes, and delivered 12+ demos on Salesforce implementation, enhancing team knowledge and productivity"
                ],
                "duration": "Jun 2019 - Jul 2021",
                "location": "Hyderabad, India",
                "title": "Software Development Engineer"
            }
        ],
        education=[
            {
                "degree": "Master of Science, Computer Science",
                "location": "Riverside, CA",
                "university": "University of California, Riverside",
                "year": "May 2023"
            },
            {
                "degree": "Bachelors of Technology, Computer Science",
                "location": "Vijayawada, India",
                "university": "KL University",
                "year": "May 2021"
            }
        ],
        achievements=[],
        certifications=[
            "Pricefx Certified Integration Engineer",
            "Pricefx Certified Configuration Engineer",
            "Certificate of Merit on Android Application Development with 97 percent from IIT Roorkee",
            "Certificate of Merit in C Language and Data Structures with 95 percent from IIT Roorkee"
        ],
        summary="Seasoned Software Engineer with 3+ years of experience specializing in Salesforce platform development and integration. Proficient in Java, Python, and JavaScript, with a strong background in designing and implementing efficient data migration solutions, resulting in a 30% improvement in processing speed. Demonstrated expertise in Agile methodologies, cloud technologies, and cross-functional collaboration, consistently delivering high-quality solutions with a 95% client satisfaction rate. Adept at leveraging Salesforce APIs and nCino to enhance system interoperability and streamline business processes, making a strong fit for Wells Fargo's Consumer Technology team in Small Business Lending."
    )

    # Create User object
    user = User(
        first_name="Srinivasa",
        last_name="Biradavolu",
        email="sbira001@ucr.edu",
        phone="+1(951)-569-8009",
        location="San Francisco, CA",
        linkedin_url="https://www.linkedin.com/in/bskarthikk/",
        github_url="",
        resume=resume
    )

    # Call make_resume with the created objects
    result_path = make_resume(
        ai_client='claude',
        job=job,
        user=user
    )

    # Add more detailed logging
    print(f"\nGenerated resume path: {result_path}")
    if Path(result_path).exists():
        print(f"Directory contents: {list(Path(result_path).glob('*'))}")
    else:
        print("Warning: Generated path does not exist!")

    assert Path(result_path).exists()
    assert Path(result_path).is_dir()
    
    # Check if PDF was generated in the directory
    pdf_files = list(Path(result_path).glob("*.pdf"))
    assert len(pdf_files) > 0

def test_make_resume_2(sample_output_path):
    """Test resume generation with sample data"""
    # Create Job object
    job = Job(
        description="Wells Fargo is seeking a Software Engineer...",  # truncated for brevity
        location="San Francisco, CA",
        role="Software Engineer",
        company_name="Wells Fargo"
    )

    # Create Resume object with all the data
    resume = Resume(
        skills={
            "skills": [
                "Programming Language: Java, Go, NodeJS, Python, SQL, C++, JavaScript",
                "Frameworks and Databases: AWS DynamoDB, React.js, Node.js, PostgreSQL, MySQL, Flask, Spring",
                "Cloud Technologies: AWS Lambda, AWS ECS, AWS EC2, AWS APIGateway, AWS CloudWatch, GCP, Azure",
                "Other Technologies: Agile, Git, Docker, Rest, Postman, JIRA, Continuous Deployment"
            ]
        },
        experiences=[
            {
            "title": "Software Development Engineer",
            "company": "ServiceNow",
            "location": "Remote",
            "duration": "Jul 2023 - Present",
            "description": [
                "Developed a dynamic pricing model with React.js and ES6+, employing adaptive pricing strategies achieving a 10% revenue increase. Utilized Sass for advanced styling, ensuring a robust and responsive UI/UX design.",
                "Refined the front-end architecture using React.js, cutting page load times by 20%. Applied asynchronous data loading with Axios for RESTful API calls and boosting backend performance by 30% with Spring Boot MVC and Java.",
                "Integrated third-party APIs and microservices with Java and Spring Boot MVC techniques, boosting application functionality and user engagement by 25%.",
                "Troubleshot and resolved critical bugs, improving application stability and reliability, which led to a 15% reduction in support tickets. Employed Git for version control, promoting efficient issue tracking and resolution.",
                "Architected reusable and modular JavaScript components, using React.js leading to a 40% improvement in code maintainability and a 30% faster development cycle for new features.",
                ]
            },
            {
            "title": "Software Development Engineer",
            "company": "Neon IT Systems",
            "location": "Hyderabad, India",
            "duration": "Jan 2020 - Nov 2021",
            "description": [
                "Devised a SQL and Python-powered financial model, integrated RESTful APIs for real-time analytics on critical KPI’s, elevating finance department efficiency by 25% through seamless data processing.",
                "Optimized financial data processing and integration with asynchronous programming in Java/Spring Boot MVC, reducing data retrieval times by 40% and managing large financial datasets effectively.",
                "Implemented Docker and Kubernetes for deploying microservices on AWS, ensuring high availability and scalability, thereby creating a robust infrastructure capable of handling peak load with ease.",
                "Employed advanced data visualization and RESTful API integration in the dashboard, significantly enhancing the clarity and accessibility of financial reports."
                ]
            }
        ],
        education=[
            {
                "degree": "Master of Science, Computer Science",
                "location": "Tempe, AZ",
                "university": "Arizona State University",
                "year": "Dec 2023"
            },
            {
                "degree": "Bachelors of Technology, Mechanical Engineering",
                "location": "Hyderabad, India",
                "university": "BITS Pilani University",
                "year": "May 2020"
            }
        ],
        achievements=[],
        certifications=[],
        summary={
            "summary": """Seasoned Software Engineer with 4 years of experience specializing in Salesforce development, including
            expertise in Apex, Lightning Web Components, and nCino. Demonstrated success in optimizing Salesforce
            platform performance, reducing page load times by 20%, and implementing dynamic pricing models resulting in
            a 10% revenue increase. Proficient in Agile methodologies, CI/CD pipelines, and integrating third-party APIs,
            with a track record of enhancing application functionality and user engagement by 25%"""
        }
    )

    # Create User object
    user = User(
        first_name="ViswaTeja",
        last_name="Bapireddy",
        email="viswab2000@gmail.com",
        phone="+1(602)-341-3436",
        location="San Francisco, CA",
        linkedin_url="",
        github_url="",
        resume=resume
    )

    # Call make_resume with the created objects
    result_path = make_resume(
        ai_client='claude',
        job=job,
        user=user
    )

    # Add more detailed logging
    print(f"\nGenerated resume path: {result_path}")
    if Path(result_path).exists():
        print(f"Directory contents: {list(Path(result_path).glob('*'))}")
    else:
        print("Warning: Generated path does not exist!")

    # assert Path(result_path).exists()
    # assert Path(result_path).is_dir()
    
    # Check if PDF was generated in the directory
    # pdf_files = list(Path(result_path).glob("*.pdf"))
    # assert len(pdf_files) > 0

def test_make_resume_invalid_input():
    """Test resume generation with invalid input"""
    with pytest.raises(Exception):
        make_resume(
            job_description=None,
            config=None,
            debug=False,
            author=None,
            email=None,
            phone=None,
            location=None,
            company_name=None,
            role=None
        ) 