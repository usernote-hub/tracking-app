import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import parse_summary_table, parse_timeline

from bs4 import BeautifulSoup
import json

def test_delivered():
    try:
        # Use path relative to this script
        file_path = os.path.join(os.path.dirname(__file__), "devlivered.html")
        with open(file_path, "r", encoding="utf-8") as f:
            html = f.read()
            
        soup = BeautifulSoup(html, 'html.parser')
        
        print("--- Testing Delivered HTML ---")
        summary = parse_summary_table(soup)
        history = parse_timeline(soup)
        
        print(f"Summary Status: {summary.get('current_status')}")
        
        if history:
            print(f"Latest History Status: {history[0].get('status')}")
            print(f"Latest History Location: {history[0].get('location')}")
            print(f"Total History Items: {len(history)}")
        else:
            print("No history found")
            
        # Logic check:
        final_status = history[0]['status'] if history else summary.get('current_status')
        print(f"Calculated Final Status: {final_status}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_delivered()
