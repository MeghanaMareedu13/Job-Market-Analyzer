from scraper import JobScraper
from analyzer import JobAnalyzer
import logging
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(message)s')
logger = logging.getLogger("Main")

def main():
    logger.info("Day 9: Job Market Analyzer starting...")
    
    # 1. Scrape Data
    scraper = JobScraper()
    html = scraper.fetch_jobs()
    jobs = scraper.parse_jobs(html)
    
    if not jobs:
        logger.error("No jobs found. Check your connection or the target URL.")
        return

    # 2. Analyze Data
    analyzer = JobAnalyzer(jobs)
    skills = analyzer.extract_skills()
    summary = analyzer.get_summary()
    
    # 3. Output Results
    print("\n" + "="*40)
    print("📈 JOB MARKET ANALYSIS SUMMARY")
    print("="*40)
    print(f"Total Jobs Analyzed: {summary['total_jobs']}")
    print("\nTop Technical Skills in Demand:")
    for skill, count in list(skills.items())[:10]:
        if count > 0:
            print(f"- {skill}: {count} mentions")
    
    print("\nTop Locations:")
    for loc, count in summary['top_locations'].items():
        print(f"- {loc}: {count} openings")
    
    print("="*40)
    
    # Save results to JSON for potential dashboard use
    with open('market_summary.json', 'w') as f:
        json.dump({"summary": summary, "skills": skills}, f, indent=4)
    logger.info("Results saved to market_summary.json")

if __name__ == "__main__":
    main()
