from notifier.telegram_bot import send_notification

send_notification(
    "🚀 Job Watcher Started Successfully!"
)

print("Done")

from scrapers.career_jobs import get_jobs
from database.job_store import save_job
from notifier.telegram_bot import send_notification

jobs = get_jobs()

for job in jobs:

    is_new = save_job(job)

    if is_new:

        message = f"""
🚀 New Job Found

Company: {job['company']}
Role: {job['role']}

Apply:
{job['link']}
"""

        send_notification(message)

print("Finished")