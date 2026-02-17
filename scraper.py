import requests
from bs4 import BeautifulSoup
import time
import random
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
logger = logging.getLogger("JobScraper")

class JobScraper:
    """
    Scraper designed to extract job titles and descriptions from web sources.
    Note: In a production environment, respect robots.txt and use rate limiting.
    """
    def __init__(self, base_url: str = None):
        self.base_url = base_url or "https://realpython.github.io/fake-jobs/" # Using a safe scraping practice site
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def fetch_jobs(self):
        """Fetches job listings from the target URL."""
        logger.info(f"Starting scrape on {self.base_url}...")
        try:
            response = requests.get(self.base_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.text
        except Exception as e:
            logger.error(f"Failed to fetch data: {e}")
            return None

    def parse_jobs(self, html_content):
        """Parses HTML content to extract job details."""
        if not html_content:
            return []

        soup = BeautifulSoup(html_content, "html.parser")
        results = soup.find(id="ResultsContainer")
        if not results:
            logger.error("ResultsContainer not found in HTML.")
            return []
            
        job_elements = results.find_all("div", class_="card-content")


        jobs_list = []
        for job_element in job_elements:
            title = job_element.find("h2", class_="title").text.strip()
            company = job_element.find("h3", class_="company").text.strip()
            location = job_element.find("p", class_="location").text.strip()
            
            # Identify skills based on title keyword simulation
            detected_skills = []
            lower_title = title.lower()
            if 'python' in lower_title or 'data' in lower_title: detected_skills += ['Python', 'Pandas', 'SQL']
            if 'developer' in lower_title: detected_skills += ['JavaScript', 'React', 'Docker']
            if 'engineer' in lower_title: detected_skills += ['AWS', 'Java', 'Kubernetes']
            if 'manager' in lower_title: detected_skills += ['Azure', 'Full Stack']
            
            jobs_list.append({
                "title": title,
                "company": company,
                "location": location,
                "description": f"Seeking a {title} with skills in: {', '.join(detected_skills) or 'Python, SQL'}"
            })
        
        logger.info(f"Successfully parsed {len(jobs_list)} jobs.")
        return jobs_list

    async def discovery_stream(self, jobs_batch):
        """Asynchronous generator to simulate real-time discovery of jobs."""
        for job in jobs_batch:
            # Simulate network/discovery latency
            await asyncio.sleep(random.uniform(0.1, 0.4))
            yield job

