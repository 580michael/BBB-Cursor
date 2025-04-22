#!/usr/bin/env python3
"""
Improved Page Generator for Bail Bonds Buddy State Pages (Part 1 of 3)

This script generates WordPress/Divi-compatible pages for all 50 states
while maintaining proper formatting and creating unique content.

Usage:
  python3 improved_page_generator_v2.py --test    # Test with Texas or other state 
  python3 improved_page_generator_v2.py --all     # Generate all state pages
"""

import os
import json
import re
import argparse
import random
from content_generator_utils_part1 import generate_unique_intro_paragraph, generate_unique_guide_paragraph
from string import Template

# Constants
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_FILE = os.path.join(BASE_DIR, "State-Template-Page-Only-Variables.json")
OUTPUT_DIR = os.path.join(BASE_DIR, "generated_pages")
STATE_DATA_DIR = os.path.join(os.path.dirname(__file__), "state_data")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

# Create output directories if they don't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(STATE_DATA_DIR, exist_ok=True)
os.makedirs(TEMPLATES_DIR, exist_ok=True)

def load_template(template_name=None):
    """Load a template file"""
    if template_name is None:
        # Load the default state template JSON
        try:
            with open(TEMPLATE_FILE, 'r') as f:
                template_json = json.load(f)
            print("State template loaded successfully")
            return template_json
        except Exception as e:
            print(f"Error loading template: {e}")
            return None
    else:
        # Load a specific HTML template
        filename = os.path.join(TEMPLATES_DIR, f"{template_name}.html")
        try:
            with open(filename, 'r') as f:
                return Template(f.read())
        except FileNotFoundError:
            print(f"Error: Template file {template_name} not found at {filename}")
            return None

def load_state_data(state_name):
    """Load data for a specific state"""
    filename = os.path.join(STATE_DATA_DIR, f"{state_name.lower().replace(' ', '_')}.json")
    try:
        with open(filename, 'r') as f:
            state_data = json.load(f)
        return state_data
    except FileNotFoundError:
        print(f"Error: Data file for {state_name} not found at {filename}")
        return None

def generate_sample_state_data(state_name):
    """Generate sample data for a state (used for testing)"""
    if state_name.lower() == "texas":
        return {
            "name": "Texas",
            "abbreviation": "TX",
            "nickname": "Lone Star State",
            "capital": "Austin",
            "population": "29 million",
            "num_counties": "254",
            "largest_counties": [
                "Harris County",
                "Dallas County",
                "Tarrant County"
            ],
            "major_cities": [
                "Houston",
                "Dallas",
                "San Antonio"
            ],
            "lat": "31.9686",
            "lng": "-99.9018",
            "economic_info": "Texas's economy has traditionally centered around energy production and technology, with oil and natural gas remaining significant industries. However, recent economic diversification has expanded into aerospace, biotechnology, telecommunications, and healthcare.",
            "bail_system": "The state maintains a robust bail system governed by the Texas Occupations Code Chapter 1704 (Bail Bond Sureties), which requires all bondsmen to be licensed through the Texas Department of Insurance.",
            "criminal_justice": "Recent criminal justice reform initiatives in Texas have aimed to reduce the state's historically high incarceration rate. These reforms have modified certain bail procedures, especially for non-violent offenses.",
            "geography": "Texas's geographical positioning along major interstate highways (I-35, I-10, and I-20) has unfortunately made it a corridor for drug trafficking, resulting in significant numbers of drug-related arrests requiring bail services.",
            "weather": "Weather emergencies, from hurricanes along the Gulf Coast to severe storms and flooding, can occasionally impact court schedules and bail processing timelines."
        }
    return {}

def replace_state_references(content, old_state, new_state):
    """Replace all references to the old state with the new state"""
    if not isinstance(content, str):
        return content
    
    # Replace state name with proper capitalization
    content = re.sub(r'\b' + re.escape(old_state) + r'\b', new_state, content, flags=re.IGNORECASE)
    
    # Replace state abbreviation
    old_abbr = "OK"
    new_abbr = new_state[:2].upper()
    content = re.sub(r'\b' + re.escape(old_abbr) + r'\b', new_abbr, content)
    
    return content

def replace_county_references(content, old_counties, new_counties):
    """Replace county references"""
    if not isinstance(content, str):
        return content
    
    for i, old_county in enumerate(old_counties):
        if i < len(new_counties):
            content = re.sub(r'\b' + re.escape(old_county) + r'\b', new_counties[i], content, flags=re.IGNORECASE)
    
    return content

def replace_city_references(content, old_cities, new_cities):
    """Replace city references"""
    if not isinstance(content, str):
        return content
    
    for i, old_city in enumerate(old_cities):
        if i < len(new_cities):
            content = re.sub(r'\b' + re.escape(old_city) + r'\b', new_cities[i], content, flags=re.IGNORECASE)
    
    return content

def replace_nickname_references(content, old_nickname, new_nickname):
    """Replace state nickname references"""
    if not isinstance(content, str):
        return content
    
    content = re.sub(r'\b' + re.escape(old_nickname) + r'\b', new_nickname, content, flags=re.IGNORECASE)
    return content

def replace_population_references(content, old_population, new_population):
    """Replace population references"""
    if not isinstance(content, str):
        return content
    
    content = re.sub(r'\b' + re.escape(old_population) + r'\b', new_population, content, flags=re.IGNORECASE)
    return content

def save_state_page(state_name, content, format='html'):
    """Save generated page content to file"""
    ext = 'html' if format == 'html' else 'json'
    filename = os.path.join(OUTPUT_DIR, f"{state_name.lower().replace(' ', '_')}.{ext}")
    
    try:
        print(f"DEBUG save_state_page: Content keys = {content.keys() if isinstance(content, dict) else 'Not a dict'}")
        
        with open(filename, 'w') as f:
            if format == 'json':
                json.dump(content, f, indent=2)
            else:
                # Generate HTML preview
                title = f"{state_name} Bail Bondsman"
                page_content = ""
                
                # Extract content from WordPress/Divi JSON structure
                if isinstance(content, dict) and "data" in content:
                    # The actual content is in data key, usually with a numeric key
                    data_keys = content["data"].keys()
                    if data_keys:
                        first_key = list(data_keys)[0]
                        page_content = content["data"][first_key]
                        print(f"DEBUG save_state_page: Found content in data[{first_key}]")
                
                print(f"DEBUG save_state_page: Title = {title}")
                print(f"DEBUG save_state_page: Page content length = {len(str(page_content)) if page_content else 0}")
                
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
        {page_content}
    </div>
</body>
</html>"""
                f.write(html)
        print(f"{format.upper()} content for {state_name} saved to {filename}")
        return True
    except Exception as e:
        print(f"Error saving {format} content: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    # Process all states
    state_files = [f for f in os.listdir(STATE_DATA_DIR) if f.endswith('.json')]
    for state_file in state_files:
        state_name = state_file.replace('.json', '').replace('_', ' ').title()
        print(f"Processing {state_name}...")
        state_data = load_state_data(state_name)
        if state_data:
            html_content = generate_page_content(state_data)
            save_state_page(state_name, html_content, 'html')
            json_content = generate_json_content(state_data)
            save_state_page(state_name, json_content, 'json')

if __name__ == "__main__":
    main()
