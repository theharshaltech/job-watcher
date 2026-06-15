import requests
from bs4 import BeautifulSoup
import urllib.parse
import time
import random
from logger import logger
from config import KEYWORDS

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
]

# Mapping of companies to their search terms and valid matching substrings
COMPANY_CONFIGS = [
    {"search_name": "Cognizant", "matches": ["cognizant"]},
    {"search_name": "Infosys", "matches": ["infosys"]},
    {"search_name": "Accenture", "matches": ["accenture"]},
    {"search_name": "Wipro", "matches": ["wipro"]},
    {"search_name": "Capgemini", "matches": ["capgemini"]},
    {"search_name": "Tata Consultancy Services", "matches": ["tata consultancy services", "tcs"]},
    {"search_name": "HCLTech", "matches": ["hcltech", "hcl technologies", "hcl"]},
    {"search_name": "IBM", "matches": ["ibm"]},
    {"search_name": "Deloitte", "matches": ["deloitte"]},
    {"search_name": "Tech Mahindra", "matches": ["tech mahindra"]}
]

def get_jobs():
    all_jobs = []
    
    # We construct a Boolean query using the keywords to search LinkedIn
    # This filters down results to only relevant roles at the search source
    boolean_filter = '("MCA" OR "Fresher" OR "Trainee" OR "Associate" OR "Analyst" OR "Engineer" OR "Developer")'
    
    for config in COMPANY_CONFIGS:
        company_name = config["search_name"]
        company_matches = config["matches"]
        
        query = f'"{company_name}" {boolean_filter}'
        encoded_query = urllib.parse.quote(query)
        
        # Querying the first 25 jobs (page 1)
        url = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={encoded_query}&location=India&start=0"
        
        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://www.linkedin.com/jobs/search"
        }
        
        logger.info(f"Scraping jobs for {company_name}...")
        
        try:
            # Adding a tiny delay to avoid overwhelming the server
            time.sleep(random.uniform(1.5, 3.0))
            
            response = requests.get(url, headers=headers, timeout=15)
            
            if response.status_code != 200:
                logger.error(f"Failed request for {company_name}: Status Code {response.status_code}")
                continue
                
            soup = BeautifulSoup(response.text, 'html.parser')
            job_cards = soup.find_all('li')
            
            logger.info(f"Found {len(job_cards)} raw cards for {company_name}")
            
            company_jobs_found = 0
            for card in job_cards:
                try:
                    # 1. Extract Role / Job Title
                    title_el = card.find('h3', class_='base-search-card__title')
                    role = title_el.text.strip() if title_el else ""
                    
                    # 2. Extract Company Name
                    company_el = card.find('h4', class_='base-search-card__subtitle')
                    company_raw = company_el.text.strip() if company_el else ""
                    
                    # 3. Extract Location
                    loc_el = card.find('span', class_='job-search-card__location')
                    location = loc_el.text.strip() if loc_el else "India"
                    
                    # 4. Extract Apply Link
                    link_el = card.find('a', class_='base-card__full-link')
                    link = link_el['href'] if link_el else ""
                    if not link:
                        link_el = card.find('a')
                        link = link_el['href'] if link_el else ""
                    
                    # Clean the link (remove tracking params)
                    link = link.split('?')[0] if link else ""
                    
                    # 5. Extract Date Posted
                    time_el = card.find('time')
                    date_posted = "N/A"
                    if time_el:
                        # Try datetime attribute first, then text
                        date_posted = time_el.get('datetime') or time_el.text.strip()
                        date_posted = date_posted.strip()
                    
                    # Skip if essential info is missing
                    if not role or not company_raw or not link:
                        continue
                        
                    # --- ELIGIBILITY FILTERS ---
                    
                    # A. Company Match (ensure it belongs to target company)
                    company_lower = company_raw.lower()
                    is_company_match = any(m in company_lower for m in company_matches)
                    
                    if not is_company_match:
                        continue
                        
                    # B. Keyword Match (case-insensitive substring check in job title)
                    role_lower = role.lower()
                    is_keyword_match = any(keyword in role_lower for keyword in KEYWORDS)
                    
                    if not is_keyword_match:
                        continue
                    
                    # Job passes all filters!
                    job = {
                        "company": company_raw,
                        "role": role,
                        "location": location,
                        "link": link,
                        "date_posted": date_posted
                    }
                    
                    all_jobs.append(job)
                    company_jobs_found += 1
                    
                except Exception as card_err:
                    logger.error(f"Scraping error parsing card details for {company_name}: {card_err}")
                    
            logger.info(f"Extracted {company_jobs_found} eligible jobs for {company_name}")
            
        except requests.exceptions.RequestException as req_err:
            logger.error(f"Failed request to LinkedIn for {company_name}: {req_err}")
        except Exception as e:
            logger.error(f"Scraping error for {company_name}: {e}")
            
    logger.info(f"Scraping complete. Total eligible jobs extracted: {len(all_jobs)}")
    return all_jobs