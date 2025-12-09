import requests
from bs4 import BeautifulSoup
import sys

def debug():
    url = "https://stcourier.com/track/shipment"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    print(f"Fetching {url}...", flush=True)
    try:
        session = requests.Session()
        resp = session.get(url, headers=headers, timeout=15)
        print(f"Page Status: {resp.status_code}", flush=True)
        
        soup = BeautifulSoup(resp.text, 'html.parser')
        forms = soup.find_all('form')
        
        print(f"Found {len(forms)} forms.", flush=True)
        for i, form in enumerate(forms):
            print(f"Form {i+1}:", flush=True)
            print(f"  Action: {form.get('action')}", flush=True)
            print(f"  Method: {form.get('method')}", flush=True)
            inputs = form.find_all('input')
            for inp in inputs:
                print(f"    Input: {inp.get('name')} (Type: {inp.get('type')}, Value: {inp.get('value')})", flush=True)

    except Exception as e:
        print(f"Error: {e}", flush=True)

if __name__ == "__main__":
    debug()
