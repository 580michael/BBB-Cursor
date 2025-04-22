#!/usr/bin/env python3
"""
State Page Creator for Bail Bonds Buddy (Version 2)
Creates state pages using a standardized Divi template file.
"""

import os
import json
import random
import requests
import time
from typing import Dict, List, Optional

# Constants
BASE_URL = "https://bailbondsbuddy.com"
AUTH = ("bbbuddy", "DpSm eiz8 yHjx Sqqk G3lG fqU6")
TEMPLATE_FILE = "divi_state_template.txt"
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
    },
    # Add other states as needed
}

def load_template() -> Optional[str]:
    """Load the Divi template from file"""
    try:
        if not os.path.exists(TEMPLATE_FILE):
            print(f"Error: Template file {TEMPLATE_FILE} not found")
            return None
        
        with open(TEMPLATE_FILE, 'r') as f:
            return f.read()
    except Exception as e:
        print(f"Error loading template: {str(e)}")
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
        question = faq['question'].replace('[state_name]', state_name)
        answer = faq['answer'].replace('[state_name]', state_name)
        
        # Replace premium rate
        premium_rate = "10" if state_name in ["Texas", "Florida", "California"] else "15"
        question = question.replace('[premium_rate]', premium_rate)
        answer = answer.replace('[premium_rate]', premium_rate)
        
        # Calculate premium example
        premium_example = str(int(premium_rate) * 100)
        answer = answer.replace('[premium_example]', premium_example)
        
        # Create accordion item
        open_state = "on" if i == 1 else "off"
        item = f'[et_pb_accordion_item title="{question}" _builder_version="4.27.4" open="{open_state}" global_colors_info="{{}}"]'
        item += answer
        item += '[/et_pb_accordion_item]'
        faq_items.append(item)
    
    return ''.join(faq_items)

def replace_placeholders(content: str, state_name: str, state_data: Dict) -> str:
    """Replace all placeholders in the template with actual content"""
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
        replacements[f'[county_name_{i}]'] = county
        replacements[f'[county_slug_{i}]'] = county.lower().replace(' ', '-').replace(',', '')
    
    # Replace all placeholders
    for placeholder, value in replacements.items():
        content = content.replace(placeholder, str(value))
    
    # Replace FAQ placeholder with actual FAQs
    faqs = load_faqs()
    faq_content = create_faq_section(faqs, state_name)
    content = content.replace('<!-- FAQ_ITEMS -->', faq_content)
    
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
                "_wp_page_template": "page-template-blank.php"
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
        return None

def main():
    """Main function to run the script"""
    state_name = "Oklahoma"  # Can be changed to any state in STATE_DATA
    create_state_page(state_name)

if __name__ == "__main__":
    main() 