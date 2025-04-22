#!/usr/bin/env python3
"""
Improved Page Generator for Bail Bonds Buddy State Pages (Part 3 of 3)

This script contains the main execution logic and state processing
for creating WordPress/Divi-compatible pages for all 50 states.

This file works together with improved_page_generator_part1.py and
improved_page_generator_part2.py to generate state pages.
"""

import os
import json
import argparse
import sys
import requests
import traceback
from improved_page_generator_part1 import load_template, load_state_data, save_state_page
from improved_page_generator_part2 import (generate_page_for_state, update_title_sections, 
                                          update_content_sections, update_page_title, 
                                          update_state_specific_sections)

# Constants
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "generated_pages")
STATE_DATA_DIR = os.path.join(os.path.dirname(__file__), "state_data")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
TEMPLATE_ID = "1120"  # WordPress ID for the new variables-only template

# WordPress API details
WP_BASE_URL = "https://bailbondsbuddy.com"
WP_API_URL = f"{WP_BASE_URL}/wp-json/wp/v2"
WP_AUTH = ("bbbuddy", "DpSm eiz8 yHjx Sqqk G3lG fqU6")

def save_generated_page(state_name, state_page):
    """Save the generated page as JSON"""
    output_file = f"{OUTPUT_DIR}/{state_name.lower()}.json"
    try:
        with open(output_file, 'w') as f:
            json.dump(state_page, f, indent=2)
        print(f"Generated page saved to {output_file}")
        return True
    except Exception as e:
        print(f"Error saving generated page: {e}")
        return False

