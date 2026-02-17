# 🕷️ Day 9: Job Market Analyzer

## 📝 Overview
A Python-based web scraper and data analyzer that identifies trending technical skills in the job market. This project demonstrates web scraping best practices, data cleaning with pandas, and strategic market awareness.

## 🚀 Features
- **Smart Scraper**: Uses `BeautifulSoup4` and `requests` to extract job data from listings.
- **Skill Analysis Engine**: Quantifies technical skill mentions (Python, SQL, AWS, etc.) using regex-based extraction.
- **Market Insights**: Generates summaries of top companies and locations for specific roles.
- **JSON Export**: Saves analysis results for ingestion into dashboards or further ETL pipelines.

## 🛠️ Tech Stack
- **Languages**: Python 3.8+
- **Libraries**: BeautifulSoup4, Requests, Pandas, Matplotlib
- **Patterns**: Functional programming for data transformation

## 🏃 Run the Analyzer
```bash
# Install dependencies
pip install -r requirements.txt

# Run the scraper and analyzer
python main.py
```

## 📊 Sample Output
```text
Total Jobs Analyzed: 100
Top Technical Skills in Demand:
- Python: 85 mentions
- SQL: 62 mentions
- AWS: 45 mentions
...
```

## 🛡️ Responsible Scraping
This project is for educational purposes. For production use, always:
- Check `robots.txt`
- Implement proper rate limiting (`time.sleep`)
- Use rotating User-Agents if necessary
- Minimize server load
