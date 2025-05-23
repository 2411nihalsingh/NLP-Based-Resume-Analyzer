import streamlit as st
from sections import homepage,ats_check,grammer_checker,jobs

st.set_page_config(page_title="Resume Analyzer", layout="wide",page_icon="🤖")

st.sidebar.button("Admin Login")

st.sidebar.title("Navigation")
app_mode = st.sidebar.selectbox("Go to", ["Homepage", "ATS Score Check", "Grammar Checker", "Find Jobs"])

# Page router
if app_mode == "Homepage":
    homepage.run()

elif app_mode == "ATS Score Check":
    st.title("You are on Ats page")

elif app_mode == "Grammar Checker":
    grammer_checker.run()

elif app_mode == "Find Jobs":
    jobs.run()