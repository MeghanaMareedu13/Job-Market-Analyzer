import pandas as pd
import re
from collections import Counter
import logging

logger = logging.getLogger("JobAnalyzer")

class JobAnalyzer:
    """
    Analyzes job descriptions to find trending technical skills.
    """
    def __init__(self, jobs_data):
        self.df = pd.DataFrame(jobs_data)
        self.skills_to_track = [
            'Python', 'SQL', 'Java', 'JavaScript', 'React', 'AWS', 'Azure', 
            'GCP', 'Docker', 'Kubernetes', 'Pandas', 'Spark', 'Tableau', 
            'FastAPI', 'Machine Learning', 'AI', 'Full Stack'
        ]

    def extract_skills(self):
        """Extracts and counts skill mentions from job descriptions."""
        if self.df.empty:
            logger.warning("No data found to analyze.")
            return {}

        all_descriptions = " ".join(self.df['description'].fillna(''))
        
        skill_counts = {}
        for skill in self.skills_to_track:
            # Case insensitive regex match for whole words
            pattern = rf'\b{re.escape(skill)}\b'
            matches = re.findall(pattern, all_descriptions, re.IGNORECASE)
            skill_counts[skill] = len(matches)
        
        # Sort by frequency
        sorted_skills = dict(sorted(skill_counts.items(), key=lambda item: item[1], reverse=True))
        return sorted_skills

    def get_summary(self):
        """Returns basic statistics about the scraped jobs."""
        summary = {
            "total_jobs": len(self.df),
            "top_locations": self.df['location'].value_counts().head(3).to_dict(),
            "top_companies": self.df['company'].value_counts().head(3).to_dict()
        }
        return summary
