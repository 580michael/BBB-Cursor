#!/usr/bin/env python3
"""
State Page Creator for Bail Bonds Buddy
Creates state pages using the Divi Theme Builder 'All States Pages' template.
"""

import requests
import random
import os
import json
import time
import traceback
import re # Import regex for more complex replacements

# Constants
BASE_URL = "https://bailbondsbuddy.com"
API_URL = f"{BASE_URL}/wp-json/v2"
AUTH = ("bbbuddy", "DpSm eiz8 yHjx Sqqk G3lG fqU6")
# Changed to JSON template file
TEMPLATE_FILE_PATH = "BailBondsBuddy.com _ Find Local Trusted Bail Bondsman in [state].json"
FAQ_FILE_PATH = "FAQ.md" # Added constant for FAQ file

# State Data
STATE_DATA = {
    "Oklahoma": {
        "abbreviation": "OK",
        "capital": {
            "name": "Oklahoma City",
            "address": "Oklahoma City, OK",
            "lat": "35.4676",
            "lng": "-97.5164"
        },
        "counties": ["Oklahoma County", "Tulsa County", "Cleveland County"],
        "sample_cities": ["Oklahoma City", "Tulsa", "Norman", "Edmond", "Lawton"]
    },
    "Texas": {
        "abbreviation": "TX",
        "capital": {
            "name": "Austin",
            "address": "Austin, TX",
            "lat": "30.2672",
            "lng": "-97.7431"
        },
        "counties": ["Harris County", "Dallas County", "Bexar County"],
        "sample_cities": ["Houston", "Dallas", "San Antonio", "Austin", "Fort Worth"]
    },
    "Florida": {
        "abbreviation": "FL",
        "capital": {
            "name": "Tallahassee",
            "address": "Tallahassee, FL",
            "lat": "30.4383",
            "lng": "-84.2807"
        },
        "counties": ["Miami-Dade County", "Broward County", "Palm Beach County"],
        "sample_cities": ["Miami", "Orlando", "Tampa", "Jacksonville", "Fort Lauderdale"]
    }
    # Add more states as needed
}

def load_faqs():
    """
    Load FAQs from the FAQ.md file
    """
    try:
        if not os.path.exists(FAQ_FILE_PATH):
            print(f"Error: {FAQ_FILE_PATH} not found")
            return []
        
        with open(FAQ_FILE_PATH, "r") as f:
            content = f.read()
        
        # Parse questions and answers
        faqs = []
        lines = content.strip().split("\n")
        
        # Skip the title line
        current_question = None
        current_answer = ""
        
        for line in lines[1:]:
            line = line.strip()
            if not line:
                # Empty line separates Q&A
                if current_question and current_answer:
                    faqs.append({
                        "question": current_question,
                        "answer": current_answer.strip()
                    })
                    current_question = None
                    current_answer = ""
            elif not current_question:
                # This is a question
                current_question = line
            else:
                # This is part of the answer
                current_answer += line + " "
        
        # Add the last FAQ if it exists
        if current_question and current_answer:
            faqs.append({
                "question": current_question,
                "answer": current_answer.strip()
            })
        
        return faqs
    except Exception as e:
        print(f"Error loading FAQs: {str(e)}")
        return []

def select_random_faqs(faqs, state_name, count=5):
    """
    Select random FAQs and customize them for the state
    """
    if len(faqs) <= count:
        selected_faqs = faqs
    else:
        selected_faqs = random.sample(faqs, count)
    
    # Customize FAQs with state information
    customized_faqs = []
    for faq in selected_faqs:
        question = faq["question"]
        answer = faq["answer"]
        
        # Replace state name
        question = question.replace("[state_name]", state_name)
        answer = answer.replace("[state_name]", state_name)
        
        # Replace premium rate (10% for TX, FL, CA; 15% for others)
        premium_rate = "10" if state_name in ["Texas", "Florida", "California"] else "15"
        question = question.replace("[premium_rate]", premium_rate)
        answer = answer.replace("[premium_rate]", premium_rate)
        
        # Calculate premium example (e.g., $1,000 for 10%)
        premium_example = str(int(premium_rate) * 100)
        answer = answer.replace("[premium_example]", premium_example)
        
        # State specific replacements
        state_specifics = {
            "Oklahoma": {
                "recent_state_change": "recent reforms in bail procedures",
                "state_specific_factor": "county-specific bail schedules"
            },
            "Texas": {
                "recent_state_change": "the 2021 bail reform legislation",
                "state_specific_factor": "different county bail practices"
            },
            "Florida": {
                "recent_state_change": "updated pretrial release guidelines",
                "state_specific_factor": "varying bail schedules by judicial circuit"
            }
        }
        
        # Apply state-specific replacements if available
        if state_name in state_specifics:
            for key, value in state_specifics[state_name].items():
                placeholder = f"[{key}]"
                answer = answer.replace(placeholder, value)
        
        customized_faqs.append({
            "question": question,
            "answer": answer
        })
    
    return customized_faqs

