from main import get_tracking_info

def debug():
    awb = "58160500650"
    print(f"Fetching data for AWB: {awb}")
    html = get_tracking_info(awb)
    
    if html:
        with open("debug_output.html", "w", encoding="utf-8") as f:
            f.write(html)
        print("HTML saved to debug_output.html")
    else:
        print("No HTML returned")

if __name__ == "__main__":
    debug()
