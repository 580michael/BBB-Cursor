#!/usr/bin/env python3
"""
Import Texas JSON Page to WordPress

This script imports the pre-generated Texas JSON file to WordPress
with proper metadata and URL structure.
"""

import os
import json
import requests
import sys
import time

# WordPress API configuration
BASE_URL = "https://bailbondsbuddy.com"
API_URL = f"{BASE_URL}/wp-json/wp/v2"
AUTH = ("bbbuddy", "DpSm eiz8 yHjx Sqqk G3lG fqU6")

# State info
STATE_NAME = "Texas"
STATE_SLUG = "texas-bail-bondsman-emergency-24-hour-service-available"
STATE_TITLE = f"Find Local {STATE_NAME} Bail Bondsmen Near You | 24/7 Emergency Service"

# File paths
TEXAS_JSON_PATH = "Manus/Generated_State_Pages/texas.json"

def main():
    print(f"Importing {STATE_NAME} page to WordPress...")
    
    # Load the Texas JSON file
    try:
        with open(TEXAS_JSON_PATH, 'r') as f:
            texas_json = json.load(f)
            print(f"Successfully loaded {TEXAS_JSON_PATH}")
    except Exception as e:
        print(f"Error loading {TEXAS_JSON_PATH}: {e}")
        sys.exit(1)
    
    # Extract the content from the JSON
    divi_content = ""
    if "data" in texas_json:
        for key, value in texas_json["data"].items():
            divi_content = value
            break
    
    if not divi_content:
        print("Error: Could not extract content from JSON file")
        sys.exit(1)
    
    # Prepare page data
    page_data = {
        "title": STATE_TITLE,
        "slug": STATE_SLUG,
        "content": divi_content,
        "status": "draft",
        "meta": {
            "_et_pb_page_layout": "et_no_sidebar",  # Full width
            "_et_pb_side_nav": "off",  # No side nav
            "_et_pb_use_builder": "on",  # Enable DIVI
            "_wp_page_template": "page-template-blank.php"  # Blank template
        }
    }
    
    # Create the page on WordPress
    try:
        response = requests.post(
            f"{API_URL}/pages",
            json=page_data,
            auth=AUTH
        )
        
        if response.status_code >= 200 and response.status_code < 300:
            page_id = response.json().get("id")
            page_link = response.json().get("link")
            print(f"Success! {STATE_NAME} page created.")
            print(f"Page ID: {page_id}")
            print(f"Draft URL: {BASE_URL}/?page_id={page_id}")
            print(f"Final URL (when published): {page_link}")
            return page_id
        else:
            print(f"Error creating page: {response.status_code}")
            print(response.text)
            sys.exit(1)
    except Exception as e:
        print(f"Exception while creating page: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 