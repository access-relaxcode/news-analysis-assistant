import os
import requests

def send_discord(message):
    webhook_url = os.environ.get("DISCORD_WEBHOOK_URL", "").strip()

    if not webhook_url:
        raise ValueError("디스코드 웹훅 주소가 설정되지 않았습니다.")
        
    response = requests.post(
        webhook_url,
        params={"wait": "true"},
        json={"content": message},
        timeout=10,
    )
    response.raise_for_status()