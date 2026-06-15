import html
from scrapers.career_jobs import get_jobs
from database.job_store import save_job
from notifier.telegram_bot import send_notification
from dashboard_gen import generate_dashboard
from logger import logger

def main():
    logger.info("=========================================")
    logger.info("AI Job Watcher service started.")
    logger.info("=========================================")
    
    try:
        # Fetch matching jobs from scrapers
        jobs = get_jobs()
        logger.info(f"Total jobs returned from scraper: {len(jobs)}")
        
        new_jobs_count = 0
        for job in jobs:
            try:
                # Save to database (returns True if it's a new, unique job)
                is_new = save_job(job)
                
                if is_new:
                    new_jobs_count += 1
                    
                    # Format message exactly as required by USER
                    # Escaped to prevent HTML injection/parsing issues
                    company_esc = html.escape(job['company'])
                    role_esc = html.escape(job['role'])
                    loc_esc = html.escape(job['location'])
                    link_esc = html.escape(job['link'])
                    
                    message = f"""🚀 New Job Found

Company: {company_esc}
Role: {role_esc}
Location: {loc_esc}

Apply:
{link_esc}"""
                    
                    # Send notification to Telegram channel/bot
                    send_notification(message)
                    
            except Exception as item_err:
                logger.error(f"Error processing job item: {job}. Error: {item_err}")
                
        logger.info(f"Execution finished. Found {new_jobs_count} new job alerts.")
        
        # Auto-update the dashboard
        generate_dashboard()
        
    except Exception as e:
        logger.error(f"Critical error in main loop: {e}")

if __name__ == "__main__":
    main()