# Imports
import streamlit as st
import time
from func import pdf_to_text, get_scores, get_report, get_cover_letter


# Page Setup
st.set_page_config(
    page_title='CheckCV',
    # page_icon= 'res/logo.png',
    layout='wide',
)
st.title('CheckCV: An AI Resume Companion')


# Main Inputs
resume = st.file_uploader('Resume', type='pdf')
job_description = st.text_area('Job Description')
col1, col2, col3 = st.columns(3)
with col1:
    company_name = st.text_input('Company Name')
with col2:
    position_name = st.text_input('Position Name')
with col3:
    type = st.radio('Position', ['Job', 'Internship'], horizontal=True)


# Buttons
col1, col2, col3 = st.columns(3)
with col2:
    col1, col2 = st.columns(2)
    with col1:
        button = st.button('Resume Report')
    with col2:
        letter_button = st.button('Cover Letter')

# Display Report
if button:
    if (resume is not None) and (job_description is not None):

        progress_bar = st.progress(0)

        resume = pdf_to_text(resume)
        progress_bar.progress(33) 

        clarity_score, ATS_score, selection_chances = get_scores(resume, job_description, type)
        progress_bar.progress(66) 

        resume_report = get_report(resume, job_description, type)
        progress_bar.progress(100)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.header('Clarity')
            st.title(clarity_score)

        with col2:
            st.header('ATS Compatibility')
            st.title(ATS_score)

        with col3:
            st.header('Selection Chances')
            st.title(f'{selection_chances}%')

        st.write(resume_report)

# Display Cover Letter
if letter_button:  
    progress_bar = st.progress(0)
    cover_letter = get_cover_letter(resume, job_description, type, position_name, company_name)
    progress_bar.progress(50)
    time.sleep(2)
    progress_bar(100)
    st.write(cover_letter)