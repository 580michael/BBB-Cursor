#!/usr/bin/env python3
"""
State Page Creator for Bail Bonds Buddy (Version 9)
BEST OF BOTH: 
- Gets the BEAUTIFUL TEMPLATE from the JSON file
- But processes placeholders like create_state_page2.py (which works)
"""

import os
import json
import random
import requests
import time
import re
from typing import Dict, List, Optional

# Constants
BASE_URL = "https://bailbondsbuddy.com"
AUTH = ("bbbuddy", "DpSm eiz8 yHjx Sqqk G3lG fqU6")
JSON_TEMPLATE_FILE = "BailBondsBuddy.com _ Find Local Trusted Bail Bondsman in [state].json"
FAQ_FILE = "FAQ.md"
TEMP_TEMPLATE_FILE = "temp_template.txt"  # Create a temporary text template file

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
    }
}

def extract_json_to_txt() -> Optional[str]:
    """Extract template from JSON and save to text file for processing"""
    try:
        if not os.path.exists(JSON_TEMPLATE_FILE):
            print(f"Error: JSON template file {JSON_TEMPLATE_FILE} not found")
            return None
        
        # Load the JSON content
        with open(JSON_TEMPLATE_FILE, 'r') as f:
            data = json.load(f)
            if "data" in data and isinstance(data["data"], dict):
                first_key = next(iter(data["data"]))
                content = data["data"][first_key]
                if content:
                    print(f"JSON template loaded: {len(content)} characters")
                    
                    # Save to temporary text file
                    with open(TEMP_TEMPLATE_FILE, 'w') as temp_f:
                        temp_f.write(content)
                    
                    print(f"Saved template to {TEMP_TEMPLATE_FILE} for processing")
                    return content
            
        print("Error: Could not extract content from JSON template")
        return None
            
    except Exception as e:
        print(f"Error extracting JSON template: {str(e)}")
        return None

def load_faqs() -> List[Dict[str, str]]:
    """Load and parse FAQs from markdown file"""
    try:
        if not os.path.exists(FAQ_FILE):
            print(f"Error: FAQ file {FAQ_FILE} not found")
            return []
        
        with open(FAQ_FILE, 'r') as f:
            content = f.read()
        
        faqs = []
        current_question = None
        current_answer = []
        
        for line in content.strip().split('\n'):
            line = line.strip()
            if line.startswith('# '):  # Skip title
                continue
            elif not line:  # Empty line marks end of QA pair
                if current_question and current_answer:
                    faqs.append({
                        'question': current_question,
                        'answer': ' '.join(current_answer)
                    })
                    current_question = None
                    current_answer = []
            elif not current_question:
                current_question = line
            else:
                current_answer.append(line)
        
        # Add last FAQ if exists
        if current_question and current_answer:
            faqs.append({
                'question': current_question,
                'answer': ' '.join(current_answer)
            })
        
        print(f"Loaded {len(faqs)} FAQs")
        return faqs
    except Exception as e:
        print(f"Error loading FAQs: {str(e)}")
        return []

def create_faq_section(faqs: List[Dict[str, str]], state_name: str) -> str:
    """Create FAQ accordion items with state-specific content"""
    if not faqs:
        return ""
    
    print("Creating FAQ section...")
    selected_faqs = random.sample(faqs, min(5, len(faqs)))
    faq_items = []
    
    for i, faq in enumerate(selected_faqs, 1):
        question = faq['question']
        answer = faq['answer']
        
        # Replace state name
        question = question.replace('[state_name]', state_name)
        answer = answer.replace('[state_name]', state_name)
        
        # Replace premium rate
        premium_rate = "10" if state_name in ["Texas", "Florida", "California"] else "15"
        question = question.replace('[premium_rate]', premium_rate)
        answer = answer.replace('[premium_rate]', premium_rate)
        
        # Calculate premium example
        premium_example = str(int(premium_rate) * 100)
        answer = answer.replace('[premium_example]', premium_example)
        
        # State specific replacements
        state_specifics = {
            "Oklahoma": {
                "recent_state_change": "recent reforms in bail procedures",
                "state_specific_factor": "county-specific bail schedules"
            }
        }
        
        # Apply state-specific replacements
        if state_name in state_specifics:
            for key, value in state_specifics[state_name].items():
                placeholder = f"[{key}]"
                answer = answer.replace(placeholder, value)
        
        # Create accordion item - Using proper Divi format for beautiful design
        open_state = "on" if i == 1 else "off"
        item = f'[et_pb_accordion_item title="{question}" _builder_version="4.27.4" open="{open_state}" global_colors_info="{{}}"]'
        item += answer
        item += '[/et_pb_accordion_item]'
        faq_items.append(item)
    
    result = ''.join(faq_items)
    print(f"Created FAQ section with {len(faq_items)} items")
    return result

def find_and_replace_all_formats(content: str, find_text: str, replace_text: str) -> str:
    """Find and replace text in all possible formats (regular, URL-encoded, HTML-encoded)"""
    # Regular format
    content = content.replace(find_text, replace_text)
    
    # URL-encoded format (%91 = [, %93 = ])
    url_encoded = find_text.replace('[', '%91').replace(']', '%93')
    content = content.replace(url_encoded, replace_text)
    
    # HTML-encoded format (&#91; = [, &#93; = ])
    html_encoded = find_text.replace('[', '&#91;').replace(']', '&#93;')
    content = content.replace(html_encoded, replace_text)
    
    return content