def save_html_preview(state_name, state_page):
    """Save an HTML preview of the page for easy review"""
    output_file = f"{OUTPUT_DIR}/{state_name.lower()}.html"
    try:
        # Extract content from the JSON
        title = state_page.get("title", f"{state_name} Bail Bondsman")
        content = state_page.get("content", "")
        
        # Create a simple HTML preview
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>{title}</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; margin: 0; padding: 20px; }}
        h1, h2, h3 {{ color: #0066cc; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{title}</h1>
        {content}
    </div>
</body>
</html>"""
        
        with open(output_file, 'w') as f:
            f.write(html)
        print(f"HTML preview saved to {output_file}")
        return True
    except Exception as e:
        print(f"Error saving HTML preview: {e}")
        return False

def test_with_state(state_name):
    """Test the script with a specified state"""
    print(f"Testing with sample state ({state_name})...")
    # Load the Oklahoma template
    template_json = load_template()
    if not template_json:
        print("Failed to load Oklahoma template")
        return False
    # Generate page for the specified state
    success = generate_page_for_state(state_name, template_json)
    if success:
        print(f"Test successful! {state_name} page generated.")
    else:
        print(f"Test failed for {state_name}.")
    return success

def generate_states_a_to_m(template_json):
    """Generate pages for states A-M"""
    states_a_to_m = [
        "Alabama", "Alaska", "Arizona", "Arkansas", "California", 
        "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", 
        "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", 
        "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", 
        "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana"
    ]
    
    success_count = 0
    for state_name in states_a_to_m:
        print(f"Generating page for {state_name}...")
        if generate_page_for_state(state_name, template_json):
            success_count += 1
    
    print(f"Successfully generated {success_count} out of {len(states_a_to_m)} state pages (A-M).")
    return success_count

def generate_states_n_to_z(template_json):
    """Generate pages for states N-Z"""
    states_n_to_z = [
        "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", 
        "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", 
        "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", 
        "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", 
        "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"
    ]
    
    success_count = 0
    for state_name in states_n_to_z:
        print(f"Generating page for {state_name}...")
        if generate_page_for_state(state_name, template_json):
            success_count += 1
    
    print(f"Successfully generated {success_count} out of {len(states_n_to_z)} state pages (N-Z).")
    return success_count

def generate_all_state_pages():
    """Generate pages for all 50 states"""
    template_json = load_template()
    if not template_json:
        return 0
    
    # Create output directories
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(STATE_DATA_DIR, exist_ok=True)
    os.makedirs(TEMPLATES_DIR, exist_ok=True)
    
    # Generate pages for states A-M
    count_a_to_m = generate_states_a_to_m(template_json)
    
    # Generate pages for states N-Z
    count_n_to_z = generate_states_n_to_z(template_json)
    
    total_count = count_a_to_m + count_n_to_z
    print(f"Page generation complete! Successfully generated {total_count} out of 50 state pages.")
    return total_count

def upload_to_wordpress(state_name):
    """Upload the generated state page to WordPress as a draft"""
    json_path = os.path.join(os.path.dirname(__file__), "generated_pages", f"{state_name.lower()}.json")
    try:
        with open(json_path, 'r') as f:
            state_json = json.load(f)
    except Exception as e:
        print(f"Error loading {json_path}: {e}")
        return False

    # Extract content from the WordPress/Divi JSON structure
    if not isinstance(state_json, dict) or "data" not in state_json:
        print(f"Error: Invalid JSON structure, missing 'data' key")
        return False
    
    data_keys = state_json["data"].keys()
    if not data_keys:
        print(f"Error: No keys found in 'data'")
        return False
    
    first_key = list(data_keys)[0]
    content = state_json["data"][first_key]
    
    print(f"DEBUG upload_to_wordpress: Found content in data[{first_key}], length: {len(content)}")
    
    # Configure page data
    title = f"Find Local {state_name} Bail Bondsmen Near You | 24/7 Emergency Service"
    slug = f"{state_name.lower()}-bail-bondsman-24-hour-emergency-service-nearby"

    page_data = {
        "title": title,
        "slug": slug,
        "content": content,
        "status": "draft",
        "meta": {
            "_et_pb_page_layout": "et_no_sidebar",
            "_et_pb_side_nav": "off",
            "_et_pb_use_builder": "on",
            "_wp_page_template": "page-template-blank.php"
        }
    }

    try:
        response = requests.post(
            f"{WP_API_URL}/pages",
            json=page_data,
            auth=WP_AUTH
        )
        if response.status_code >= 200 and response.status_code < 300:
            page_id = response.json().get("id")
            page_link = response.json().get("link")
            print(f"Success! {state_name} page created on WordPress.")
            print(f"Page ID: {page_id}")
            print(f"Draft URL: {WP_BASE_URL}/?page_id={page_id}")
            print(f"Final URL (when published): {page_link}")
            return True
        else:
            print(f"Error creating page: {response.status_code}")
            print(response.text)
            return False
    except Exception as e:
        print(f"Exception while creating page: {e}")
        import traceback
        traceback.print_exc()
        return False

def generate_state_page(state_name, args=None):
    """Generate a production page for a given state"""
    print(f"Generating production page for {state_name}...")
    
    # Load template
    template_json = load_template()
    if not template_json:
        return False
    
    # Load state data
    state_data = load_state_data(state_name)
    if not state_data:
        print(f"Error: Could not load state data for {state_name}")
        return False
    
    print(f"State data for {state_name}:")
    print(f"  Capital: {state_data['capital']}")
    print(f"  Population: {state_data['population']}")
    print(f"  Cities: {', '.join(state_data['major_cities'][:3])}, and more...")
    
    # Update page title and content with state-specific information
    template_json = update_page_title(template_json, state_name)
    
    # Update content sections with state data
    template_json = update_content_sections(template_json, state_data)
    
    # Generate and update state-specific sections
    template_json = update_state_specific_sections(template_json, state_data)
    
    # Save the state page
    saved_path = save_state_page(template_json, state_name)
    if not saved_path:
        return False
    
    print(f"Generated page saved at {saved_path}")
    
    # Upload to WordPress if requested
    if args and args.upload:
        success = upload_to_wordpress(state_name)
        if not success:
            print("Failed to upload to WordPress")
            return False
    
    return True

# Main function
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--test', nargs='?', const='Texas', default=None, help='Test with a specific state (default: Texas)')
    parser.add_argument('--all', action='store_true', help='Generate all state pages')
    parser.add_argument('--state', type=str, help='Generate a single state page (production mode)')
    parser.add_argument('--upload', action='store_true', help='Upload the generated state page to WordPress as a draft')
    args = parser.parse_args()

    if args.state:
        state_name = args.state
        print(f"Generating production page for {state_name}...")
        template_json = load_template()
        if not template_json:
            print("Failed to load Oklahoma template")
        else:
            success = generate_page_for_state(state_name, template_json)
            if success:
                print(f"Production page for {state_name} generated.")
                if args.upload:
                    upload_to_wordpress(state_name)
            else:
                print(f"Failed to generate production page for {state_name}.")
    elif args.test:
        state_name = args.test
        print(f"Testing with sample state ({state_name})...")
        test_with_state(state_name)
    elif args.all:
        generate_all_state_pages()
    else:
        print("No valid arguments provided. Use --state [State], --test [State], or --all.")