def format_title(state_name):
    """Create a properly formatted page title"""
    return f"Bail Bonds in {state_name} | Licensed Bail Bonds Company"

def create_slug(state_name):
    """Create a URL slug for the page"""
    abbr = STATE_DATA.get(state_name, {}).get("abbreviation", "").lower()
    # Ensure abbreviation is present for slug creation
    if not abbr:
        print(f"Warning: No abbreviation found for {state_name}. Using full name in slug.")
        return f"bail-bonds-in-{state_name.lower().replace(' ', '-')}"
    return f"bail-bonds-in-{state_name.lower().replace(' ', '-')}-{abbr}"

def generate_meta_description(state_name):
    """Generate a meta description for SEO"""
    templates = [
        f"Find trusted bail bond agents in {state_name}. 24/7 service, fast release, and affordable payment options. Licensed bail bondsmen ready to help.",
        f"Need a bail bondsman in {state_name}? Our professional bail bond services provide immediate assistance with jail release. Available 24/7.",
        f"{state_name} bail bond services you can trust. Our licensed agents help with quick jail release and affordable rates."
    ]
    return random.choice(templates)

def get_template_content():
    """Try both JSON and direct template loading"""
    try:
        # First try JSON template
        if os.path.exists(TEMPLATE_FILE_PATH):
            with open(TEMPLATE_FILE_PATH, 'r') as f:
                data = json.load(f)
                if "data" in data and isinstance(data["data"], dict):
                    first_key = next(iter(data["data"]))
                    content = data["data"][first_key]
                    if content:
                        return content
        
        # If JSON fails, try direct template
        template_response = requests.get(
            f"{BASE_URL}/wp-json/wp/v2/pages/870",  # Your working template page
            auth=AUTH,
            params={'context': 'edit'}
        )
        template_response.raise_for_status()
        template_data = template_response.json()
        content = template_data.get('content', {}).get('raw', '')
        
        if content:
            return content
            
        raise ValueError("Could not get content from either source")
        
    except Exception as e:
        print(f"Error getting template: {str(e)}")
        traceback.print_exc()
        return None

def replace_faq_placeholders(content, faqs):
    """Replaces FAQ placeholders in the content with actual FAQs."""
    if not faqs:
        print("No FAQs provided for replacement.")
        return content

    print(f"Replacing FAQ placeholders for {len(faqs)} FAQs...")
    for i, faq in enumerate(faqs):
        # Handle both formats for FAQ placeholders
        question_placeholders = [
            f"[FAQ_QUESTION_{i+1}]",
            f"%91FAQ_QUESTION_{i+1}%93",
            f"[FAQ_QUESTION]",
            f"%91FAQ_QUESTION%93"
        ]
        answer_placeholders = [
            f"[FAQ_ANSWER_{i+1}]",
            f"%91FAQ_ANSWER_{i+1}%93",
            f"[FAQ_ANSWER]",
            f"%91FAQ_ANSWER%93"
        ]
        
        # Replace all variations of placeholders
        for placeholder in question_placeholders:
            content = content.replace(placeholder, faq['question'])
        for placeholder in answer_placeholders:
            content = content.replace(placeholder, faq['answer'])
        print(f"Replaced FAQ {i+1}")

    return content
    
def replace_county_placeholders(content, state_name):
    """Replaces county placeholders with actual county names"""
    state_info = STATE_DATA.get(state_name)
    if not state_info:
        print(f"Warning: No state data found for {state_name} to replace counties.")
        return content
    
    counties = state_info.get("counties", [])
    if not counties:
        print(f"Warning: No counties listed for {state_name}.")
        return content

    print(f"Replacing county placeholders for {state_name}...")
    
    # Replace county names - handle both formats
    for i, county in enumerate(counties[:3]):  # Only use first 3 counties
        # Regular format
        content = content.replace(f"[county_name_{i+1}]", county)
        content = content.replace(f"[county_slug_{i+1}]", county.lower().replace(" ", "-"))
        # URL encoded format
        content = content.replace(f"%91county_name_{i+1}%93", county)
        content = content.replace(f"%91county_slug_{i+1}%93", county.lower().replace(" ", "-"))
        # Also try just [county_name]
        content = content.replace("[county_name]", county)
        content = content.replace("%91county_name%93", county)
        print(f"Replaced county placeholder with: {county}")
    
    return content