def replace_placeholders(content: str, state_name: str, state_data: Dict) -> str:
    """Replace all placeholders in all possible formats"""
    print("Replacing placeholders with comprehensive approach...")
    
    # Basic replacements
    replacements = {
        '[state_name]': state_name,
        '[state_abbr]': state_data['abbreviation'],
        '[state_capital_address]': state_data['capital']['address'],
        '[state_capital_lat]': state_data['capital']['lat'],
        '[state_capital_lng]': state_data['capital']['lng'],
        '[premium_rate]': "10" if state_name in ["Texas", "Florida", "California"] else "15"
    }
    
    # Add county replacements
    for i, county in enumerate(state_data['counties'][:3], 1):
        county_slug = county.lower().replace(' ', '-').replace(',', '')
        replacements[f'[county_name_{i}]'] = county
        replacements[f'[county_slug_{i}]'] = county_slug
    
    # Also add generic county_name
    if state_data['counties']:
        replacements['[county_name]'] = state_data['counties'][0]
    
    # Apply all replacements with all possible encodings
    for placeholder, value in replacements.items():
        original_count = content.count(placeholder)
        if original_count > 0:
            print(f"Found {original_count} instances of {placeholder}")
        
        # Apply replacements in all formats
        content = find_and_replace_all_formats(content, placeholder, str(value))
    
    # Handle FAQ placeholders
    faqs = load_faqs()
    faq_content = create_faq_section(faqs, state_name)
    
    # Look for FAQ accordion section markers
    faq_markers = [
        '[et_pb_accordion', 
        '<!-- FAQ_ITEMS -->', 
        '<!-- FAQ_SECTION -->'
    ]
    
    for marker in faq_markers:
        if marker in content:
            # Find the complete accordion section
            start_idx = content.find(marker)
            if start_idx >= 0:
                # Find the end of the opening tag
                open_end_idx = content.find(']', start_idx)
                if open_end_idx >= 0:
                    # Find the closing tag
                    close_tag = '[/et_pb_accordion]'
                    close_idx = content.find(close_tag, open_end_idx)
                    if close_idx >= 0:
                        # Extract the opening tag
                        opening_tag = content[start_idx:open_end_idx+1]
                        
                        # Replace the entire accordion content
                        before = content[:open_end_idx+1]
                        after = content[close_idx:]
                        
                        # Construct new content with FAQ items
                        content = before + faq_content + after
                        print(f"Replaced FAQ accordion section using marker {marker}")
                        break
    
    # Also try direct FAQ placeholder replacement
    faq_placeholders = ['[FAQ_QUESTION_', '[FAQ_ANSWER_']
    
    for i in range(1, 6):
        for placeholder in faq_placeholders:
            question = f"How does the bail process work in {state_name}? (Question {i})"
            answer = f"The bail process in {state_name} involves posting a bond through a licensed bail bondsman who charges a premium fee (typically 15%). (Answer {i})"
            
            # Apply replacements based on placeholder type
            if 'QUESTION' in placeholder:
                content = find_and_replace_all_formats(content, f"{placeholder}{i}]", question)
            else:
                content = find_and_replace_all_formats(content, f"{placeholder}{i}]", answer)
    
    # Final pass to check for leftover placeholders
    pattern = r'\[([^\]]+)\]'
    matches = re.findall(pattern, content)
    if matches:
        print(f"WARNING: Found {len(matches)} remaining placeholders after replacement")
        for match in matches[:5]:  # Show first 5
            if not match.startswith('et_pb_') and not match.startswith('/et_pb_'):
                print(f"  - [{match}]")
                # Try one more replacement with state name as fallback
                content = content.replace(f"[{match}]", state_name)
    
    return content

def create_state_page(state_name: str) -> Optional[int]:
    """Create a new state page with the specified content"""
    print(f"Creating page for {state_name}...")
    
    try:
        # Validate state data
        state_data = STATE_DATA.get(state_name)
        if not state_data:
            print(f"Error: No data found for state {state_name}")
            return None
        
        # Extract JSON template to txt for processing
        template_content = extract_json_to_txt()
        if not template_content:
            return None
        
        # Replace placeholders
        content = replace_placeholders(template_content, state_name, state_data)
        
        # Prepare page data with ALL required meta fields
        page_data = {
            "title": f"Bail Bonds in {state_name} | Licensed Bail Bonds Company",
            "slug": f"bail-bonds-in-{state_name.lower().replace(' ', '-')}-{state_data['abbreviation'].lower()}",
            "content": content,
            "status": "draft",
            "meta": {
                "description": f"Find trusted bail bond agents in {state_name}. 24/7 service, fast release, and affordable payment options. Licensed bail bondsmen ready to help.",
                "_et_pb_use_builder": "on",
                "_et_pb_page_layout": "et_no_sidebar",
                "_et_pb_side_nav": "off",
                "_wp_page_template": "page-template-blank.php",
                "_et_pb_post_type_layout": "custom_body",
                "_et_gb_content_width": "1080px"
            }
        }
        
        # Create page
        print("Sending page to WordPress...")
        response = requests.post(
            f"{BASE_URL}/wp-json/wp/v2/pages",
            auth=AUTH,
            json=page_data
        )
        
        if response.status_code in range(200, 300):
            page_id = response.json().get("id")
            print(f"Successfully created page for {state_name} with ID {page_id}")
            print(f"Draft page URL: {BASE_URL}/?page_id={page_id}")
            return page_id
        else:
            print(f"Error creating page: {response.status_code}")
            print(response.text)
            return None
            
    except Exception as e:
        print(f"Error creating page for {state_name}: {str(e)}")
        return None

def main():
    """Main function to run the script"""
    state_name = "Oklahoma"  # Can be changed to any state in STATE_DATA
    create_state_page(state_name)

if __name__ == "__main__":
    main() 