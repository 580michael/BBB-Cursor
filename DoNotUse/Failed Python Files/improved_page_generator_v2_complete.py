#!/usr/bin/env python3
"""
Improved Page Generator for Bail Bonds Buddy State Pages

This script generates WordPress/Divi-compatible pages for all 50 states
while maintaining proper formatting and creating unique content.

Usage:
  python3 improved_page_generator_v2.py --test    # Test with Texas
  python3 improved_page_generator_v2.py --all     # Generate all state pages
"""

import os
import json
import re
import argparse
import random
from content_generator_utils import ContentGeneratorUtils as utils

# Constants
BASE_DIR = "/home/ubuntu/bailbonds"
TEMPLATE_FILE = f"{BASE_DIR}/Oklahoma Bail Bondsman Emergency 24_7 Service.json"
OUTPUT_DIR = f"{BASE_DIR}/generated_pages"
STATE_DATA_DIR = f"{BASE_DIR}/state_data"

def load_template():
    """Load the Oklahoma template JSON file"""
    try:
        with open(TEMPLATE_FILE, 'r') as f:
            template_json = json.load(f)
        print("Oklahoma template loaded successfully")
        return template_json
    except Exception as e:
        print(f"Error loading template: {e}")
        return None

def load_state_data(state_name):
    """Load data for a specific state"""
    state_file = f"{STATE_DATA_DIR}/{state_name.lower().replace(' ', '_')}.json"
    try:
        with open(state_file, 'r') as f:
            state_data = json.load(f)
        return state_data
    except Exception as e:
        print(f"Error loading state data for {state_name}: {e}")
        # Generate sample data for testing
        if state_name.lower() == "texas":
            print(f"Generating sample data for {state_name}...")
            sample_data = generate_sample_state_data(state_name)
            # Save sample data
            os.makedirs(STATE_DATA_DIR, exist_ok=True)
            with open(state_file, 'w') as f:
                json.dump(sample_data, f, indent=2)
            print(f"Sample data for {state_name} saved to {state_file}")
            return sample_data
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

def replace_content_sections(content, state_data):
    """Replace standard content sections with unique content"""
    if not isinstance(content, str):
        return content
    
    state_name = state_data["name"]
    
    # Replace intro paragraph
    intro_pattern = r'We understand that finding a reliable bail bondsman can be stressful.*?most\.'
    if re.search(intro_pattern, content, re.DOTALL):
        unique_intro = utils.generate_unique_intro_paragraph(state_name)
        content = re.sub(intro_pattern, unique_intro, content, flags=re.DOTALL)
    
    # Replace "Every hour spent in jail" paragraph
    hours_pattern = r'Every hour spent in jail can impact someone.*?matters most\.'
    if re.search(hours_pattern, content, re.DOTALL):
        unique_arrest = utils.generate_unique_arrest_paragraph(state_name)
        content = re.sub(hours_pattern, unique_arrest, content, flags=re.DOTALL)
    
    # Replace 24/7 Availability section
    availability_pattern = r'Emergency bail bond services available any time.*?help now\.'
    if re.search(availability_pattern, content, re.DOTALL):
        unique_availability = utils.generate_unique_availability_content(state_name)
        content = re.sub(availability_pattern, unique_availability, content, flags=re.DOTALL)
    
    # Replace Verified Bondsman section
    verified_pattern = r'Emergency bail bond services available from pre-screened.*?business practices\.'
    if re.search(verified_pattern, content, re.DOTALL):
        unique_verified = utils.generate_unique_verified_content(state_name)
        content = re.sub(verified_pattern, unique_verified, content, flags=re.DOTALL)
    
    # Replace Nationwide Coverage section
    coverage_pattern = r'From small towns to major cities, find bail bondsmen across.*?need it\.'
    if re.search(coverage_pattern, content, re.DOTALL):
        unique_coverage = utils.generate_unique_coverage_content(state_name)
        content = re.sub(coverage_pattern, unique_coverage, content, flags=re.DOTALL)
    
    # Replace "When you or a loved one is arrested" paragraph
    arrest_pattern = r'When you or a loved one is arrested, time is of the essence.*?family responsibilities\.'
    if re.search(arrest_pattern, content, re.DOTALL):
        unique_network = utils.generate_unique_network_paragraph(state_name)
        content = re.sub(arrest_pattern, unique_network, content, flags=re.DOTALL)
    
    # Replace BailBondsBuddy paragraph
    buddy_pattern = r'BailBondsBuddy.com gives you instant access to trusted bondsmen.*?family responsibilities\.'
    if re.search(buddy_pattern, content, re.DOTALL):
        unique_buddy = utils.generate_unique_bailbondsbuddy_paragraph(state_name)
        content = re.sub(buddy_pattern, unique_buddy, content, flags=re.DOTALL)
    
    return content

def replace_faq_sections(content, state_data):
    """Replace FAQ sections with unique questions and answers"""
    if not isinstance(content, str):
        return content
    
    state_name = state_data["name"]
    
    # Generate unique FAQ questions for this state
    unique_questions = utils.generate_unique_faq_questions(state_name)
    
    # Find and replace FAQ sections
    faq_pattern = r'<div class="et_pb_toggle_title">(.*?)</div>.*?<div class="et_pb_toggle_content clearfix">(.*?)</div>'
    faq_matches = re.finditer(faq_pattern, content, re.DOTALL)
    
    for i, match in enumerate(faq_matches):
        if i < len(unique_questions):
            question = unique_questions[i]
            answer = utils.generate_unique_faq_answer(question, state_name)
            
            # Create replacement with proper formatting
            replacement = f'<div class="et_pb_toggle_title">{question}</div><div class="et_pb_toggle_content clearfix"><p>{answer}</p></div>'
            
            # Replace this specific FAQ
            content = content.replace(match.group(0), replacement, 1)
    
    return content

