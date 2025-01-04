import requests
import time
import uuid

# Function to send the /tap request
def send_tap_request(available_taps, count, token):
    url = 'https://api-gw.geagle.online/tap'
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'authorization': f'Bearer {token}',
        'content-type': 'application/json',
        'origin': 'https://telegram.geagle.online',
        'priority': 'u=1, i',
        'referer': 'https://telegram.geagle.online/',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    }

    timestamp = int(time.time())
    salt = str(uuid.uuid4())

    data = {
        "available_taps": available_taps,
        "count": count,
        "timestamp": timestamp,
        "salt": salt
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Function to send the /wallet/claim request
def send_claim_request(token):
    url = 'https://api-gw.geagle.online/wallet/claim'
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'authorization': f'Bearer {token}',
        'content-length': '0',
        'origin': 'https://telegram.geagle.online',
        'priority': 'u=1, i',
        'referer': 'https://telegram.geagle.online/',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    }

    response = requests.post(url, headers=headers)
    return response.json()

# Read the Bearer tokens from data.txt
with open('data.txt', 'r') as file:
    tokens = [line.strip() for line in file.readlines()]

# Fixed values for the /tap request
available_taps = 1000
count = 419

# Loop to send requests for each token, alternating between /tap and /wallet/claim
while True:
    for token in tokens:
        # Send the /tap request
        tap_response = send_tap_request(available_taps, count, token)
        print(f"/tap response for token {token}: {tap_response}")

        # Send the /wallet/claim request
        claim_response = send_claim_request(token)
        print(f"/wallet/claim response for token {token}: {claim_response}")

    # Wait for 7 minutes before repeating the process for all accounts
    print("Waiting for 7 minutes before repeating...")
    time.sleep(7 * 60)  # Wait for 7 minutes before starting the next iteration
