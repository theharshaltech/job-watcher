import requests

BOT_TOKEN = "8918728773:AAEnQQlECYOWHtc879gIf8wDccw6kWHnmGg"
CHAT_ID = "904529200"

message = """
🚀 Job Watcher Online

Hello Harshal!
Telegram notifications are working.
"""

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

response = requests.post(
    url,
    data={
        "chat_id": CHAT_ID,
        "text": message 
    }
)

print(response.text)