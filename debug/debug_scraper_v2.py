import requests

def debug():
    awb = "58160500650"
    url_page = "https://stcourier.com/track/shipment"
    url_check = "https://stcourier.com/track/doCheck"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    session = requests.Session()
    session.headers.update(headers)
    
    print("Visiting main page...")
    resp_page = session.get(url_page)
    print(f"Main Page Status: {resp_page.status_code}")
    print(f"Cookies: {session.cookies.get_dict()}")
    
    print("Posting to doCheck...")
    payload = {"awb_no": awb}
    resp_check = session.post(url_check, data=payload)
    print(f"Check Status: {resp_check.status_code}")
    print(f"Response Content: {resp_check.text[:500]}") # Print first 500 chars

    # If it is JSON, print it all
    try:
        print("JSON Decode:", resp_check.json())
    except:
        pass

    with open("debug_output_v2.html", "w", encoding="utf-8") as f:
        f.write(resp_check.text)

if __name__ == "__main__":
    debug()
