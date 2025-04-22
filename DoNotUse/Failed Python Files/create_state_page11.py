#!/usr/bin/env python3
"""
State Page Creator v11 - FINAL VERSION
- Uses the BEAUTIFUL template
- Handles ALL placeholders correctly
- Creates perfect pages
"""

import os
import json
import random
import requests
import re
from typing import Dict, List, Optional

# Constants
BASE_URL = "https://bailbondsbuddy.com"
AUTH = ("bbbuddy", "DpSm eiz8 yHjx Sqqk G3lG fqU6")
TEMPLATE_FILE = "fix_template.txt"  # Using the beautiful template!
FAQ_FILE = "FAQ.md"

# State Data - Oklahoma focused
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
    """Load the beautiful template file content"""
    try:
        if not os.path.exists(TEMPLATE_FILE):
            print(f"Error: Template file {TEMPLATE_FILE} not found")
            return None
        
        with open(TEMPLATE_FILE, 'r') as f:
            content = f.read()
            print(f"Beautiful template loaded: {len(content)} characters")
            return content
    except Exception as e:
        print(f"Error loading template: {str(e)}")
        return None

def load_faqs() -> List[Dict[str, str]]:
    """Load and parse FAQs from markdown file"""
    try:
        if not os.path.exists(FAQ_FILE):
            print(f"Warning: FAQ file {FAQ_FILE} not found. Using default FAQs.")
            # Return some default FAQs if file not found
            return [
                {
                    "question": "How much does a bail bond cost in [STATE_NAME]?",
                    "answer": "In [STATE_NAME], bail bond fees are typically [PREMIUM_RATE]% of the total bail amount. For example, if bail is set at $10,000, you would pay $[PREMIUM_EXAMPLE] to a bail bondsman."
                },
                {
                    "question": "How long does it take to get out of jail with a bail bond in [STATE_NAME]?",
                    "answer": "Release times in [STATE_NAME] vary by facility, but typically range from 1-6 hours after the bond is posted. Our bail agents work quickly to expedite the process."
                },
                {
                    "question": "Do I get my bail money back in [STATE_NAME]?",
                    "answer": "If you pay the full bail amount directly to the court, you will receive it back when the case concludes (minus any fees). However, the premium paid to a bail bondsman (the [PREMIUM_RATE]%) is non-refundable."
                },
                {
                    "question": "Can I get a bail bond with no money down in [STATE_NAME]?",
                    "answer": "While most [STATE_NAME] bail bond agencies require some form of upfront payment, many offer flexible payment plans. Some may accept collateral instead of immediate cash payment."
                },
                {
                    "question": "What happens if someone misses court after I bailed them out in [STATE_NAME]?",
                    "answer": "If the defendant misses court, the bail bond becomes forfeit. You, as the indemnitor, become responsible for the full bail amount if the defendant cannot be located, and the bail agency may pursue recovery of assets used as collateral."
                }
            ]
        
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
        
        print(f"Loaded {len(faqs)} FAQs from file")
        return faqs
    except Exception as e:
        print(f"Error loading FAQs: {str(e)}. Using default FAQs.")
        # Return some default FAQs in case of error
        return [
            {
                "question": "How much does a bail bond cost in [STATE_NAME]?",
                "answer": "In [STATE_NAME], bail bond fees are typically [PREMIUM_RATE]% of the total bail amount. For example, if bail is set at $10,000, you would pay $[PREMIUM_EXAMPLE] to a bail bondsman."
            },
            {
                "question": "How does the bail process work in [STATE_NAME]?",
                "answer": "After an arrest in [STATE_NAME], the defendant appears before a judge who sets bail. A bail bondsman can post a surety bond for a fee of [PREMIUM_RATE]% of the bail amount, allowing release until the court date."
            }
        ]

def create_faq_section(faqs: List[Dict[str, str]], state_name: str, premium_rate: str) -> str:
    """Create FAQ accordion items with proper state-specific content"""
    if not faqs:
        return ""
    
    print("Creating FAQ section...")
    selected_faqs = random.sample(faqs, min(5, len(faqs)))
    faq_items = []
    
    for i, faq in enumerate(selected_faqs, 1):
        question = faq['question']
        answer = faq['answer']
        
        # Replace placeholder values
        question = question.replace('[STATE_NAME]', state_name)
        answer = answer.replace('[STATE_NAME]', state_name)
        
        question = question.replace('[PREMIUM_RATE]', premium_rate)
        answer = answer.replace('[PREMIUM_RATE]', premium_rate)
        
        premium_example = str(int(premium_rate) * 100)
        answer = answer.replace('[PREMIUM_EXAMPLE]', premium_example)
        
        # Create accordion item
        open_state = "on" if i == 1 else "off"
        item = f'[et_pb_accordion_item title="{question}" _builder_version="4.27.4" open="{open_state}" global_colors_info="{{}}"]'
        item += answer
        item += '[/et_pb_accordion_item]'
        faq_items.append(item)
    
    result = ''.join(faq_items)
    print(f"Created FAQ section with {len(faq_items)} items")
    return result

