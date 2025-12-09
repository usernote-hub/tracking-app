# structural_schema.py

# A dictionary of critical selectors that MUST exist for our scraper to work.
# Key: Description, Value: CSS Selector
REQUIRED_SELECTORS = {
    "Summary Table": "table.table-bordered",
    "Summary Rows": "table.table-bordered tr",
    "Current Status Label": "td", # We might check text content in the validator
    "History Container": "div.col-md-8", # The container for history
    "History Event Row": "div.tl08",     # The weird class name we noticed, assuming it's stable-ish or we verify the structure
}

# Optional: Text content we expect to find in the page to ensure we are on the right page
REQUIRED_TEXTS = [
    "Delivery Status",
    "Status of AWB No"
]
