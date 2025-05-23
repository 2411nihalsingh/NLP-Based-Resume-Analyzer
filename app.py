import streamlit as st
from sections import homepage,ats_check,grammer_checker,jobs

st.set_page_config(page_title="Resume Analyzer", layout="wide",page_icon="🤖")

st.sidebar.title("Navigation")
app_mode = st.sidebar.radio("Go to", ["Homepage", "ATS Score Check", "Grammar Checker", "Find Jobs"])

# Page router
if app_mode == "Homepage":
    st.title("You are on homepage")

elif app_mode == "ATS Score Check":
    st.title("You are on Ats page")

elif app_mode == "Grammar Checker":
    st.title("You are on grammer page")

elif app_mode == "Find Jobs":
    st.title("You are on job page")