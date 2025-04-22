#!/usr/bin/env python3
"""
State Page Creator for Bail Bonds Buddy (Version 6)
Final version with extremely aggressive placeholder replacement
"""

import os
import json
import random
import requests
import re
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
                    print(f"Template loaded: {len(content)} characters")
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
        
        print(f"Loaded {len(faqs)} FAQs")
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
        
        # Create accordion item without double braces to avoid issues
        open_state = "on" if i == 1 else "off"
        item = f'[et_pb_accordion_item title="{question}" _builder_version="4.27.4" open="{open_state}" global_colors_info="{{}}"]'
        item += answer
        item += '[/et_pb_accordion_item]'
        faq_items.append(item)
    
    return ''.join(faq_items)

def find_all_patterns(content: str) -> List[str]:
    """Find all possible placeholder patterns in the content"""
    patterns = []
    
    # Find regular [placeholder] patterns
    regular_pattern = r'\[([^\]]+)\]'
    regular_matches = re.findall(regular_pattern, content)
    patterns.extend([f"[{m}]" for m in regular_matches if not m.startswith('et_pb_') and not m.startswith('/et_pb_')])
    
    # Find URL-encoded %91placeholder%93 patterns
    url_pattern = r'%91([^%]+)%93'
    url_matches = re.findall(url_pattern, content)
    patterns.extend([f"%91{m}%93" for m in url_matches])
    
    # Find HTML-encoded &#91;placeholder&#93; patterns
    html_pattern = r'&#91;([^&]+)&#93;'
    html_matches = re.findall(html_pattern, content)
    patterns.extend([f"&#91;{m}&#93;" for m in html_matches])
    
    return patterns

