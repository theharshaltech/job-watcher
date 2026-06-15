import os

# Load .env file manually if it exists (for local testing)
if os.path.exists(".env"):
    with open(".env", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, val = line.split("=", 1)
                os.environ[key.strip()] = val.strip()

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

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