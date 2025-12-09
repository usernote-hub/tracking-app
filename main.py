from fastapi import FastAPI, HTTPException, status
import requests
from bs4 import BeautifulSoup
import uvicorn
import re

app = FastAPI(title="ST Courier Tracking API")

@app.get("/health")
def health_check():
    return {"status": "ok"}

def get_tracking_info(awb: str):
    url_check = "https://stcourier.com/track/doCheck"
    url_page = "https://stcourier.com/track/shipment"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    session = requests.Session()
    session.headers.update(headers)
    
    try:
        # Step 1: POST to doCheck to init session/state
        payload = {"awb_no": awb}
        resp_check = session.post(url_check, data=payload, timeout=30)
        resp_check.raise_for_status()
        
        # Step 2: GET the shipment page which should now contain the data
        resp_page = session.get(url_page, timeout=30)
        resp_page.raise_for_status()
        
        return resp_page.text
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def parse_summary_table(soup):
    summary = {}
    # Locate the table with class table-bordered
    table = soup.find('table', class_='table-bordered')
    if not table:
        return None
    
    rows = table.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        if len(cols) == 2:
            key_text = cols[0].get_text(strip=True)
            value_text = cols[1].get_text(strip=True)
            
            # Normalize keys to match requirements
            key = key_text.lower().replace(" ", "_")
            summary[key] = value_text
            
    return summary

def parse_timeline(soup):
    history = []
    # Resilient Selector Strategy:
    # 1. Find h4 with "Status of AWB No"
    target_h4 = None
    for h4 in soup.find_all('h4'):
        if "Status of AWB No" in h4.get_text():
            target_h4 = h4
            break
            
    if not target_h4:
        return []

    # 2. Find sibling div immediately following that h4
    container = target_h4.find_next_sibling('div')
    if not container:
        return []
        
    # 3. Iterate through direct children divs (each represents an event)
    events = container.find_all('div', recursive=False)
    for event in events:
        # Inside each event, we expect columns.
        # Based on inspection/doc: 
        # 1st column (Date/Time)
        # 2nd column (Connector/Icon) - Optional/Ignore
        # 3rd column (Status/Location)
        
        cols = event.find_all('div', recursive=False)
        
        # We need at least the Date/Time and Status/Location columns.
        # They might be at index 0 and 2.
        if len(cols) >= 1:
            date_time_div = cols[0]
            # Use separator to split lines (Date vs Time)
            dt_lines = list(date_time_div.stripped_strings)
            date = dt_lines[0] if len(dt_lines) > 0 else ""
            time_val = dt_lines[1] if len(dt_lines) > 1 else ""
            
            status = ""
            location = ""
            
            # Try to find the status/location column.
            # If there are 3 cols, it's likely index 2.
            # If there are 2 cols, maybe index 1?
            # Let's assume the last column if > 1
            if len(cols) > 1:
                status_loc_div = cols[-1] 
                sl_lines = list(status_loc_div.stripped_strings)
                status = sl_lines[0] if len(sl_lines) > 0 else ""
                location = sl_lines[1] if len(sl_lines) > 1 else ""
            
            # If we successfully extracted at least a date, add it
            if date:
                history.append({
                    "date": date,
                    "time": time_val,
                    "status": status,
                    "location": location
                })
                
    return history

@app.get("/api/track/{awb}")
def track_shipment(awb: str):
    html_content = get_tracking_info(awb)
    if not html_content:
        raise HTTPException(status_code=500, detail="Failed to fetch data from ST Courier")
        
    soup = BeautifulSoup(html_content, 'html.parser')
    
    summary = parse_summary_table(soup)
    if not summary:
        # If summary table is missing, it's likely an invalid AWB or structure change
        raise HTTPException(status_code=404, detail="AWB not found or data unavailable")
        
    history = parse_timeline(soup)
    
    if history:
        # Override summary status with the latest timeline status as it is more accurate/granular
        summary['current_status'] = history[0]['status']
    
    return {
        "success": True,
        "awb": awb,
        "summary": summary,
        "history": history
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
