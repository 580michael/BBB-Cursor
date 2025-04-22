#!/usr/bin/env python3
import os
import json
import requests
import sys
import traceback

# WordPress API details
WP_BASE_URL = "https://bailbondsbuddy.com"
WP_API_URL = f"{WP_BASE_URL}/wp-json/wp/v2"
WP_AUTH = ("bbbuddy", "DpSm eiz8 yHjx Sqqk G3lG fqU6")

def upload_state_page(state_name):
    """Upload a state page JSON to WordPress"""
    # Construct path to the JSON file
    json_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                            "Combined Json State Files", f"{state_name.lower()}.json")
    
    print(f"Looking for JSON file at: {json_path}")
    
    # Check if file exists
    if not os.path.exists(json_path):
        print(f"Error: JSON file not found for {state_name}")
        return False

    try:
        # Load the JSON file
        with open(json_path, 'r') as f:
            state_json_data = json.load(f)
            
        # Extract the content string from the first key in 'data'
        if isinstance(state_json_data.get("data"), dict):
            data_keys = list(state_json_data["data"].keys())
            if data_keys:
                page_content_string = state_json_data["data"][data_keys[0]]
            else:
                print("Error: No content found in JSON data")
                return False
        else:
            print("Error: Invalid JSON structure")
            return False

        # Prepare the page data
        title = f"Find Local {state_name} Bail Bondsmen Near You | 24/7 Emergency Service"
        slug = f"{state_name.lower().replace(' ', '-')}-bail-bondsman-24-hour-emergency-service-nearby"[:100]
        
        page_data = {
            "title": title,
            "slug": slug,
            "content": page_content_string,
            "status": "draft",
            "meta": {
                "_et_pb_use_builder": "on",
                "_et_pb_page_layout": "et_no_sidebar",
                "_et_pb_side_nav": "off"
            }
        }

        # Upload to WordPress
        print(f"Uploading {state_name} page to WordPress...")
        response = requests.post(
            f"{WP_API_URL}/pages",
            json=page_data,
            auth=WP_AUTH,
            timeout=30
        )
        response.raise_for_status()

        # Get page info
        page_info = response.json()
        page_id = page_info.get("id")
        page_link = page_info.get("link")
        edit_link = f"{WP_BASE_URL}/wp-admin/post.php?post={page_id}&action=edit"

        print(f"\nSuccess! {state_name} page uploaded to WordPress")
        print(f"Page ID: {page_id}")
        print(f"Preview Link: {page_link}&preview=true")
        print(f"Edit Link: {edit_link}")
        return True

    except FileNotFoundError:
        print(f"Error: Could not open JSON file for {state_name}")
        return False
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in file: {e}")
        return False
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
        print(f"Response: {e.response.text}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 upload_state_page.py StateName")
        print("Example: python3 upload_state_page.py Alabama")
        sys.exit(1)
        
    state_name = sys.argv[1].strip()
    upload_state_page(state_name) 