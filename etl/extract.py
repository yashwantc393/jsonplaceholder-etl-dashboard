import requests
import json
import os

BASE_URL = "https://jsonplaceholder.typicode.com"

def fetch_and_save(endpoint):
    response = requests.get(f"{BASE_URL}/{endpoint}")
    response.raise_for_status()

    os.makedirs("data/raw", exist_ok=True)

    with open(f"data/raw/{endpoint}.json", "w") as f:
        json.dump(response.json(), f, indent=2)

if __name__ == "__main__":
    fetch_and_save("posts")
    fetch_and_save("users")
    fetch_and_save("todos")
    fetch_and_save("comments")

