import requests
import json
import time

def test_api():
    url = "http://localhost:8000/api/track/58160500650"
    print(f"Testing URL: {url}")
    
    try:
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("Response JSON:")
            print(json.dumps(data, indent=2))
        else:
            print("Response Text:")
            print(response.text)
            
    except Exception as e:
        print(f"Test failed: {e}")

if __name__ == "__main__":
    # Wait a bit for server to start if run immediately after
    time.sleep(2) 
    test_api()
