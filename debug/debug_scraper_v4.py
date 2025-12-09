import requests

def debug():
    base_url = "https://stcourier.com"
    awb = "58160500650"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    session = requests.Session()
    session.headers.update(headers)
    
    # Test 1: GET with query param
    print("Test 1: GET /track/shipment?awb_no=...", flush=True)
    try:
        resp = session.get(f"{base_url}/track/shipment?awb_no={awb}", timeout=15)
        print(f"Status: {resp.status_code}", flush=True)
        if "Status of AWB No" in resp.text:
            print("-> SUCCESS: Found data via GET query param", flush=True)
        else:
            print("-> Failed via GET query param", flush=True)
    except Exception as e:
        print(f"Test 1 Failed with error: {e}", flush=True)
        
    # Test 2: POST then GET
    print("\nTest 2: POST /track/doCheck then GET /track/shipment", flush=True)
    try:
        resp_post = session.post(f"{base_url}/track/doCheck", data={"awb_no": awb}, timeout=15)
        print(f"POST Status: {resp_post.status_code}", flush=True)
        print(f"POST JSON: {resp_post.json()}", flush=True)
        
        resp_get = session.get(f"{base_url}/track/shipment", timeout=15)
        print(f"GET Status: {resp_get.status_code}", flush=True)
        if "Status of AWB No" in resp_get.text:
           print("-> SUCCESS: Found data via POST + GET", flush=True)
           # Save successful HTML
           with open("success_output.html", "w", encoding="utf-8") as f:
               f.write(resp_get.text)
        elif "In Transit" in resp_get.text:
           print("-> SUCCESS: Found 'In Transit' via POST + GET", flush=True)
        else:
           print("-> Failed via POST + GET", flush=True)
           # Save HTML to see what's there
           with open("debug_v4_page.html", "w", encoding="utf-8") as f:
               f.write(resp_get.text)
               
    except Exception as e:
         print(f"Test 2 Failed with error: {e}", flush=True)

if __name__ == "__main__":
    debug()
