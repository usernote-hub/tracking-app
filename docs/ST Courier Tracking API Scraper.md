This is a perfect task for an AI coding assistant. To get the best results from Cursor, Windsurf, or generic LLMs (Claude/GPT), you need to structure the prompt as a **Product Requirement Document (PRD)** or a **Technical Specification**.

Here is the prepared **Todo-Document**. You can copy-paste this entire block directly into your AI tool.

# ---

**Technical Spec: ST Courier Tracking API Scraper**

## **1\. Project Overview**

**Goal:** Build a backend API that accepts a tracking number (AWB), scrapes the ST Courier website, parses the HTML response, and returns the shipment status in a clean JSON format.

Target Website: https://stcourier.com/track/shipment  
Method: Web Scraping (since no public JSON API exists).

## **2\. Tech Stack Recommendations**

* **Language:** Python (preferred) or Node.js.  
* **Framework:** FastAPI (Python) or Express (Node.js).  
* **Scraping Library:** BeautifulSoup4 (Python) or Cheerio (Node.js).  
* **HTTP Client:** requests or httpx.

## **3\. Workflow Logic**

1. **Input:** User calls our API endpoint GET /track/{awb\_number}.  
2. **Upstream Request:**  
   * The system sends a POST request to https://stcourier.com/track/doCheck.  
   * **Headers:** Standard User-Agent to avoid blocking.  
   * **Payload:** awb\_no={awb\_number}.  
3. **Response Handling:**  
   * The server returns raw HTML.  
   * Check for HTTP 200/201.  
4. **Parsing (Extraction):**  
   * Extract "Delivery Status" table (Current Status, Origin, Destination).  
   * Extract "Shipment History" timeline (Date, Time, Location, Activity).  
5. **Output:** Return structured JSON.

## **4\. HTML Parsing Strategy (Selectors)**

### **Part A: The Summary Table**

**Target HTML Context:**

HTML

\<table class\="table-bordered table ..."\>  
    \<tbody\>  
        \<tr\> \<td\>Current Status\</td\> \<td class\="font-normal"\>In Transit\</td\> \</tr\>  
        \</tbody\>  
\</table\>

**Extraction Logic:**

* Locate the table with class table-bordered.  
* Iterate through tr elements.  
* Key \= first td text (trimmed).  
* Value \= second td text (trimmed).

### **Part B: The Timeline (History)**

**Target HTML Context:**

HTML

\<div class\="col-md-8"\>  
    \<h4 class\="mb-3"\>Status of AWB No...\</h4\>  
    \<div class\="4f23a tr08"\> \<div class\="295TEh tl08"\> \<div class\="61F2N92"\>Dec 08, 2025\<br\>04:39 PM\</div\> \<div class\="H7C3Kd9"\>Consignment Booked\<br\>VALAPADI, TN\</div\> \</div\>  
    \</div\>  
\</div\>

**Extraction Logic:**

* **Warning:** The class names (e.g., 4f23a, 61F2N92) look obfuscated/random. Do **not** rely solely on them if possible.  
* **Resilient Selector Strategy:**  
  1. Find the h4 containing text "Status of AWB No".  
  2. Find the sibling div immediately following that h4.  
  3. Iterate through the direct children divs (each represents an event).  
  4. Inside each event:  
     * **Date/Time:** Extract text from the 1st column div (left side). Split by \<br\> or newline to get Date vs Time.  
     * **Status/Location:** Extract text from the 3rd column div (right side). Split by \<br\> or newline to get Status vs Location.

## **5\. Development Todo List (Step-by-Step)**

### **Step 1: Setup**

* \[ \] Initialize project structure.  
* \[ \] Install dependencies (fastapi, uvicorn, requests, beautifulsoup4).

### **Step 2: The Scraper Function**

* \[ \] Create a function get\_tracking\_info(awb).  
* \[ \] Implement the POST request to https://stcourier.com/track/doCheck.  
* \[ \] handle the awb\_no form data.

### **Step 3: The Parser**

* \[ \] Implement parse\_summary\_table(html\_content):  
  * Should return dict: {"current\_status": "...", "origin": "...", "destination": "...", "consignment": "..."}.  
* \[ \] Implement parse\_timeline(html\_content):  
  * Should return list of objects: \[{"date": "...", "time": "...", "status": "...", "location": "..."}\].  
* \[ \] **Clean Data:** Ensure whitespace is stripped (\\n, \\t).

### **Step 4: The API Endpoint**

* \[ \] Create route GET /api/track/{awb}.  
* \[ \] Call the scraper function.  
* \[ \] Handle errors:  
  * If the table isn't found, return 404 "AWB not found".  
  * If the request fails, return 500\.

## **6\. Sample Data for Testing**

**AWB:** 58160500650

**Expected JSON Output:**

JSON

{  
  "success": true,  
  "awb": "58160500650",  
  "summary": {  
    "current\_status": "In Transit",  
    "origin": "TNSLM-VPD",  
    "destination": "TNSLM-VPD",  
    "consignment": "Dox \- 1 Nos"  
  },  
  "history": \[  
    {  
      "timestamp": "2025-12-08 16:39",  
      "date": "Dec 08, 2025",  
      "time": "04:39 PM",  
      "status": "Consignment Booked",  
      "location": "VALAPADI, TN"  
    }  
  \]  
}  
