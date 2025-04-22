#!/usr/bin/env python3
"""
Extracts raw content from JSON file and processes placeholders
- Uses the EXACT JSON file content directly
- No parsing or re-serializing of JSON
- Handles replacement in raw content
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
JSON_TEMPLATE_FILE = "BailBondsBuddy.com _ Find Local Trusted Bail Bondsman in [state].json"
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

def extract_content_from_json() -> Optional[str]:
    """Extracts raw content field from JSON file without parsing full structure"""
    try:
        if not os.path.exists(JSON_TEMPLATE_FILE):
            print(f"Error: JSON template file {JSON_TEMPLATE_FILE} not found")
            return None
        
        print(f"Loading JSON template file: {JSON_TEMPLATE_FILE}")
        
        # First attempt - try full JSON parsing
        try:
            with open(JSON_TEMPLATE_FILE, 'r') as f:
                data = json.load(f)
                if "data" in data and isinstance(data["data"], dict):
                    first_key = next(iter(data["data"]))
                    content = data["data"][first_key]
                    if content:
                        print(f"Successfully extracted content: {len(content)} characters")
                        return content
        except Exception as json_error:
            print(f"Could not parse full JSON: {str(json_error)}")
        
        # Second attempt - use regex to extract content
        with open(JSON_TEMPLATE_FILE, 'r') as f:
            raw_text = f.read()
            
        # Look for content between quotes after "data" field
        matches = re.search(r'"data":\s*{\s*"[^"]+"\s*:\s*"(.*?)"\s*}', raw_text, re.DOTALL)
        if matches:
            content = matches.group(1)
            
            # Clean up escaped quotes and newlines
            content = content.replace('\\"', '"')
            content = content.replace('\\n', '\n')
            
            print(f"Extracted content using regex: {len(content)} characters")
            return content
        
        # Third attempt - manual search for large content block
        with open(JSON_TEMPLATE_FILE, 'r') as f:
            lines = f.readlines()
        
        start_line = -1
        for i, line in enumerate(lines):
            if '"data": {' in line:
                start_line = i + 1
                break
        
        if start_line > 0 and start_line < len(lines):
            # Combine next few lines and extract content
            combined = ''.join(lines[start_line:start_line+50])
            # Find content after first colon and before end brace
            matches = re.search(r':\s*"(.*?)"\s*}', combined, re.DOTALL)
            if matches:
                content = matches.group(1)
                
                # Clean up escaped quotes and newlines
                content = content.replace('\\"', '"')
                content = content.replace('\\n', '\n')
                
                print(f"Extracted content manually: {len(content)} characters")
                return content
        
        print("Could not extract content from JSON file")
        return None
            
    except Exception as e:
        print(f"Error extracting content from JSON: {str(e)}")
        return None

def load_faqs() -> List[Dict[str, str]]:
    """Load and parse FAQs from markdown file"""
    try:
        if not os.path.exists(FAQ_FILE):
            print(f"Warning: FAQ file {FAQ_FILE} not found. Using default FAQs.")
            # Return some default FAQs if file not found
            return [
                {
                    "question": "How much does a bail bond cost in [state_name]?",
                    "answer": "In [state_name], bail bond fees are typically [premium_rate]% of the total bail amount. For example, if bail is set at $10,000, you would pay $[premium_example] to a bail bondsman."
                },
                {
                    "question": "How long does it take to get out of jail with a bail bond in [state_name]?",
                    "answer": "Release times in [state_name] vary by facility, but typically range from 1-6 hours after the bond is posted. Our bail agents work quickly to expedite the process."
                },
                {
                    "question": "Do I get my bail money back in [state_name]?",
                    "answer": "If you pay the full bail amount directly to the court, you will receive it back when the case concludes (minus any fees). However, the premium paid to a bail bondsman (the [premium_rate]%) is non-refundable."
                },
                {
                    "question": "Can I get a bail bond with no money down in [state_name]?",
                    "answer": "While most [state_name] bail bond agencies require some form of upfront payment, many offer flexible payment plans. Some may accept collateral instead of immediate cash payment."
                },
                {
                    "question": "What happens if someone misses court after I bailed them out in [state_name]?",
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
                "question": "How much does a bail bond cost in [state_name]?",
                "answer": "In [state_name], bail bond fees are typically [premium_rate]% of the total bail amount. For example, if bail is set at $10,000, you would pay $[premium_example] to a bail bondsman."
            },
            {
                "question": "How does the bail process work in [state_name]?",
                "answer": "After an arrest in [state_name], the defendant appears before a judge who sets bail. A bail bondsman can post a surety bond for a fee of [premium_rate]% of the bail amount, allowing release until the court date."
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
        question = question.replace('[state_name]', state_name)
        answer = answer.replace('[state_name]', state_name)
        
        question = question.replace('[premium_rate]', premium_rate)
        answer = answer.replace('[premium_rate]', premium_rate)
        
        premium_example = str(int(premium_rate) * 100)
        answer = answer.replace('[premium_example]', premium_example)
        
        # Create accordion item - USING THE EXACT FORMAT FROM THE ORIGINAL TEMPLATE
        open_state = "on" if i == 1 else "off"
        item = f'[et_pb_accordion_item title="{question}" _builder_version="4.16.0" open="{open_state}" hover_enabled="0" sticky_enabled="0"]'
        item += answer
        item += '[/et_pb_accordion_item]'
        faq_items.append(item)
    
    result = ''.join(faq_items)
    print(f"Created FAQ section with {len(faq_items)} items")
    return result

def replace_placeholders(content: str, state_name: str, state_data: Dict) -> str:
    """Replace placeholders in the content, preserving the exact format"""
    print(f"Replacing placeholders in content for {state_name}...")
    
    # Set premium rate based on state
    premium_rate = "10" if state_name in ["Texas", "Florida", "California"] else "15"
    
    # Create map of replacements - Add EVERY possible format of placeholders
    replacements = {
        # Basic state info placeholders - with both formats
        '[state_name]': state_name,
        '[STATE_NAME]': state_name,
        '[State_Name]': state_name,
        '[state name]': state_name,
        '[state-name]': state_name,
        '[state]': state_name,
        
        '[state_abbr]': state_data['abbreviation'],
        '[STATE_ABBR]': state_data['abbreviation'],
        
        '[state_name_lower]': state_name.lower(),
        '[STATE_NAME_LOWER]': state_name.lower(),
        
        '[state_abbr_lower]': state_data['abbreviation'].lower(),
        '[STATE_ABBR_LOWER]': state_data['abbreviation'].lower(),
        
        '[premium_rate]': premium_rate,
        '[PREMIUM_RATE]': premium_rate,
        
        # Location data
        '[state_capital_address]': state_data['capital']['address'],
        '[STATE_CAPITAL_ADDRESS]': state_data['capital']['address'],
        
        '[state_capital_lat]': state_data['capital']['lat'],
        '[STATE_CAPITAL_LAT]': state_data['capital']['lat'],
        
        '[state_capital_lng]': state_data['capital']['lng'],
        '[STATE_CAPITAL_LNG]': state_data['capital']['lng'],
    }
    
    # Add county placeholders for all positions (with multiple formats)
    for i, county in enumerate(state_data['counties'][:3], 1):
        county_slug = county.lower().replace(' ', '-').replace(',', '')
        
        # With numbers
        replacements[f'[county_name_{i}]'] = county
        replacements[f'[COUNTY_NAME_{i}]'] = county
        replacements[f'[County_Name_{i}]'] = county
        
        replacements[f'[county_slug_{i}]'] = county_slug
        replacements[f'[COUNTY_SLUG_{i}]'] = county_slug
        
        # Without numbers (for repeating sections)
        if i == 1:
            replacements['[county_name]'] = county
            replacements['[COUNTY_NAME]'] = county
            replacements['[County_Name]'] = county
            replacements['[county name]'] = county
            
            replacements['[county_slug]'] = county_slug
            replacements['[COUNTY_SLUG]'] = county_slug
    
    # Add broader replacement for any county format
    replacements['[county_name]'] = state_data['counties'][0] if state_data['counties'] else "County"
    replacements['[COUNTY_NAME]'] = state_data['counties'][0] if state_data['counties'] else "County"
    
    # Apply all basic replacements (use regex for case insensitivity)
    for placeholder, value in replacements.items():
        # Count occurrences for debug (case insensitive)
        pattern = re.compile(re.escape(placeholder), re.IGNORECASE)
        matches = pattern.findall(content)
        if matches:
            print(f"Replacing {len(matches)} instances of {placeholder} (case insensitive)")
            
        # Replace all occurrences (case insensitive)
        content = re.sub(pattern, str(value), content)
    
    # Handle FAQ placeholders more thoroughly
    faqs = load_faqs()
    selected_faqs = random.sample(faqs, min(5, len(faqs)))
    
    # Multiple FAQ section formats
    faq_patterns = ['<!-- FAQ_ITEMS -->', '<!-- FAQ_SECTION -->', '[FAQ_SECTION]', '[FAQ_ITEMS]']
    faq_content = create_faq_section(faqs, state_name, premium_rate)
    
    for pattern in faq_patterns:
        if pattern in content:
            content = content.replace(pattern, faq_content)
            print(f"Replaced FAQ section with pattern: {pattern}")
    
    # Individual FAQ questions/answers with EXACT pattern matching
    for i, faq in enumerate(selected_faqs, 1):
        question = faq['question'].replace('[state_name]', state_name).replace('[premium_rate]', premium_rate)
        question = question.replace('[STATE_NAME]', state_name).replace('[PREMIUM_RATE]', premium_rate)
        
        answer = faq['answer'].replace('[state_name]', state_name).replace('[premium_rate]', premium_rate)
        answer = answer.replace('[STATE_NAME]', state_name).replace('[PREMIUM_RATE]', premium_rate)
        
        premium_example = str(int(premium_rate) * 100)
        answer = answer.replace('[premium_example]', premium_example)
        answer = answer.replace('[PREMIUM_EXAMPLE]', premium_example)
        
        # ALL possible FAQ placeholder formats
        faq_question_formats = [
            f'[FAQ_QUESTION_{i}]', 
            f'[faq_question_{i}]',
            f'[Faq_Question_{i}]',
            f'[FAQ QUESTION {i}]',
            f'[faq question {i}]',
            f'[FAQ-QUESTION-{i}]',
            f'[faq-question-{i}]'
        ]
        
        faq_answer_formats = [
            f'[FAQ_ANSWER_{i}]', 
            f'[faq_answer_{i}]',
            f'[Faq_Answer_{i}]',
            f'[FAQ ANSWER {i}]',
            f'[faq answer {i}]',
            f'[FAQ-ANSWER-{i}]',
            f'[faq-answer-{i}]'
        ]
        
        # Replace all question formats
        for format in faq_question_formats:
            if format in content:
                content = content.replace(format, question)
                print(f"Replaced FAQ question placeholder: {format}")
        
        # Replace all answer formats
        for format in faq_answer_formats:
            if format in content:
                content = content.replace(format, answer)
                print(f"Replaced FAQ answer placeholder: {format}")
    
    # Custom replacements for specific template
    special_replacements = {
        'Major Counties in [state_name]': f'Major Counties in {state_name}',
        'Major Counties in [STATE_NAME]': f'Major Counties in {state_name}',
        '[county_name]': state_data['counties'][0] if state_data['counties'] else "County",
        '[COUNTY_NAME]': state_data['counties'][0] if state_data['counties'] else "County"
    }
    
    for placeholder, value in special_replacements.items():
        content = content.replace(placeholder, value)
    
    # Final verification pass - list ANY remaining placeholders
    pattern = r'\[(.*?)\]'
    matches = re.findall(pattern, content)
    
    # Filter out Divi shortcode brackets that shouldn't be replaced
    divi_tags = ['et_pb_', '/et_pb_']
    remaining_placeholders = [m for m in matches if not any(tag in m for tag in divi_tags)]
    
    if remaining_placeholders:
        unique_placeholders = set(remaining_placeholders)
        print(f"WARNING: {len(unique_placeholders)} types of placeholders remain:")
        for placeholder in unique_placeholders:
            if len(placeholder) < 30 and not '"' in placeholder and not '{' in placeholder:
                print(f"  - [{placeholder}]")
                # Replace ANY remaining simple placeholders with state name
                content = content.replace(f"[{placeholder}]", state_name)
    else:
        print("SUCCESS: All placeholders replaced!")
    
    return content

def create_state_page_from_content(state_name: str) -> Optional[int]:
    """Create a state page using the EXACT template content"""
    print(f"Creating EXACT page for {state_name} using directly extracted content...")
    
    try:
        # Validate state data
        if state_name not in STATE_DATA:
            print(f"Error: No data found for state {state_name}")
            return None
        
        state_data = STATE_DATA[state_name]
        
        # Extract content from JSON
        raw_content = extract_content_from_json()
        if not raw_content:
            return None
        
        # Replace placeholders in the raw content
        processed_content = replace_placeholders(raw_content, state_name, state_data)
        
        # Prepare page data with ALL required meta fields
        page_data = {
            "title": f"Bail Bonds in {state_name} | Licensed Bail Bonds Company",
            "slug": f"bail-bonds-in-{state_name.lower().replace(' ', '-')}-{state_data['abbreviation'].lower()}",
            "content": processed_content,
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
        print("Sending EXACT page to WordPress API...")
        response = requests.post(
            f"{BASE_URL}/wp-json/wp/v2/pages",
            auth=AUTH,
            json=page_data
        )
        
        if response.status_code in range(200, 300):
            page_id = response.json().get("id")
            print(f"✅ Success! Created EXACT page for {state_name} with ID {page_id}")
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
    """Main function to run the script"""
    state_name = "Oklahoma"  # Only Oklahoma for now
    page_id = create_state_page_from_content(state_name)
    
    if page_id:
        print(f"\n✅ SUCCESS! Created the EXACT page for {state_name}.")
        print(f"View the page at: {BASE_URL}/?page_id={page_id}")
        print("This page will be EXACTLY as designed in your original template!")
    else:
        print(f"\n❌ FAILED to create page for {state_name}.")

if __name__ == "__main__":
    main() 