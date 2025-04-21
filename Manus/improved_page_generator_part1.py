#!/usr/bin/env python3
"""
Improved Page Generator for Bail Bonds Buddy State Pages (Part 1 of 3)

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
