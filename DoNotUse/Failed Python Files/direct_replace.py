#!/usr/bin/env python3
"""
DIRECT STRING REPLACEMENT SCRIPT
- No JSON parsing at all
- No regex complexity
- Just raw string replacements
"""

import os
import requests
import random
from typing import Dict, List

# Constants
BASE_URL = "https://bailbondsbuddy.com"
AUTH = ("bbbuddy", "DpSm eiz8 yHjx Sqqk G3lG fqU6")
JSON_TEMPLATE_FILE = "BailBondsBuddy.com _ Find Local Trusted Bail Bondsman in [state].json"
FAQ_FILE = "FAQ.md"

# Oklahoma data
STATE_DATA = {
    "name": "Oklahoma",
    "abbreviation": "OK",
    "capital_address": "Oklahoma City, OK",
    "capital_lat": "35.4676",
    "capital_lng": "-97.5164",
    "counties": ["Oklahoma County", "Tulsa County", "Cleveland County"],
    "cities": ["Oklahoma City", "Tulsa", "Norman", "Edmond", "Lawton"],
    "premium_rate": "15"
}

def load_raw_template() -> str:
    """Load raw template file as a string"""
    with open(JSON_TEMPLATE_FILE, 'r') as f:
        content = f.read()
    
    # Extract just the HTML content, ignoring JSON structure
    start_marker = '"data": {'
    end_marker = '}}'
    
    start_pos = content.find(start_marker) + len(start_marker)
    end_pos = content.rfind(end_marker)
    
    if start_pos > 0 and end_pos > start_pos:
        # Extract the inner content
        inner_content = content[start_pos:end_pos]
        
        # Find the first colon and extract content after it
        colon_pos = inner_content.find(':')
        if colon_pos > 0:
            html_content = inner_content[colon_pos+1:]
            
            # Clean up the content
            html_content = html_content.strip()
            if html_content.startswith('"'):
                html_content = html_content[1:]
            if html_content.endswith('"'):
                html_content = html_content[:-1]
            
            # Unescape the content
            html_content = html_content.replace('\\"', '"')
            html_content = html_content.replace('\\n', '\n')
            
            print(f"Extracted raw content: {len(html_content)} characters")
            return html_content
    
    print("Couldn't extract content from file - falling back to read entire file")
    return content

def load_faqs() -> List[Dict[str, str]]:
    """Load FAQs from file"""
    try:
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
                "question": "How much does a bail bond cost in Oklahoma?",
                "answer": "In Oklahoma, bail bond fees are typically 15% of the total bail amount. For example, if bail is set at $10,000, you would pay $150 to a bail bondsman."
            },
            {
                "question": "How does the bail process work in Oklahoma?",
                "answer": "After an arrest in Oklahoma, the defendant appears before a judge who sets bail. A bail bondsman can post a surety bond for a fee of 15% of the bail amount, allowing release until the court date."
            }
        ]

def create_faq_content(faqs: List[Dict[str, str]], state_name: str, premium_rate: str) -> List[Dict[str, str]]:
    """Create FAQ content for insertion"""
    selected_faqs = random.sample(faqs, min(5, len(faqs)))
    
    # Replace placeholders in FAQs
    processed_faqs = []
    for faq in selected_faqs:
        question = faq['question'].replace('[state_name]', state_name)
        question = question.replace('[STATE_NAME]', state_name)
        
        answer = faq['answer'].replace('[state_name]', state_name)
        answer = answer.replace('[STATE_NAME]', state_name)
        
        answer = answer.replace('[premium_rate]', premium_rate)
        answer = answer.replace('[PREMIUM_RATE]', premium_rate)
        
        premium_example = str(int(premium_rate) * 100)
        answer = answer.replace('[premium_example]', premium_example)
        
        processed_faqs.append({
            'question': question,
            'answer': answer
        })
    
    return processed_faqs

