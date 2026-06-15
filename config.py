import os

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "8918728773:AAEnQQlECYOWHtc879gIf8wDccw6kWHnmGg")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "904529200")

# Companies to monitor
COMPANIES = [
    "Cognizant",
    "Infosys",
    "Accenture",
    "Wipro",
    "Capgemini",
    "TCS",
    "HCL",
    "IBM",
    "Deloitte",
    "Tech Mahindra"
]

# Keywords for eligibility (case-insensitive substring match)
KEYWORDS = [
    "mca",
    "fresher",
    "graduate trainee",
    "associate software engineer",
    "programmer analyst",
    "system engineer",
    "data analyst",
    "python developer",
    "java developer",
    "cloud engineer",
    "ai engineer"
]