import sys
import os
import requests

# Add parent path to import main
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import get_tracking_info
from tests.validate_structure import validate_html_structure

def check_website_status():
    # Use a known historic AWB, or just check the error page/landing page structure if possible.
    # Since we need the table, we need a valid AWB. 
    # Use the one we know works: 58160500650
    test_awb = "58160500650" 
    
    print(f"Fetching data for AWB {test_awb} to validate site structure...")
    html = get_tracking_info(test_awb)
    
    if not html:
        print("CRITICAL: Failed to fetch data from ST Courier. Site might be down or blocking.")
        sys.exit(1)
        
    errors = validate_html_structure(html)
    
    if errors:
        print("WARNING: Website structure drift detected!")
        for err in errors:
            print(f" - {err}")
        print("The scraper is likely BROKEN.")
        sys.exit(1)
    else:
        print("SUCCESS: Website structure appears normal.")
        sys.exit(0)

if __name__ == "__main__":
    check_website_status()
