import streamlit as st

# 1. MANDATORY: This must be the absolute first Streamlit command.
st.set_page_config(page_title="Job Market Insights", page_icon="🕷️", layout="wide")

import sys
import traceback
import pandas as pd
import plotly.express as px
import requests
import time

# 2. FAIL-SAFE IMPORTS
try:
    from bs4 import BeautifulSoup
    from scraper import JobScraper
    from analyzer import JobAnalyzer
except Exception as e:
    st.error("🚨 CRITICAL BOOT ERROR: Could not import project modules.")
    st.code(traceback.format_exc())
    st.stop()

# 3. UI HEADER
st.title("🕷️ Job Market Analyzer v2.2")
st.markdown("Analyzing technical skill trends in real-time.")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    url_option = st.selectbox("Source", ["Demo Site (Safe)"])
    scrape_button = st.button("🚀 Start Analysis", use_container_width=True)
    
    st.divider()
    if st.button("📝 Show System Health"):
        st.write(f"Python: {sys.version.split()[0]}")
        st.write(f"Streamlit: {st.__version__}")
        st.write("File Structure: OK")

# UI Placeholders
m1, m2 = st.columns(2)
total_count = m1.empty()
status_msg = m2.empty()
progress_bar = st.progress(0)

chart_area = st.empty()
log_area = st.empty()

def run_flow():
    try:
        scraper = JobScraper()
        
        # Step 1: Fetch
        with st.spinner("Connecting to source..."):
            html = scraper.fetch_jobs()
            if not html:
                st.error("Connection failed.")
                return

        # Step 2: Parse
        status_msg.info("Parsing data...")
        jobs = scraper.parse_jobs(html)
        
        if not jobs:
            st.warning("No listings found.")
            return

        total_count.metric("Total Jobs Found", len(jobs))
        
        # Step 3: Analyze
        status_msg.info("Analyzing skills...")
        analyzer = JobAnalyzer(jobs)
        skills = analyzer.extract_skills()
        summary = analyzer.get_summary()
        
        progress_bar.progress(1.0)
        status_msg.success("Analysis Complete!")

        # Step 4: Visualize
        if any(skills.values()):
            df_skills = pd.DataFrame(list(skills.items()), columns=['Skill', 'Mentions'])
            df_skills = df_skills[df_skills['Mentions'] > 0].sort_values(by='Mentions', ascending=True)
            
            fig = px.bar(
                df_skills, 
                x='Mentions', 
                y='Skill', 
                orientation='h',
                title='Skill Popularity',
                template='plotly_dark',
                color_discrete_sequence=['#00CC96']
            )
            chart_area.plotly_chart(fig, use_container_width=True)
        
        # Secondary Stats
        st.divider()
        c1, c2 = st.columns(2)
        if summary['top_locations']:
            df_loc = pd.DataFrame(list(summary['top_locations'].items()), columns=['Loc', 'Val'])
            c1.plotly_chart(px.pie(df_loc, values='Val', names='Loc', title='Locations', template='plotly_dark'), use_container_width=True)
        if summary['top_companies']:
            df_comp = pd.DataFrame(list(summary['top_companies'].items()), columns=['Comp', 'Val'])
            c2.plotly_chart(px.bar(df_comp, x='Val', y='Comp', title='Companies', template='plotly_dark'), use_container_width=True)

    except Exception as e:
        st.error(f"Error during execution: {e}")
        st.code(traceback.format_exc())

if scrape_button:
    run_flow()
else:
    st.info("Click 'Start Analysis' to begin.")