def create_state_page(state_name):
    """Create a new state page with the specified content"""
    print(f"Creating page for {state_name}...")
    
    try:
        # Get state data
        state_data = STATE_DATA.get(state_name)
        if not state_data:
            print(f"Error: No data found for state {state_name}")
            return
            
        # Get template content
        template_content = get_template_content()
        if not template_content:
            print("Error: Could not load template content")
            return
            
        print("Replacing placeholders...")
        
        # Basic state replacements
        content = template_content
        
        # Replace state name in all formats
        content = content.replace('[state_name]', state_name)
        content = content.replace('%91state_name%93', state_name)
        content = content.replace('Oklahoma', state_name)  # Replace hardcoded state name
        content = content.replace('Find Bail Bonds in [state_name]', f'Find Bail Bonds in {state_name}')
        content = content.replace('Find Licensed [state_name]', f'Find Licensed {state_name}')
        content = content.replace('[state_name] Bail Bondsmen', f'{state_name} Bail Bondsmen')
        
        # Replace state abbreviation
        content = content.replace('[state_abbr]', state_data["abbreviation"])
        content = content.replace('%91state_abbr%93', state_data["abbreviation"])
        content = content.replace('OK', state_data["abbreviation"])  # Replace hardcoded abbreviation
        
        # Replace map coordinates
        content = content.replace('Oklahoma City, OK, USA', state_data["capital"]["address"])
        content = content.replace('35.4688692', state_data["capital"]["lat"])
        content = content.replace('-97.519539', state_data["capital"]["lng"])
        
        # Replace counties
        counties = state_data.get("counties", [])
        if counties:
            content = content.replace('Oklahoma County', counties[0])
            if len(counties) > 1:
                content = content.replace('Tulsa County', counties[1])
            if len(counties) > 2:
                content = content.replace('Cleveland County', counties[2])
        
        # Load and replace FAQs
        faqs = load_faqs()
        if faqs:
            selected_faqs = select_random_faqs(faqs, state_name)
            for i, faq in enumerate(selected_faqs):
                # Replace FAQ placeholders
                content = content.replace(f'[FAQ_QUESTION_{i+1}]', faq['question'])
                content = content.replace(f'[FAQ_ANSWER_{i+1}]', faq['answer'])
                print(f"Replaced FAQ {i+1}")
        else:
            print("No FAQs provided for replacement.")
        
        print("Placeholders replaced.")
        
        # Create the page via WordPress API
        print(f"Sending API request to create DRAFT page for {state_name}...")
        
        page_data = {
            "title": format_title(state_name),
            "slug": create_slug(state_name),
            "content": content,
            "status": "draft",
            "meta": {
                "description": generate_meta_description(state_name),
                "_et_pb_page_layout": "et_no_sidebar",  # Set to full width
                "_et_pb_side_nav": "off",  # Disable side navigation
                "_et_pb_use_builder": "on",  # Enable Divi builder
                "_wp_page_template": "page-template-blank.php"  # Use blank template
            }
        }
        
        response = requests.post(
            f"{BASE_URL}/wp-json/wp/v2/pages",
            auth=AUTH,
            json=page_data
        )
        
        if 200 <= response.status_code < 300:
            page_id = response.json().get("id")
            print(f"Successfully created DRAFT page for {state_name} with ID {page_id}")
            print(f"Draft Page URL: {BASE_URL}/?page_id={page_id}\n")
            return page_id
        else:
            print(f"Error creating page: {response.status_code}")
            print(response.text)
            return None
            
    except Exception as e:
        print(f"Error creating page for {state_name}: {str(e)}")
        traceback.print_exc()
        return None

def create_pages_for_states(state_list):
    """
    Create pages for a list of states
    """
    for state_name in state_list:
        print(f"\\n--- Creating page for {state_name} ---")
        create_state_page(state_name)
        # Add a pause between requests to avoid overwhelming the API
        print("Pausing for 2 seconds...")
        time.sleep(2)

def main():
    """Main function to run the script"""
    # Create a page for Oklahoma as our test
    create_state_page("Oklahoma")
    
if __name__ == "__main__":
    main() 