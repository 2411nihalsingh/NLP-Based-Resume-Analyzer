import streamlit as st
from sections import grammar_checker, homepage,ats_check,jobs,admin_panel

st.set_page_config(page_title="Resume Analyzer", layout="wide",page_icon="🤖")

admin_button = st.sidebar.button("Admin Login")

if not admin_button:
     
    st.sidebar.title("Navigation")
    app_mode = st.sidebar.selectbox("Go to", ["Homepage", "ATS Score Check", "Grammar Checker", "Find Jobs"])

    # Page router
    if app_mode == "Homepage":
        homepage.run()

    elif app_mode == "ATS Score Check":
        ats_check.run()

    elif app_mode == "Grammar Checker":
        grammar_checker.run()

    elif app_mode == "Find Jobs":
        jobs.run()
    
else:
   return_button = st.sidebar.button("return")
   if(return_button):
       homepage.run()
   admin_panel.run()
