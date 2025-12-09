import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import parse_timeline, parse_summary_table
from bs4 import BeautifulSoup
import json
import sys

def test():
    try:
        with open("debug_awb_2.html", "r", encoding="utf-8") as f:
            html = f.read()
        
        soup = BeautifulSoup(html, 'html.parser')
        summary = parse_summary_table(soup)
        history = parse_timeline(soup)
        
        print("SUMMARY_STATUS:", summary.get("current_status"))
        if history:
            print("LATEST_HISTORY_STATUS:", history[0]["status"])
            print("LATEST_HISTORY_LOC:", history[0]["location"])
        else:
            print("NO_HISTORY")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test()
