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
from improved_page_generator_part1 import load_template, load_state_data
from improved_page_generator_part2 import generate_page_for_state

# Constants
BASE_DIR = "/home/ubuntu/bailbonds"
OUTPUT_DIR = f"{BASE_DIR}/generated_pages"
STATE_DATA_DIR = f"{BASE_DIR}/state_data"

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

def test_with_sample_state():
    """Test the script with a sample state (Texas)"""
    print("Testing with sample state (Texas)...")
    template_json = load_template()
    if not template_json:
        return False
    
    success = generate_page_for_state("Texas", template_json)
    if success:
        print("Test successful! Texas page generated.")
    else:
        print("Test failed.")
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
    
    # Generate pages for states A-M
    count_a_to_m = generate_states_a_to_m(template_json)
    
    # Generate pages for states N-Z
    count_n_to_z = generate_states_n_to_z(template_json)
    
    total_count = count_a_to_m + count_n_to_z
    print(f"Page generation complete! Successfully generated {total_count} out of 50 state pages.")
    return total_count

# Main function
if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Generate bail bondsman pages for all 50 states')
    parser.add_argument('--test', action='store_true', help='Test the script with a sample state (Texas)')
    parser.add_argument('--all', action='store_true', help='Generate pages for all 50 states')
    args = parser.parse_args()
    
    # Create output directories
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(STATE_DATA_DIR, exist_ok=True)
    
    if args.test:
        test_with_sample_state()
    elif args.all:
        generate_all_state_pages()
    else:
        print("Please specify either --test or --all")
        print("  --test: Test the script with a sample state (Texas)")
        print("  --all: Generate pages for all 50 states")
