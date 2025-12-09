import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import get_tracking_info, parse_summary_table, parse_timeline
from bs4 import BeautifulSoup
import json

def test_new_awb():
    awb = "58158720966"
    print(f"Testing AWB: {awb}")
    
    html = get_tracking_info(awb)
    if not html:
        print("Failed to get HTML")
        return

    soup = BeautifulSoup(html, 'html.parser')
    
    print("--- Summary ---")
    summary = parse_summary_table(soup)
    print(json.dumps(summary, indent=2))
    
    print("\n--- History ---")
    history = parse_timeline(soup)
    print(json.dumps(history, indent=2))
    
    # Save HTML for inspection if needed
    with open("debug_awb_2.html", "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    test_new_awb()
