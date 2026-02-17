import streamlit as st
import pandas as pd
import plotly.express as px
from scraper import JobScraper
from analyzer import JobAnalyzer
import time
import asyncio

# Page Config
st.set_page_config(page_title="Job Market Insights", page_icon="🕷️", layout="wide")

st.title("🕷️ Real-Time Job Market Analyzer")
st.markdown("Extracting and analyzing technical skill trends from live job postings.")

# Sidebar
with st.sidebar:
    st.header("⚙️ Scraper Settings")
    url_option = st.selectbox("Select Target", ["Fake Jobs Demo (Safe)", "Custom URL (Requires Setup)"])
    if url_option == "Custom URL (Requires Setup)":
        st.warning("Note: Scraping real sites may require rotating proxies and headers.")
    
    scrape_button = st.button("🚀 Start Scraping", type="primary")

# UI Placeholders
metrics_col1, metrics_col2 = st.columns(2)
total_count = metrics_col1.empty()
status_msg = metrics_col2.empty()

progress_bar = st.progress(0)

chart_col, log_col = st.columns([2, 1])
chart_area = chart_col.empty()
log_area = log_col.empty()

def run_streamlit_flow():
    scraper = JobScraper()
    
    # 1. Fetching
    with st.spinner("Fetching job listings..."):
        html = scraper.fetch_jobs()
        if not html:
            st.error("Failed to fetch data.")
            return

    # 2. Parsing (Streaming visualization)
    status_msg.info("Step 1: Parsing HTML and extracting jobs...")
    jobs = scraper.parse_jobs(html)
    total_count.metric("Jobs Found", len(jobs))
    
    # Simulate a "streaming" feel for parsing
    log_content = []
    for i, job in enumerate(jobs[:20]): # Show first 20 in logs for performance
        log_content.append(f"✅ Extracted: {job['title']} @ {job['company']}")
        log_area.code("\n".join(log_content[-15:]))
        progress_bar.progress(min((i + 1) / len(jobs), 0.5))
        time.sleep(0.05)

    # 3. Analyzing
    status_msg.info("Step 2: Running Skill Frequency Analysis...")
    analyzer = JobAnalyzer(jobs)
    skills = analyzer.extract_skills()
    summary = analyzer.get_summary()
    
    progress_bar.progress(1.0)
    status_msg.success("Analysis Complete!")

    # 4. Display Charts
    if skills:
        df_skills = pd.DataFrame(list(skills.items()), columns=['Skill', 'Mentions'])
        df_skills = df_skills[df_skills['Mentions'] > 0].head(12)
        
        fig = px.bar(
            df_skills, 
            x='Mentions', 
            y='Skill', 
            orientation='h',
            title='Top Trending Skills',
            color='Mentions',
            color_continuous_scale='Viridis',
            template='plotly_dark'
        )
        fig.update_layout(yaxis={'categoryorder':'total ascending'})
        chart_area.plotly_chart(fig, use_container_width=True)

    # Summary Stats
    st.subheader("📍 Job Distribution")
    col1, col2 = st.columns(2)
    
    df_loc = pd.DataFrame(list(summary['top_locations'].items()), columns=['Location', 'Count'])
    fig_loc = px.pie(df_loc, values='Count', names='Location', title='Jobs by Location', template='plotly_dark')
    col1.plotly_chart(fig_loc, use_container_width=True)

    df_comp = pd.DataFrame(list(summary['top_companies'].items()), columns=['Company', 'Count'])
    fig_comp = px.bar(df_comp, x='Count', y='Company', title='Top Hiring Companies', template='plotly_dark')
    col2.plotly_chart(fig_comp, use_container_width=True)

if scrape_button:
    run_streamlit_flow()
else:
    st.info("Click 'Start Scraping' in the sidebar to begin the market analysis.")
    st.image("https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&q=80&w=1200", caption="Data-Driven Career Strategy")
