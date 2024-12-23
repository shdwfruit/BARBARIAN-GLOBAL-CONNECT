import streamlit as st
import requests

# Set page configuration
st.set_page_config(page_title="Decision Maker Dashboard", layout="wide")

# Page Title
st.title("Decision Maker Dashboard")
st.write("**Welcome, Dr. Smith!**")
st.divider()

# Navigation Sidebar
from modules.nav import SideBarLinks
SideBarLinks(show_home=True)

# Create buttons for navigation
st.subheader("Navigate to:")

if st.button("Student Engagement Insights", type="primary"):
    st.switch_page("pages/Student_Engagement_Insights.py")
    
if st.button("Progress Visualization", type="primary"):
    st.switch_page("pages/Progress_Visualization.py")
    
if st.button("Feedback Analysis", type="primary"):
    st.switch_page("pages/Feedback_Analysis.py")
    
if st.button("Cultural Competence Trends", type="primary"):
    st.switch_page("pages/Cultural_Competence_Trends.py")

# Divider
st.divider()

# Report an issue section
st.subheader("Report an issue")
description = st.text_area("Description (Functional, Visual, etc.)")
status = st.radio("Current Status", 
                  ["Active", "Inactive"])
reported_by = st.session_state['id']
if st.button('Report Issue'):
    if not description:
        st.error("Please enter a description")
    elif not status:
        st.error("Please choose a status")
    else:
        data = {
            "reported_by": reported_by,
            "status": status,
            "description": description
        }
        
        try:
            response = requests.post('http://api:4000/ir/report_issue', json=data)
            if response.status_code == 200:
                st.success("Issue successfully reported!")
                st.balloons()
            else:
                st.error("Error reporting issue")
        except Exception as e:
            st.error(f"Error connecting to server: {str(e)}")