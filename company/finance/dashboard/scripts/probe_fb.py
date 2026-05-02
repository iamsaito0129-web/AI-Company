import requests

urls = [
    "https://oku-jissenn-default-rtdb.firebaseio.com/.json",
    "https://oku-jissenn.firebaseio.com/.json",
    "https://oku-jissenn-default-rtdb.asia-southeast1.firebasedatabase.app/.json",
    "https://oku-jissenn-default-rtdb.europe-west1.firebasedatabase.app/.json"
]

for url in urls:
    try:
        print(f"Testing {url}...")
        resp = requests.get(url)
        print(f"Status: {resp.status_code}")
        if resp.status_code != 404:
            print(f"Content: {resp.text[:100]}")
    except Exception as e:
        print(f"Error: {e}")
