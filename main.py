import requests
import time
import json
import random

# Read authentication tokens from data.txt
with open("data.txt", "r") as file:
    auth_tokens = [line.strip() for line in file if line.strip()]

# API URLs
tap_url = "https://gold-eagle-api.fly.dev/tap"
claim_url = "https://gold-eagle-api.fly.dev/wallet/claim"

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

def send_tap_request(auth_token):
    """Send tap request using a specific authorization token."""
    headers = headers_template.copy()
    headers["authorization"] = f"Bearer {auth_token}"

    data = {
        "available_taps": 1000,  
        "count": random.randint(269, 311), # Number of taps as random number
        "timestamp": int(time.time()),  # Generate current timestamp
        "salt": "83fded5f-fac6-4882-82a6-26723fe8071c"
    }

    try:
        response = requests.post(tap_url, headers=headers, data=json.dumps(data))
        print(f"TAP Response ({auth_token[:10]}...): {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"TAP Request failed for {auth_token[:10]}: {e}")

def send_claim_request(auth_token):
    """Send claim request using a specific authorization token."""
    headers = headers_template.copy()
    headers["authorization"] = f"Bearer {auth_token}"
    headers["content-length"] = "0"

    try:
        response = requests.post(claim_url, headers=headers)
        print(f"CLAIM Response ({auth_token[:10]}...): {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"CLAIM Request failed for {auth_token[:10]}: {e}")

cycle_count = 0  # Track cycles

while True:
    cycle_count += 1
    print(f"Starting Cycle {cycle_count}...")

    for token in auth_tokens:
        send_tap_request(token)
        time.sleep(2)  # Small delay between requests to avoid rate limits

    if cycle_count % 2 == 0:  # Every 2 cycles, send claim requests
        print("Sending CLAIM requests for all accounts...")
        for token in auth_tokens:
            send_claim_request(token)
            time.sleep(2)  # Small delay between requests

    print("Waiting 5 minutes before the next cycle...")
    time.sleep(300)  # Wait for 5 minutes before restarting