def exhaustive_replacements(content: str, state_name: str, state_data: Dict) -> str:
    """
    Extremely aggressive approach to replace all placeholders
    """
    print("Starting aggressive placeholder replacement...")
    
    # First identify all patterns in the content
    all_patterns = find_all_patterns(content)
    custom_patterns = [p for p in all_patterns if 'state_name' in p.lower() or 'county_name' in p.lower() or 'faq' in p.lower()]
    print(f"Found {len(all_patterns)} total patterns, {len(custom_patterns)} relevant patterns")
    
    # 1. Replace all state_name variations
    print("Replacing state name patterns...")
    content = re.sub(r'\[state_name\]', state_name, content, flags=re.IGNORECASE)
    content = re.sub(r'%91state_name%93', state_name, content, flags=re.IGNORECASE)
    content = re.sub(r'&#91;state_name&#93;', state_name, content, flags=re.IGNORECASE)
    
    # 2. Replace all county_name variations with looping
    print("Replacing county name patterns...")
    counties = state_data['counties']
    
    # Handle numbered county_name placeholders
    for i, county in enumerate(counties[:3], 1):
        county_slug = county.lower().replace(' ', '-').replace(',', '')
        
        # Regular formats
        content = re.sub(f'\\[county_name_{i}\\]', county, content, flags=re.IGNORECASE)
        content = re.sub(f'\\[county_slug_{i}\\]', county_slug, content, flags=re.IGNORECASE)
        
        # URL-encoded formats
        content = re.sub(f'%91county_name_{i}%93', county, content, flags=re.IGNORECASE)
        content = re.sub(f'%91county_slug_{i}%93', county_slug, content, flags=re.IGNORECASE)
        
        # HTML-encoded formats
        content = re.sub(f'&#91;county_name_{i}&#93;', county, content, flags=re.IGNORECASE)
        content = re.sub(f'&#91;county_slug_{i}&#93;', county_slug, content, flags=re.IGNORECASE)
    
    # Also replace generic [county_name] with first county
    if counties:
        first_county = counties[0]
        content = re.sub(r'\[county_name\]', first_county, content, flags=re.IGNORECASE)
        content = re.sub(r'%91county_name%93', first_county, content, flags=re.IGNORECASE)
        content = re.sub(r'&#91;county_name&#93;', first_county, content, flags=re.IGNORECASE)
    
    # 3. Replace all other basic placeholders
    print("Replacing other placeholders...")
    replacements = {
        '[state_abbr]': state_data['abbreviation'],
        '[state_capital_address]': state_data['capital']['address'],
        '[state_capital_lat]': state_data['capital']['lat'],
        '[state_capital_lng]': state_data['capital']['lng'],
        '[premium_rate]': "10" if state_name in ["Texas", "Florida", "California"] else "15"
    }
    
    # Apply all basic replacements
    for placeholder, value in replacements.items():
        # Regular format
        content = content.replace(placeholder, str(value))
        # URL-encoded format
        url_placeholder = placeholder.replace('[', '%91').replace(']', '%93')
        content = content.replace(url_placeholder, str(value))
        # HTML-encoded format
        html_placeholder = placeholder.replace('[', '&#91;').replace(']', '&#93;')
        content = content.replace(html_placeholder, str(value))
    
    # 4. Handle FAQs - completely rebuild the accordion section
    print("Handling FAQ section...")
    faqs = load_faqs()
    faq_content = create_faq_section(faqs, state_name)
    
    # Replace entire FAQ accordion section if possible
    start_marker = '[et_pb_accordion'
    end_marker = '[/et_pb_accordion]'
    
    if start_marker in content and end_marker in content:
        # Find the start of the accordion section
        start_idx = content.find(start_marker)
        # Find the end of the attributes part
        start_content_idx = content.find(']', start_idx)
        # Find the end of the accordion section
        end_idx = content.find(end_marker, start_content_idx) + len(end_marker)
        
        # Extract the accordion attributes from the original content
        accordion_attrs = content[start_idx:start_content_idx+1]
        
        # Reconstruct with new FAQ content
        before_content = content[:start_idx]
        after_content = content[end_idx:]
        
        # Create a completely new accordion section
        new_section = accordion_attrs + faq_content + end_marker
        content = before_content + new_section + after_content
        print("Replaced FAQ accordion section")
    
    # 5. Also replace individual FAQ_QUESTION and FAQ_ANSWER placeholders
    print("Replacing individual FAQ placeholders...")
    for i in range(1, 6):
        default_question = f"How does the bail process work in {state_name}? (Question {i})"
        default_answer = f"The bail process in {state_name} involves posting a bond through a licensed bail bondsman who charges a premium fee (typically 15%). (Answer {i})"
        
        # Regular format
        content = content.replace(f'[FAQ_QUESTION_{i}]', default_question)
        content = content.replace(f'[FAQ_ANSWER_{i}]', default_answer)
        # URL-encoded format
        content = content.replace(f'%91FAQ_QUESTION_{i}%93', default_question)
        content = content.replace(f'%91FAQ_ANSWER_{i}%93', default_answer)
        # HTML-encoded format
        content = content.replace(f'&#91;FAQ_QUESTION_{i}&#93;', default_question)
        content = content.replace(f'&#91;FAQ_ANSWER_{i}&#93;', default_answer)
    
    # Also replace non-numbered FAQ_QUESTION and FAQ_ANSWER
    default_question = f"How does the bail process work in {state_name}?"
    default_answer = f"The bail process in {state_name} involves posting a bond through a licensed bail bondsman who charges a premium fee (typically 15%)."
    
    # Regular format
    content = content.replace('[FAQ_QUESTION]', default_question)
    content = content.replace('[FAQ_ANSWER]', default_answer)
    # URL-encoded format
    content = content.replace('%91FAQ_QUESTION%93', default_question)
    content = content.replace('%91FAQ_ANSWER%93', default_answer)
    # HTML-encoded format
    content = content.replace('&#91;FAQ_QUESTION&#93;', default_question)
    content = content.replace('&#91;FAQ_ANSWER&#93;', default_answer)
    
    # 6. Check for any remaining [placeholder] patterns and replace them
    remaining_patterns = find_all_patterns(content)
    print(f"After primary replacements, {len(remaining_patterns)} patterns remain")
    
    # Replace any remaining placeholders with generic text
    for pattern in remaining_patterns:
        if 'state' in pattern.lower():
            content = content.replace(pattern, state_name)
        elif 'county' in pattern.lower():
            content = content.replace(pattern, counties[0] if counties else "County")
        elif 'question' in pattern.lower():
            content = content.replace(pattern, default_question)
        elif 'answer' in pattern.lower():
            content = content.replace(pattern, default_answer)
        elif 'capital' in pattern.lower():
            content = content.replace(pattern, state_data['capital']['name'])
        else:
            # Generic replacement for anything else
            clean_pattern = pattern.replace('[', '').replace(']', '').replace('%91', '').replace('%93', '')
            content = content.replace(pattern, f"{state_name} {clean_pattern}")
    
    # Final check
    final_patterns = find_all_patterns(content)
    print(f"Final placeholder count: {len(final_patterns)}")
    if final_patterns:
        print("REMAINING PATTERNS:")
        for p in final_patterns:
            print(f"  {p}")
    
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
        content = exhaustive_replacements(template_content, state_name, state_data)
        
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