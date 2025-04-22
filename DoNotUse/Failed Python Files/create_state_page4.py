#!/usr/bin/env python3
"""
State Page Creator for Bail Bonds Buddy (Version 4)
Combines working elements from previous versions:
- Correct formatting/styling from create_state_page3.py
- Working placeholder replacement from create_state_page2.py
"""

import os
import json
import random
import requests
import time
import traceback
from typing import Dict, List, Optional

# Constants
BASE_URL = "https://bailbondsbuddy.com"
AUTH = ("bbbuddy", "DpSm eiz8 yHjx Sqqk G3lG fqU6")
TEMPLATE_FILE = "BailBondsBuddy.com _ Find Local Trusted Bail Bondsman in [state].json"
FAQ_FILE = "FAQ.md"

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

def load_template() -> Optional[str]:
    """Load the Divi template from JSON file"""
    try:
        if not os.path.exists(TEMPLATE_FILE):
            print(f"Error: Template file {TEMPLATE_FILE} not found")
            return None
        
        with open(TEMPLATE_FILE, 'r') as f:
            data = json.load(f)
            if "data" in data and isinstance(data["data"], dict):
                first_key = next(iter(data["data"]))
                content = data["data"][first_key]
                if content:
                    return content
            
        print("Error: Could not extract content from template JSON")
        return None
            
    except Exception as e:
        print(f"Error loading template: {str(e)}")
        traceback.print_exc()
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
        
        return faqs
    except Exception as e:
        print(f"Error loading FAQs: {str(e)}")
        return []

def create_faq_section(faqs: List[Dict[str, str]], state_name: str) -> str:
    """Create FAQ accordion items with state-specific content"""
    if not faqs:
        return ""
    
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
        
        # Create accordion item
        open_state = "on" if i == 1 else "off"
        item = f'[et_pb_accordion_item title="{question}" _builder_version="4.27.4" open="{open_state}" global_colors_info="{{}}"]'
        item += answer
        item += '[/et_pb_accordion_item]'
        faq_items.append(item)
    
    return ''.join(faq_items)

def process_content_recursively(content: str, replacements: Dict[str, str]) -> str:
    """Recursively process content to handle nested placeholders"""
    previous_content = None
    current_content = content
    
    # Keep replacing until no more changes occur
    while previous_content != current_content:
        previous_content = current_content
        for placeholder, value in replacements.items():
            current_content = current_content.replace(placeholder, str(value))
    
    return current_content

def replace_placeholders(content: str, state_name: str, state_data: Dict) -> str:
    """Replace all placeholders in the template with actual content"""
    try:
        # Build comprehensive replacements dictionary
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
            replacements[f'[county_name]'] = county
        
        # First pass: Replace all basic placeholders recursively
        content = process_content_recursively(content, replacements)
        
        # Second pass: Handle FAQ section
        faqs = load_faqs()
        faq_content = create_faq_section(faqs, state_name)
        
        # Replace FAQ section
        start_marker = '[et_pb_accordion _builder_version="4.27.4"'
        end_marker = '[/et_pb_accordion]'
        
        if start_marker in content and end_marker in content:
            start_idx = content.find(start_marker)
            end_idx = content.find(end_marker) + len(end_marker)
            
            before_content = content[:start_idx + len(start_marker)]
            after_content = content[end_idx:]
            
            content = before_content + ' global_colors_info="{}" theme_builder_area="post_content"]' + faq_content + end_marker + after_content
        
        # Final pass: Catch any remaining placeholders
        content = process_content_recursively(content, replacements)
        
        return content
        
    except Exception as e:
        print(f"Error replacing placeholders: {str(e)}")
        traceback.print_exc()
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
        
        # Load template
        template_content = load_template()
        if not template_content:
            return None
        
        # Replace placeholders
        content = replace_placeholders(template_content, state_name, state_data)
        
        # Prepare page data
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
        traceback.print_exc()
        return None

def main():
    """Main function to run the script"""
    state_name = "Oklahoma"  # Can be changed to any state in STATE_DATA
    create_state_page(state_name)

if __name__ == "__main__":
    main() 