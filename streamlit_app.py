import streamlit as st

# 1. MANDATORY: This must be the absolute first Streamlit command.
st.set_page_config(page_title="Job Market Insights", page_icon="🕷️", layout="wide")

import sys
import traceback
import pandas as pd
import plotly.express as px
import requests
import time
import asyncio
import random
from scraper import JobScraper

from analyzer import JobAnalyzer

# 2. STATE INITIALIZATION
if 'all_jobs' not in st.session_state:
    st.session_state.all_jobs = []
if 'is_streaming' not in st.session_state:
    st.session_state.is_streaming = False

# 3. UI HEADER
st.title("🕷️ Job Market Analyzer v3.0 (Live Stream)")
st.markdown("Analyzing technical skill trends from live job postings in real-time.")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    mode = st.radio("App Mode", ["One-Time Scrape", "Live Data Stream"])
    
    col1, col2 = st.columns(2)
    start_btn = col1.button("🚀 Start", use_container_width=True, type="primary")
    stop_btn = col2.button("🛑 Stop", use_container_width=True)
    
    if stop_btn:
        st.session_state.is_streaming = False
        st.rerun()

    st.divider()
    if st.button("🧹 Clear Data"):
        st.session_state.all_jobs = []
        st.rerun()

# UI Placeholders
m1, m2, m3 = st.columns(3)
total_count = m1.empty()
status_msg = m2.empty()
throughput = m3.empty()

progress_bar = st.progress(0)

chart_area = st.empty()
log_area = st.empty()

def update_visuals(jobs_list):
    """Refreshes charts and statistics based on current data."""
    if not jobs_list:
        return

    analyzer = JobAnalyzer(jobs_list)
    skills = analyzer.extract_skills()
    summary = analyzer.get_summary()

    total_count.metric("Total Jobs Indexed", len(jobs_list))
    
    # Update Chart
    if any(skills.values()):
        df_skills = pd.DataFrame(list(skills.items()), columns=['Skill', 'Mentions'])
        df_skills = df_skills[df_skills['Mentions'] > 0].sort_values(by='Mentions', ascending=True).tail(12)
        
        if not df_skills.empty:
            fig = px.bar(
                df_skills, 
                x='Mentions', 
                y='Skill', 
                orientation='h',
                title='🔥 Live Skill Popularity',
                template='plotly_dark',
                color='Mentions',
                color_continuous_scale='Turbo'
            )
            chart_area.plotly_chart(fig, use_container_width=True)

async def run_live_stream():
    st.session_state.is_streaming = True
    scraper = JobScraper()
    
    status_msg.info("📡 Connecting to live job seed...")
    html = scraper.fetch_jobs()
    if not html:
        st.error("Connection failed.")
        return
    
    seed_jobs = scraper.parse_jobs(html)
    random.shuffle(seed_jobs) # Mix them up for better "scrolling" feel
    
    status_msg.success("Live Feed Active")
    log_content = []
    start_time = time.time()
    
    # Iterate through discovery stream
    async for job in scraper.discovery_stream(seed_jobs):
        if not st.session_state.is_streaming:
            break
            
        # Add to state
        st.session_state.all_jobs.append(job)
        
        # Update logs
        log_content.append(f"⏱️ {time.strftime('%H:%M:%S')} | Found: {job['title']} @ {job['company']}")
        log_area.code("\n".join(log_content[-10:]))
        
        # Performance metrics
        elapsed = time.time() - start_time
        tp = len(st.session_state.all_jobs) / elapsed if elapsed > 0 else 0
        throughput.metric("Stream Speed", f"{tp:.1f} jobs/s")
        
        # Refresh visuals every few jobs
        if len(st.session_state.all_jobs) % 2 == 0:
            update_visuals(st.session_state.all_jobs)
            progress_bar.progress(min(len(st.session_state.all_jobs) / len(seed_jobs), 1.0))
        
        # Yield to allow UI interactions (though Streamlit async is limited)
        await asyncio.sleep(0.01)

def run_one_time():
    scraper = JobScraper()
    with st.spinner("Analyzing current market state..."):
        html = scraper.fetch_jobs()
        if html:
            jobs = scraper.parse_jobs(html)
            st.session_state.all_jobs = jobs
            update_visuals(jobs)
            status_msg.success("Snapshot Complete")

# MAIN EXECUTION
if start_btn:
    if mode == "Live Data Stream":
        asyncio.run(run_live_stream())
    else:
        run_one_time()
elif st.session_state.is_streaming:
    # If it was streaming, keep going (this pattern is tricky in vanilla Streamlit)
    asyncio.run(run_live_stream())
else:
    if not st.session_state.all_jobs:
        st.info("System Idle. Select 'Live Data Stream' and click 'Start' to see the engine in action.")
        st.image("https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&q=80&w=1200", caption="Real-Time Data Intelligence")
    else:
        update_visuals(st.session_state.all_jobs)
