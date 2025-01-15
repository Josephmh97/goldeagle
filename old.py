import requests
import time
import json
import random

# Read authentication tokens from data.txt
with open("data.txt", "r") as file:
    auth_tokens = [line.strip() for line in file if line.strip()]

# API URL
url = "https://gold-eagle-api.fly.dev/tap"

# Headers template (common for all requests except Authorization)
headers_template = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/json",
    "origin": "https://telegram.geagle.online",
    "priority": "u=1, i",
    "referer": "https://telegram.geagle.online/",
    "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}

def send_request(auth_token):
    """Send request using a specific authorization token."""
    headers = headers_template.copy()
    headers["authorization"] = f"Bearer {auth_token}"

    data = {
        "available_taps": 1000,
        "count": random.randint(300, 349),# Number of taps
        "timestamp": int(time.time()),  # Generate current timestamp
        "salt": "83fded5f-fac6-4882-82a6-26723fe8071c"
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        print(f"Response ({auth_token[:10]}...): {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed for {auth_token[:10]}: {e}")

while True:
    for token in auth_tokens:
        send_request(token)
        time.sleep(2)  # Small delay between accounts to avoid rate limits

    print("Waiting 3 minutes before the next cycle...")
    time.sleep(180)  # Wait for 3 minutes before restarting