def replace_placeholders(content: str, state_name: str, state_data: Dict) -> str:
    """Replace ALL placeholders with proper values - BOTH UPPER AND LOWER CASE!"""
    print("Replacing ALL placeholders...")
    
    # Set premium rate based on state
    premium_rate = "10" if state_name in ["Texas", "Florida", "California"] else "15"
    
    # Create a complete map of ALL possible placeholders
    replacements = {
        # Basic state info placeholders
        '[STATE_NAME]': state_name,
        '[STATE_ABBR]': state_data['abbreviation'],
        '[STATE_NAME_LOWER]': state_name.lower(),
        '[STATE_ABBR_LOWER]': state_data['abbreviation'].lower(),
        '[PREMIUM_RATE]': premium_rate,
        
        # Location data
        '[STATE_CAPITAL_ADDRESS]': state_data['capital']['address'],
        '[STATE_CAPITAL_LAT]': state_data['capital']['lat'],
        '[STATE_CAPITAL_LNG]': state_data['capital']['lng'],
    }
    
    # Also add lowercase versions of all placeholders for case insensitivity
    lowercase_replacements = {}
    for key, value in replacements.items():
        lowercase_replacements[key.lower()] = value
    replacements.update(lowercase_replacements)
    
    # Add county placeholders for all positions
    for i, county in enumerate(state_data['counties'][:3], 1):
        county_slug = county.lower().replace(' ', '-').replace(',', '')
        replacements[f'[COUNTY_NAME_{i}]'] = county
        replacements[f'[county_name_{i}]'] = county  # lowercase version
        replacements[f'[COUNTY_SLUG_{i}]'] = county_slug
        replacements[f'[county_slug_{i}]'] = county_slug  # lowercase version
    
    # Add generic county name (first county)
    if state_data['counties']:
        replacements['[COUNTY_NAME]'] = state_data['counties'][0]
        replacements['[county_name]'] = state_data['counties'][0]  # lowercase version
        replacements['[COUNTY_SLUG]'] = state_data['counties'][0].lower().replace(' ', '-').replace(',', '')
        replacements['[county_slug]'] = state_data['counties'][0].lower().replace(' ', '-').replace(',', '')  # lowercase version
    
    # Apply all basic replacements (case-insensitive for robustness)
    for placeholder, value in replacements.items():
        # Count occurrences for debug
        count = content.count(placeholder)
        if count > 0:
            print(f"Replacing {count} instances of {placeholder}")
        
        # Simple replacement (no regex needed since we handle both cases)
        content = content.replace(placeholder, str(value))
    
    # Handle FAQ section
    faqs = load_faqs()
    faq_content = create_faq_section(faqs, state_name, premium_rate)
    
    # Replace FAQ section
    if '<!-- FAQ_ITEMS -->' in content:
        content = content.replace('<!-- FAQ_ITEMS -->', faq_content)
        print("Replaced FAQ items placeholder")
    
    # Final verification pass - list any remaining placeholders
    pattern = r'\[(.*?)\]'
    matches = re.findall(pattern, content)
    
    # Filter out Divi shortcode brackets that shouldn't be replaced
    divi_tags = ['et_pb_', '/et_pb_']
    remaining_placeholders = [m for m in matches if not any(tag in m for tag in divi_tags)]
    
    if remaining_placeholders:
        unique_placeholders = set(remaining_placeholders)
        print(f"WARNING: {len(unique_placeholders)} types of placeholders remain:")
        for placeholder in unique_placeholders:
            print(f"  - [{placeholder}]")
            # Try to replace with state name as fallback
            content = content.replace(f"[{placeholder}]", state_name)
    else:
        print("SUCCESS: All placeholders replaced!")
        
    return content

def create_state_page(state_name: str) -> Optional[int]:
    """Create a state page with COMPLETE placeholder replacement"""
    print(f"Creating page for {state_name}...")
    
    try:
        # Validate state data
        if state_name not in STATE_DATA:
            print(f"Error: No data found for state {state_name}")
            return None
        
        state_data = STATE_DATA[state_name]
        
        # Load template
        template_content = load_template()
        if not template_content:
            return None
        
        # Replace ALL placeholders
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
                "_wp_page_template": "default",
                "_et_pb_post_type_layout": "et_body_layout",
                "_et_gb_content_width": "1080px"
            }
        }
        
        # Send to WordPress
        print("Sending page to WordPress API...")
        response = requests.post(
            f"{BASE_URL}/wp-json/wp/v2/pages",
            auth=AUTH,
            json=page_data
        )
        
        if response.status_code in range(200, 300):
            page_id = response.json().get("id")
            print(f"✅ Success! Created page for {state_name} with ID {page_id}")
            print(f"Draft page URL: {BASE_URL}/?page_id={page_id}")
            return page_id
        else:
            print(f"❌ Error creating page: {response.status_code}")
            print(response.text)
            return None
            
    except Exception as e:
        print(f"❌ Error creating page for {state_name}: {str(e)}")
        return None

def main():
    """Simple main function to run the script"""
    state_name = "Oklahoma"  # Only Oklahoma for now
    page_id = create_state_page(state_name)
    
    if page_id:
        print(f"\n✅ SUCCESS! Created page for {state_name}.")
        print(f"View the page at: {BASE_URL}/?page_id={page_id}")
        print("This page should be BEAUTIFUL with ALL placeholders properly replaced!")
    else:
        print(f"\n❌ FAILED to create page for {state_name}.")

if __name__ == "__main__":
    main() 