import sys
import os
from bs4 import BeautifulSoup
# Add parent dir to path to allow importing if needed, mostly for independence
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tests.structural_schema import REQUIRED_SELECTORS, REQUIRED_TEXTS

def validate_html_structure(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    errors = []
    
    # Check Selectors
    for name, selector in REQUIRED_SELECTORS.items():
        if not soup.select(selector):
            errors.append(f"Missing Critical Element: {name} (Selector: '{selector}')")
            
    # Check Text
    text_content = soup.get_text()
    for text in REQUIRED_TEXTS:
        if text not in text_content:
            errors.append(f"Missing Critical Text: '{text}'")
            
    return errors

def main():
    # Example usage: Validating the delivered.html
    path = os.path.join(os.path.dirname(__file__), "devlivered.html")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            html = f.read()
        
        print(f"Validating {path}...")
        results = validate_html_structure(html)
        if results:
            print("Validation FAILED!")
            for err in results:
                print(f" - {err}")
        else:
            print("Validation PASSED: Structure matches schema.")
    else:
        print("devlivered.html not found for testing.")

if __name__ == "__main__":
    main()
