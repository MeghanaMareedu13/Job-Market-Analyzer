import streamlit as st
import sys
import traceback

# 1. CRITICAL BOOT CHECK
# We wrap everything in a try-except at the top level to catch import/syntax errors
try:
    import pandas as pd
    import plotly.express as px
    import requests
    from bs4 import BeautifulSoup
    import time
    from scraper import JobScraper
    from analyzer import JobAnalyzer
except Exception as e:
    st.error("🚨 CRITICAL BOOT ERROR: A dependency is missing or failing.")
    st.code(traceback.format_exc())
    st.stop()

# 2. Page Config (Must be first Streamlit command)
st.set_page_config(page_title="Job Market Insights", page_icon="🕷️", layout="wide")

st.title("🕷️ Real-Time Job Market Analyzer (v2.1)")
st.markdown("Extracting and analyzing technical skill trends from live job postings.")

# Sidebar
with st.sidebar:
    st.header("⚙️ Scraper Settings")
    url_option = st.selectbox("Select Target", ["Fake Jobs Demo (Safe)", "Custom URL (Requires Setup)"])
    scrape_button = st.button("🚀 Start Scraping", type="primary")
    
    st.divider()
    st.info("Debugging Info:")
    st.write(f"Python Version: {sys.version.split()[0]}")
    st.write(f"Streamlit Version: {st.__version__}")

# UI Placeholders
metrics_col1, metrics_col2 = st.columns(2)
total_count = metrics_col1.empty()
status_msg = metrics_col2.empty()

progress_bar = st.progress(0)

chart_col, log_col = st.columns([2, 1])
chart_area = chart_col.empty()
log_area = log_col.empty()

def run_streamlit_flow():
    try:
        scraper = JobScraper()
        
        # 1. Fetching
        with st.spinner("Fetching data..."):
            html = scraper.fetch_jobs()
            if not html:
                st.error("Failed to fetch data from the source. Source might be down or blocking the request.")
                return

        # 2. Parsing
        status_msg.info("Step 1: Parsing HTML...")
        jobs = scraper.parse_jobs(html)
        
        if not jobs:
            total_count.metric("Jobs Found", 0)
            st.warning("No jobs were found. The website structure might have changed.")
            return

        total_count.metric("Jobs Found", len(jobs))
        
        # Simulated log "stream"
        log_content = []
        max_logs = min(len(jobs), 20)
        for i in range(max_logs):
            job = jobs[i]
            log_content.append(f"✅ Found: {job['title']} @ {job['company']}")
            log_area.code("\n".join(log_content[-10:]))
            # Safe progress
            prog = 0.1 + (i / max_logs) * 0.4
            progress_bar.progress(prog)
            time.sleep(0.05)

        # 3. Analyzing
        status_msg.info("Step 2: Analyzing Skills...")
        analyzer = JobAnalyzer(jobs)
        skills = analyzer.extract_skills()
        summary = analyzer.get_summary()
        
        progress_bar.progress(1.0)
        status_msg.success("Analysis Complete!")

        # 4. Display Charts
        if any(skills.values()):
            df_skills = pd.DataFrame(list(skills.items()), columns=['Skill', 'Mentions'])
            df_skills = df_skills[df_skills['Mentions'] > 0].sort_values(by='Mentions', ascending=True).tail(10)
            
            if not df_skills.empty:
                fig = px.bar(
                    df_skills, 
                    x='Mentions', 
                    y='Skill', 
                    orientation='h',
                    title='Top 10 Trending Skills',
                    color='Mentions',
                    color_continuous_scale='Bluered_r',
                    template='plotly_dark'
                )
                chart_area.plotly_chart(fig, use_container_width=True)
        else:
            chart_area.warning("No tracked skills found in job descriptions.")

        # Distribution UI
        st.subheader("📍 Insights Summary")
        c1, c2 = st.columns(2)
        
        if summary['top_locations']:
            df_loc = pd.DataFrame(list(summary['top_locations'].items()), columns=['Location', 'Total'])
            fig_loc = px.pie(df_loc, values='Total', names='Location', title='Opening Distribution', template='plotly_dark')
            c1.plotly_chart(fig_loc, use_container_width=True)
        
        if summary['top_companies']:
            df_comp = pd.DataFrame(list(summary['top_companies'].items()), columns=['Company', 'Openings'])
            fig_comp = px.bar(df_comp, x='Openings', y='Company', title='Active Companies', template='plotly_dark')
            c2.plotly_chart(fig_comp, use_container_width=True)
            
    except Exception as e:
        st.error(f"Execution Error: {str(e)}")
        st.code(traceback.format_exc())

if scrape_button:
    run_streamlit_flow()
else:
    st.info("Ready. Click 'Start Scraping' to analyze the current market trends.")
    # Fallback visual
    st.markdown("""
    ---
    ### 📊 What this analyzer looks for:
    - **Cloud**: AWS, Azure, GCP
    - **Data**: SQL, Pandas, Spark, Tableau
    - **Dev**: Python, Java, JavaScript, React, Docker
    - **Emerging**: AI, Machine Learning, FastAPI
    """)
