import requests
from config import BOT_TOKEN, CHAT_ID
from logger import logger

def send_notification(message):
    logger.info("Sending Telegram Message...")
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    
    try:
        response = requests.post(
            url,
            data={
                "chat_id": CHAT_ID,
                "text": message,
                "parse_mode": "HTML" # Support HTML formatting for rich messages
            },
            timeout=15
        )
        
        if response.status_code == 200:
            logger.info("Telegram notification sent successfully.")
            return True
        else:
            logger.error(f"Failed to send Telegram notification. Status Code: {response.status_code}. Response: {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"Error sending Telegram notification: {e}")
        return False