def replace_state_specific_content(content, state_data):
    """Replace state-specific content sections"""
    if not isinstance(content, str):
        return content
    
    state_name = state_data["name"]
    
    # Replace state description section
    state_desc_pattern = r'Oklahoma, known as the Sooner State.*?legal process\.'
    if re.search(state_desc_pattern, content, re.DOTALL):
        # Create unique state description
        state_desc = f"{state_name}, known as the {state_data['nickname']}, combines rich Native American heritage, pioneering spirit, and modern economic growth across its diverse landscape. With a population of approximately {state_data['population']} residents spread throughout {state_data['num_counties']} counties, {state_name} presents unique challenges and opportunities within its criminal justice system.\n\nThe state's largest metropolitan areas – {state_data['major_cities'][0]} and {state_data['major_cities'][1]} – account for the highest concentration of arrests and bail needs, but {state_name}'s extensive rural communities also require specialized bail bond services. {state_name}'s county jail system operates under state supervision while maintaining individual county administration, creating a patchwork of procedures that experienced bail bondsmen must navigate daily.\n\n{state_name}'s economy has traditionally centered around {state_data['economic_info']} This economic evolution has affected crime patterns and bail requirements throughout the state, with growing urban centers experiencing different needs than rural communities.\n\nThe state maintains a robust bail system governed by the {state_data['bail_system']}\n\n{state_data['criminal_justice']}\n\n{state_data['geography']}\n\n{state_data['weather']} Local bondsmen familiar with {state_name}'s systems know how to manage these disruptions while ensuring clients meet all legal obligations.\n\nFor families seeking to secure a loved one's release from any of {state_name}'s detention facilities, working with an {state_name}-based bail bondsman who understands the state's unique characteristics provides the most efficient path to reunion and beginning the next steps in the legal process."
        
        content = re.sub(state_desc_pattern, state_desc, content, flags=re.DOTALL)
    
    # Replace "Major Counties in Oklahoma" heading
    counties_heading_pattern = r'Major Counties in Oklahoma'
    if re.search(counties_heading_pattern, content):
        counties_heading = f"Major Counties in {state_name}"
        content = re.sub(counties_heading_pattern, counties_heading, content)
    
    # Replace county headings
    for i, county in enumerate(state_data["largest_counties"]):
        county_name = county.split(" ")[0]  # Extract just the county name without "County"
        old_county_pattern = f"Oklahoma County|Tulsa County|Cleveland County"
        if i == 0:
            content = re.sub(old_county_pattern, county, content, count=1)
        elif re.search(old_county_pattern, content):
            content = re.sub(old_county_pattern, county, content, count=1)
    
    return content

def replace_title_and_headings(content, state_data):
    """Replace title and headings with state-specific versions"""
    if not isinstance(content, str):
        return content
    
    state_name = state_data["name"]
    
    # Replace page title
    title_pattern = r'Oklahoma Bail Bondsman Emergency 24/7 Service \| BailBondsBuddy\.com'
    if re.search(title_pattern, content):
        new_title = f"{state_name} Bail Bondsman Emergency 24/7 Service | BailBondsBuddy.com"
        content = re.sub(title_pattern, new_title, content)
    
    # Replace "Find Local Bail Bondsmen Near You" heading
    heading_pattern = r'Find Local (Oklahoma )?Bail Bondsmen Near You'
    if re.search(heading_pattern, content):
        new_heading = f"Find Local {state_name} Bail Bondsmen Near You"
        content = re.sub(heading_pattern, new_heading, content)
    
    # Replace "Find Licensed Bail Bond Agents" heading
    agents_pattern = r'Find Licensed (Oklahoma )?Bail Bond Agents Available Now'
    if re.search(agents_pattern, content):
        new_agents = f"Find Licensed {state_name} Bail Bond Agents Available Now"
        content = re.sub(agents_pattern, new_agents, content)
    
    # Replace "Your Guide to Finding Local Bail Bondsmen" heading
    guide_pattern = r'Your Guide to Finding Local (Oklahoma )?Bail Bondsmen'
    if re.search(guide_pattern, content):
        new_guide = f"Your Guide to Finding Local {state_name} Bail Bondsmen"
        content = re.sub(guide_pattern, new_guide, content)
    
    # Replace "Oklahoma: The Sooner State" heading
    state_heading_pattern = r'Oklahoma: The Sooner State'
    if re.search(state_heading_pattern, content):
        new_state_heading = f"{state_name}: The {state_data['nickname']}"
        content = re.sub(state_heading_pattern, new_state_heading, content)
    
    return content

def process_json_content(template_json, state_data):
    """Process the JSON content to replace all state-specific information"""
    # Make a deep copy of the template
    new_json = json.loads(json.dumps(template_json))
    
    # Extract state information
    old_state = "Oklahoma"
    new_state = state_data["name"]
    old_nickname = "Sooner State"
    new_nickname = state_data["nickname"]
    old_population = "4 million"
    new_population = state_data["population"]
    old_counties = ["Oklahoma County", "Tulsa County", "Cleveland County"]
    new_counties = state_data["largest_counties"]
    old_cities = ["Oklahoma City", "Tulsa"]
    new_cities = state_data["major_cities"][:2]  # Use first two cities
    
    # Process each field in the JSON
    def process_field(obj):
        if isinstance(obj, dict):
            for key, value in obj.items():
                if isinstance(value, (dict, list)):
                    process_field(value)
                elif isinstance(value, str):
                    # Replace state references
                    value = replace_state_references(value, old_state, new_state)
                    # Replace nickname
                    value = replace_nickname_references(value, old_nickname, new_n
(Content truncated due to size limit. Use line ranges to read in chunks)