def create_page_for_state() -> None:
    """Create a page with direct string replacements"""
    # Load the template
    content = load_raw_template()
    
    # Load and prepare FAQs
    faqs = load_faqs()
    processed_faqs = create_faq_content(faqs, STATE_DATA['name'], STATE_DATA['premium_rate'])
    
    # DIRECT replacements - with explicit strings
    replacements = [
        # State info
        ('[state_name]', STATE_DATA['name']),
        ('[STATE_NAME]', STATE_DATA['name']),
        ('[state]', STATE_DATA['name']),
        ('[State_Name]', STATE_DATA['name']),
        ('Major Counties in [state_name]', f"Major Counties in {STATE_DATA['name']}"),
        ('Major Counties in [STATE_NAME]', f"Major Counties in {STATE_DATA['name']}"),
        
        # Abbreviation
        ('[state_abbr]', STATE_DATA['abbreviation']),
        ('[STATE_ABBR]', STATE_DATA['abbreviation']),
        ('[state_abbr_lower]', STATE_DATA['abbreviation'].lower()),
        ('[STATE_ABBR_LOWER]', STATE_DATA['abbreviation'].lower()),
        
        # Lowercase
        ('[state_name_lower]', STATE_DATA['name'].lower()),
        ('[STATE_NAME_LOWER]', STATE_DATA['name'].lower()),
        
        # Capital info
        ('[state_capital_address]', STATE_DATA['capital_address']),
        ('[STATE_CAPITAL_ADDRESS]', STATE_DATA['capital_address']),
        ('[state_capital_lat]', STATE_DATA['capital_lat']),
        ('[STATE_CAPITAL_LAT]', STATE_DATA['capital_lat']),
        ('[state_capital_lng]', STATE_DATA['capital_lng']),
        ('[STATE_CAPITAL_LNG]', STATE_DATA['capital_lng']),
        
        # Premium rate
        ('[premium_rate]', STATE_DATA['premium_rate']),
        ('[PREMIUM_RATE]', STATE_DATA['premium_rate']),
        
        # County names with indexes
        ('[county_name_1]', STATE_DATA['counties'][0] if len(STATE_DATA['counties']) > 0 else "County"),
        ('[COUNTY_NAME_1]', STATE_DATA['counties'][0] if len(STATE_DATA['counties']) > 0 else "County"),
        ('[county_name_2]', STATE_DATA['counties'][1] if len(STATE_DATA['counties']) > 1 else "County"),
        ('[COUNTY_NAME_2]', STATE_DATA['counties'][1] if len(STATE_DATA['counties']) > 1 else "County"),
        ('[county_name_3]', STATE_DATA['counties'][2] if len(STATE_DATA['counties']) > 2 else "County"),
        ('[COUNTY_NAME_3]', STATE_DATA['counties'][2] if len(STATE_DATA['counties']) > 2 else "County"),
        
        # Generic county names
        ('[county_name]', STATE_DATA['counties'][0] if len(STATE_DATA['counties']) > 0 else "County"),
        ('[COUNTY_NAME]', STATE_DATA['counties'][0] if len(STATE_DATA['counties']) > 0 else "County"),
        
        # County slugs
        ('[county_slug_1]', STATE_DATA['counties'][0].lower().replace(' ', '-').replace(',', '') if len(STATE_DATA['counties']) > 0 else "county"),
        ('[COUNTY_SLUG_1]', STATE_DATA['counties'][0].lower().replace(' ', '-').replace(',', '') if len(STATE_DATA['counties']) > 0 else "county"),
        ('[county_slug_2]', STATE_DATA['counties'][1].lower().replace(' ', '-').replace(',', '') if len(STATE_DATA['counties']) > 1 else "county"),
        ('[COUNTY_SLUG_2]', STATE_DATA['counties'][1].lower().replace(' ', '-').replace(',', '') if len(STATE_DATA['counties']) > 1 else "county"),
        ('[county_slug_3]', STATE_DATA['counties'][2].lower().replace(' ', '-').replace(',', '') if len(STATE_DATA['counties']) > 2 else "county"),
        ('[COUNTY_SLUG_3]', STATE_DATA['counties'][2].lower().replace(' ', '-').replace(',', '') if len(STATE_DATA['counties']) > 2 else "county"),
        
        # Other state text replacements
        ('[state_name], from', f"{STATE_DATA['name']}, from"),
        ('in [state_name],', f"in {STATE_DATA['name']},"),
        ('in [state_name].', f"in {STATE_DATA['name']}."),
        ('in [state_name]', f"in {STATE_DATA['name']}"),
        
        # FAQ placeholders
        ('[FAQ_SECTION]', ''),
        ('[FAQ_ITEMS]', '')
    ]
    
    # Apply all replacements
    print(f"Starting replacements on content ({len(content)} characters)")
    for old, new in replacements:
        if old in content:
            count = content.count(old)
            content = content.replace(old, new)
            print(f"Replaced {count} occurrences of '{old}' with '{new}'")
    
    # Handle FAQ questions and answers individually
    for i, faq in enumerate(processed_faqs, 1):
        question_placeholder = f'[FAQ_QUESTION_{i}]'
        answer_placeholder = f'[FAQ_ANSWER_{i}]'
        
        if question_placeholder in content:
            content = content.replace(question_placeholder, faq['question'])
            print(f"Replaced FAQ question {i}")
        
        if answer_placeholder in content:
            content = content.replace(answer_placeholder, faq['answer'])
            print(f"Replaced FAQ answer {i}")
    
    # Prepare page data with ALL required meta fields
    page_data = {
        "title": f"Bail Bonds in {STATE_DATA['name']} | Licensed Bail Bonds Company",
        "slug": f"bail-bonds-in-{STATE_DATA['name'].lower().replace(' ', '-')}-{STATE_DATA['abbreviation'].lower()}",
        "content": content,
        "status": "draft",
        "meta": {
            "description": f"Find trusted bail bond agents in {STATE_DATA['name']}. 24/7 service, fast release, and affordable payment options. Licensed bail bondsmen ready to help.",
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
        print(f"✅ Success! Created page for {STATE_DATA['name']} with ID {page_id}")
        print(f"Draft page URL: {BASE_URL}/?page_id={page_id}")
        
        # Save a backup of the created content
        with open("last_content_sent.txt", "w") as f:
            f.write(content)
        print("Saved content backup to last_content_sent.txt")
    else:
        print(f"❌ Error creating page: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    create_page_for_state() 