# Imports, Keys & Model
import os
import streamlit as st
from PyPDF2 import PdfReader

from dotenv import load_dotenv
load_dotenv()

import google.generativeai as genai
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')


# PDF to Text
def pdf_to_text(pdf_file):
    pdf_reader = PdfReader(pdf_file)
    full_text = ''
    for page in pdf_reader.pages:
        full_text += page.extract_text()
        full_text += ' '
    
    return full_text

# Report - Scores
def get_scores(resume, job_description, type):

    prompt = f"""
    You are an AI designed analyze resumes based on various parameters 
    and check their compatibilty and chances of selection with the given job description.

    Now, One candidate is applying for a {type} with the following job description and his resume is given below.
    Analyze the resume based on suitable parameters that are required for a typical job in the given job description and also this particular job description.

    Check for parameters like:
    - Clarity in langugae of resume, mentioning skills, mentioning education, 
    mentioning relevant courses, soft-skills and adding projects.


    Analyze the resume thorouhgly and match it's compatibilty against job description,
    give three scores out of 100, where 0 represents least chances and 100 represents highest chances.
        - Clarity & Coherence
        - ATS friendliness
        - Chances of selection


        This is the Resume: {resume}
        This is the Job Description: {job_description}


    Your output must be a text where three scores are seperated by space
    Sample output pattern: 50 70 75
    """

    response = model.generate_content(prompt).text
    clarity_score, ATS_score, selection_chances = map(str, response.split())
    return clarity_score, ATS_score, selection_chances

# Report - Detailed Feedback
def get_report(resume, job_description, type):

    prompt = f"""
    You are an AI designed analyze resumes based on various parameters 
    and check their compatibilty and chances of selection with the given job description.

    Now, One candidate is applying for a {type} with the following job description and his resume is given below.
    Analyze the resume based on suitable parameters that are required for a typical job in the given job description and also this particular job description.

    Check for parameters like:
    - Clarity in langugae of resume, mentioning skills, mentioning education, 
    mentioning relevant courses, soft-skills and adding projects.
    - Use industry-relevant parameters that are used to asses resumes.
    - Use algorithms or parameters that are used in ATS in organizations, etc.

    Analyze the resume thorouhgly and match it's compatibilty against job description,
    and give a detailed report on the resume using followin points:
    - Clarity & Coherence of resume content (If resume has too little/ too much info, etc.)
    - Highlights on Skills, Experience & education against compatibilty with the Job description

    And lastly, givr detailed Actionale recommendations that can be implemented and practiced to improve resume ultimately,
    increasing chances of selection.

    Here is the resume & job description:
    Resume: {resume}
    Job Description: {job_description}

    Your output must be in following format:

    Firstly, give a report in tabular format (Requirements vs Your Resume) 
    that compares similarities and dissimilarities in Requirements in job description vs content in resume, 
    Put a green tick in Your Resume column where match and red cross where unmatch nad put a exclamation mark where you are uncertain.
    (Properly check everything, for e.g: Education requirements/ skills, if anything special is required in description which is not resume and you are uncertain, put an exclaimation mark.)

    Clarity & Coherence
        Pros:
        Cons:

    Skills & Experience
        Pros:
    Cons:

    Actionable Recommendations
    (Bulllet points)
"""

    response = model.generate_content(prompt).text
    return response

# Cover Letter
def get_cover_letter(resume, job_description, type, position_name, company_name):
    prompt = f"""
            You are an AI designed to write a cover letter for a {type} application.
            I have provided you with the my resume, the job description that I am applying to.

            My Resume: {resume}
            Job Description: {job_description}
            Opportunity (Position): {position_name}
            Company Name: {company_name}

            You have to understand the job description, their requirements and write a appealing cover letter that shows why I am the best fit fo their job,
            while writing you have to seem like that I am much eager and give importance to this opportunity, and not sound like an AI/Machine, sound natural and more human.

            You have to write a professional cover letter that I will use to improve my chances at selection.
            Include following things in the cover letter:
            - My Experience that is related and helpful to job description
            - My Skills that are related and helpful to job description
            - I am a fast learner, adaptive and a team-worker, etc. (use your creativity and add more points)
            """
    response = model.generate_content(prompt).text
    return response