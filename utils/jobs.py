import streamlit as st
from typing import List, Dict

# Define job portals
PORTALS = [
    {
        "name": "LinkedIn",
        "icon": "🔗",
        "color": "#0A66C2",
        "url": "https://www.linkedin.com/jobs/search/?keywords={}&location={}",
    },
    {
        "name": "Naukri",
        "icon": "🏢",
        "color": "#FF7555",
        "url": "https://www.naukri.com/{}-jobs-in-{}",
    },
    {
        "name": "Foundit (Monster)",
        "icon": "🌐",
        "color": "#5D3FD3",
        "url": "https://www.foundit.in/srp/results?query={}&locations={}",
    },
    {
        "name": "FreshersWorld",
        "icon": "🎓",
        "color": "#003A9B",
        "url": "https://www.freshersworld.com/jobs/jobsearch/{}-jobs-in-{}",
    },
    {
        "name": "TimesJobs",
        "icon": "💼",
        "color": "#003A9B",
        "url": "https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords={}&txtLocation={}",
    },
    {
        "name": "Instahyre",
        "icon": "🧑‍💼",
        "color": "#003A9B",
        "url": "https://www.instahyre.com/{}-jobs-in-{}",
    },
    {
        "name": "Indeed",
        "icon": "💰",
        "color": "#003A9B",
        "url": "https://in.indeed.com/jobs?q={}&l={}",
    }
]

def format_query(s: str) -> str:
    return s.strip().replace(" ", "+")

def search_jobs(job_title: str, location: str) -> List[Dict]:
    job = format_query(job_title)
    loc = format_query(location)

    results = []
    for portal in PORTALS:
        try:
            url = portal["url"].format(job, loc)
            results.append({
                "portal": portal["name"],
                "icon": portal["icon"],
                "color": portal["color"],
                "url": url
            })
        except Exception as e:
            print(f"Error building URL for {portal['name']}: {e}")
    return results

# --- Streamlit UI ---
st.set_page_config(page_title="Job Search Portal", layout="centered")

st.title("🔍 Job Search Links Generator")

job_title = st.text_input("Enter Job Title (e.g., Data Scientist)")
location = st.text_input("Enter Location (e.g., Bangalore)")

if st.button("Generate Links"):
    if job_title and location:
        links = search_jobs(job_title, location)
        st.success(f"Showing job links for **{job_title}** in **{location}**")

        for link in links:
            st.markdown(
                f"""
                <div style="background-color:{link['color']}; padding:10px; border-radius:10px; margin:10px 0;">
                    <h4 style="color:white;">{link['icon']} {link['portal']}</h4>
                    <a href="{link['url']}" target="_blank" style="color:white; text-decoration:underline;">View Jobs</a>
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.warning("Please enter both Job Title and Location.")
