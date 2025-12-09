import requests
import time
import json

def test():
    awb = "58158720966"
    url = f"http://localhost:8000/api/track/{awb}"
    print(f"Testing URL: {url}")
    
    try:
        response = requests.get(url)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("Current Status:", data['summary'].get('current_status'))
            print("Full Response:")
            print(json.dumps(data, indent=2))
        else:
            print("Error:", response.text)
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    time.sleep(1)
    test()
