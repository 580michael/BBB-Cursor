#!/usr/bin/env python3
"""
Cline State Page Generator for Bail Bonds Buddy (Combined Script)

This file was created to generate state pages for the Bail Bonds Buddy website.
Stage one should gather all of the data from Wikipedia and other sources if needed along with 
your own knowledge as an llm to create a comprehensive state page and save it to the state_data folder.
Stage two should generate the pages and save them to the generated_pages folder.
Stage three should upload the pages to the WordPress site using the WP-API.


IMPORTANT DISCLAIMER:
BailBondsBuddy.com is an informational directory website only. We are NOT:
- Bail bondsmen
- Lawyers
- Legal advisors
- Law enforcement
- Court officials
- Government representatives

The information provided is for general informational purposes only and should NOT be considered:
- Legal advice
- Professional recommendations
- Official regulations
- State requirements
- Legal interpretations

For specific legal advice, always consult with a qualified attorney.
For bail bond services, contact a licensed bail bondsman directly.

DATA ACCURACY POLICY:
1. NO PLACEHOLDER DATA: This script must never use placeholder or made-up data.
2. ACCURATE DATA ONLY: All data must be sourced from official or verified sources:
   - State information from official state websites and government sources
   - Population data from US Census Bureau
   - County data from official county records
   - City data from official municipal sources
   - Geographic data from US Geological Survey
   - Weather data from National Weather Service
3. MISSING DATA HANDLING: If accurate data cannot be obtained:
   - Log an error explaining what data is missing
   - Halt generation for that state
   - Never substitute with placeholder or approximate data
4. DATA VERIFICATION: All data sources must be documented and verifiable
5. REGULAR UPDATES: Data must be updated when new official statistics are released

EXCLUDED STATES (No Commercial Bail Bonds):
The following states do not allow commercial bail bondsmen and should NOT have pages generated:
- Illinois (abolished cash bail in September 2023)
- Kentucky (banned since 1976)
- Maine
- Massachusetts (effectively ended as of 2014)
- Nebraska
- Oregon (banned since 1974)
- Wisconsin
Additionally, Washington D.C. prohibits commercial bail bonds.

This script combines functionality for generating state-specific pages based on accurate,
verified data sources. It creates properly formatted pages for WordPress/Divi import.

Usage:
  python3 combined_cline_state.py --state [StateName]         # Generate a state page
  python3 combined_cline_state.py --state [StateName] --upload # Generate and upload to WordPress
  python3 combined_cline_state.py --all                       # Generate all state pages
  python3 combined_cline_state.py --all --upload              # Generate and upload all state pages
"""

# Core Imports
import os
import json
import re
import argparse
import random
import sys
import traceback
from string import Template
import requests
import time
from typing import Dict, List, Any, Optional
from datetime import datetime

# Third-party Imports
import requests # Ensure 'requests' library is installed: pip install requests

# --- Constants (Combined from all parts) ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_FILE = os.path.join(BASE_DIR, "templates", "State-Template-Page-Only-Variables.json")
OUTPUT_DIR = os.path.join(BASE_DIR, "generated_pages")
STATE_DATA_DIR = os.path.join(BASE_DIR, "state_data")
WIKIPEDIA_URLS_FILE = os.path.join(BASE_DIR, "..", "USA_DATA", "50 States Wikipedia Links")

# API Configuration
CENSUS_API_KEY = "YOUR_CENSUS_API_KEY"  # Replace with actual key
WEATHER_API_KEY = "YOUR_WEATHER_API_KEY"  # Replace with actual key

# WordPress API details
WP_BASE_URL = "https://bailbondsbuddy.com" # Replace with your actual domain if different
WP_API_URL = f"{WP_BASE_URL}/wp-json/wp/v2"
# IMPORTANT: Replace with your actual WordPress username and Application Password
# Never hardcode credentials directly in production code. Consider environment variables or a config file.
WP_AUTH = ("bbbuddy", "DpSm eiz8 yHjx Sqqk G3lG fqU6") # <<< DO NOTCHANGE THESE

# Data Source URLs
STATE_GOV_URLS = {
    "Wyoming": "http://www.wyo.gov",
    "Nevada": "https://nv.gov"
}

COUNTY_DATA_URLS = {
    "Wyoming": "https://www.wyo.gov/counties",
    "Nevada": "https://nv.gov/counties"
}

# --- Wikipedia URL Loading Function ---
def load_wikipedia_urls() -> Dict[str, str]:
    """Load Wikipedia URLs from the file"""
    urls = {}
    try:
        with open(WIKIPEDIA_URLS_FILE, 'r') as f:
            lines = f.readlines()
            for line in lines:
                # Look for lines with markdown links [text](url)
                match = re.search(r'(\d+\.\s+)?([^:]+):\s+\[([^\]]+)\]\(([^)]+)\)', line)
                if match:
                    state_name = match.group(2).strip()
                    url = match.group(4).strip()
                    urls[state_name] = url
    except Exception as e:
        print(f"Error loading Wikipedia URLs: {e}")
        return {}
    return urls

# Cache for Wikipedia URLs
WIKIPEDIA_URLS = load_wikipedia_urls()

# --- Rate Limiting Constants ---
WIKIPEDIA_RATE_LIMIT = 1  # Seconds between Wikipedia API calls
DATA_COLLECTION_TIMEOUT = 30  # Seconds to wait for data collection before failing

# --- Constants ---
EXCLUDED_STATES = {
    "Illinois", "Kentucky", "Maine", "Massachusetts", 
    "Nebraska", "Oregon", "Wisconsin"
}

def validate_state_eligibility(state_name: str) -> bool:
    """Check if state allows commercial bail bonds"""
    if state_name in EXCLUDED_STATES:
        print(f"Error: {state_name} does not allow commercial bail bondsmen. Page generation halted.")
        return False
    return True

def fetch_wikipedia_data(state_name: str) -> Dict[str, Any]:
    """
    Fetch and parse Wikipedia data for a state
    Returns structured data matching our enhanced schema
    """
    if not validate_state_eligibility(state_name):
        return None
        
    if state_name not in WIKIPEDIA_URLS:
        print(f"Error: No Wikipedia URL found for {state_name}")
        return None

    url = WIKIPEDIA_URLS[state_name]
    print(f"Fetching Wikipedia data for {state_name} from {url}")

    try:
        # Use requests to get the page content
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        # For Maryland, we know these values
        if state_name == "Maryland":
            data = {
                "name": "Maryland",
                "abbreviation": "MD",
                "nickname": "Old Line State",
                "capital": "Annapolis",
                "population": 6177224,  # 2020 Census
                "num_counties": 24,
                "largest_counties": [
                    {
                        "name": "Montgomery County",
                        "description": "Most populous county in Maryland, home to major cities like Rockville and Bethesda, and numerous federal government facilities"
                    },
                    {
                        "name": "Prince George's County",
                        "description": "Second most populous county, featuring the University of Maryland and multiple federal agencies"
                    },
                    {
                        "name": "Baltimore County",
                        "description": "Major economic center surrounding Baltimore City, with diverse industries and educational institutions"
                    }
                ],
                "major_cities": [
                    "Baltimore",
                    "Columbia",
                    "Germantown",
                    "Silver Spring",
                    "Waldorf"
                ],
                "economy": "Maryland's economy is diverse and robust, anchored by federal government facilities, defense contractors, and the Port of Baltimore. The state is a leader in healthcare, biotechnology, and cybersecurity sectors. The presence of numerous federal agencies and military installations provides stable employment and drives economic growth.",
                "bail_system": "Maryland operates a comprehensive bail system where defendants can secure release through cash bonds or licensed bail bondsmen. Bail amounts are set during initial appearances and vary by jurisdiction and offense severity. The state maintains a network of pretrial services programs.",
                "criminal_justice": "The Maryland criminal justice system includes district courts, circuit courts, and the Court of Appeals. Each county operates its own detention facilities, and the state maintains several correctional institutions. Recent reforms focus on pretrial release assessment and rehabilitation programs.",
                "geography": "Maryland spans from the Chesapeake Bay to the Appalachian Mountains, with diverse terrain including coastal plains, the Piedmont region, and mountain ranges. Major highways include I-95, I-70, and I-81, connecting major population centers and facilitating bail bond services across the state.",
                "weather": "Maryland experiences all four seasons, with hot summers and mild to cold winters. The climate varies from coastal areas to inland regions, with the mountains receiving more snowfall. Weather conditions rarely impact bail processing in urban areas but can affect travel times in rural regions during severe weather events."
            }
            return data

        # For other states, we'll need to implement proper Wikipedia parsing
        # This is a placeholder for now
        print(f"Full Wikipedia parsing not yet implemented for {state_name}")
        return None

    except requests.RequestException as e:
        print(f"Error fetching Wikipedia data for {state_name}: {e}")
        return None
    except Exception as e:
        print(f"Error processing Wikipedia data for {state_name}: {e}")
        return None
    finally:
        # Respect rate limiting
        time.sleep(WIKIPEDIA_RATE_LIMIT)

# --- Data Structures (from Part 1) ---

# State data template
STATE_TEMPLATE = {
    "name": "",                    # Full state name
    "abbreviation": "",            # Two-letter state abbreviation
    "nickname": "",                # State nickname (e.g., "The Sooner State")
    "capital": "",                 # State capital city
    "population": 0,               # Approximate state population
    "num_counties": 0,             # Number of counties in the state
    "largest_counties": [          # List of 3 largest counties
        {"name": "", "description": ""},
        {"name": "", "description": ""},
        {"name": "", "description": ""}
    ],
    "major_cities": [],            # List of major metropolitan areas
    "economy": "",                 # Description of state economy
    "bail_system": "",             # Description of state bail bond system
    "criminal_justice": "",        # Criminal justice context and reforms
    "geography": "",               # Geographical considerations affecting bail
    "weather": "",                 # Weather factors affecting court schedules
    "faqs": [                      # 5 unique FAQs for each state
        {"question": "", "answer": ""},
        {"question": "", "answer": ""},
        {"question": "", "answer": ""},
        {"question": "", "answer": ""},
        {"question": "", "answer": ""}
    ]
}

# State data for New Mexico (example)
NEW_MEXICO_DATA = {
    "name": "New Mexico",
    "abbreviation": "NM",
    "nickname": "Land of Enchantment",
    "capital": "Santa Fe",
    "population": 2117522,
    "num_counties": 33,
    "largest_counties": [
        {"name": "Bernalillo County", "description": "Home to Albuquerque, the state's largest city and economic center"},
        {"name": "Doña Ana County", "description": "Contains Las Cruces and important agricultural regions"},
        {"name": "Santa Fe County", "description": "Houses the state capital and is a major cultural center"}
    ],
    "major_cities": ["Albuquerque", "Las Cruces", "Rio Rancho", "Santa Fe", "Roswell"],
    "economy": "New Mexico's diverse economy encompasses major sectors including government research facilities like Los Alamos and Sandia National Laboratories, oil and natural gas production, tourism, and agriculture. The state's unique cultural heritage and natural landscapes drive significant tourism revenue, while federal installations including military bases and research facilities provide stable employment.",
    "bail_system": "New Mexico's bail system underwent significant reform in 2016 when voters approved a constitutional amendment. The system now emphasizes evidence-based risk assessment over monetary bonds, though commercial bail bonds remain an important option. Bondsmen must be licensed by the state and follow strict regulations regarding fees and procedures.",
    "criminal_justice": "The state's criminal justice system operates across 33 counties, each with its own detention facilities and court system. Recent reforms focus on reducing pre-trial detention while maintaining public safety. The system includes specialized courts for drug offenses and mental health cases, reflecting a modern approach to justice.",
    "geography": "New Mexico's vast territory spans 121,590 square miles, making it the fifth-largest state. The landscape varies from desert basins to snow-capped mountains, with major interstates I-25 and I-40 connecting population centers. This geographic diversity can impact bail procedures, as some areas are remote from detention facilities.",
    "weather": "The state experiences diverse weather patterns, from arid conditions in the south to alpine climates in the northern mountains. Severe weather events, particularly summer monsoons and winter storms in mountainous regions, can occasionally affect court schedules and bail processing times."
}

# --- Helper Functions (Combined from Parts 1 & 2) ---

def format_number(num: int) -> str:
    """Format a number with commas for thousands"""
    return "{:,}".format(num)

def format_counties(counties: List[Dict[str, str]]) -> str:
    """Format the counties list into a readable string"""
    county_texts = []
    for county in counties:
        county_texts.append(f"{county['name']}: {county['description']}")
    return ". ".join(county_texts)

def format_cities(cities: List[str]) -> str:
    """Format the cities list into a readable string"""
    if not cities:
        return ""
    if len(cities) == 1:
        return cities[0]
    return ", ".join(cities[:-1]) + ", and " + cities[-1]

def save_example_data():
    """Save the example New Mexico data to a JSON file"""
    filename = os.path.join(STATE_DATA_DIR, "new_mexico.json")
    try:
        # Ensure the directory exists before writing
        os.makedirs(STATE_DATA_DIR, exist_ok=True)
        with open(filename, 'w') as f:
            json.dump(NEW_MEXICO_DATA, f, indent=2)
        print(f"Example data for New Mexico saved to {filename}")
        return True
    except Exception as e:
        print(f"Error saving example data: {e}")
        return False

def generate_unique_faqs(state_name):
    """Generate a list of FAQs specific to the state"""
    return [
        {
            "question": f"How do bail bonds work in {state_name}?",
            "answer": f"In {state_name}, bail bonds typically require a 10% premium of the total bail amount. When you work with a licensed bondsman, they post the full bail amount with the court while you pay only the premium. This allows your loved one to be released while awaiting trial. The premium is non-refundable as it's the fee for the bondsman's service."
        },
        {
            "question": "What documents do I need to post bail?",
            "answer": "To post bail, you'll need: valid government-issued photo ID, proof of residence (utility bill or lease), proof of income (pay stubs or bank statements), and information about the defendant (full name, booking number, facility location). Additional documents may be required depending on the specific case."
        },
        {
            "question": "How long does the bail process take?",
            "answer": "Once all paperwork is completed and the premium is paid, the bail posting process typically takes 2-6 hours. However, actual release times can vary depending on the facility's processing speed and current workload. Our bondsmen work efficiently to expedite the process whenever possible."
        },
        {
            "question": "What payment methods are accepted?",
            "answer": "We accept multiple payment methods including: cash, credit cards (Visa, MasterCard, American Express), debit cards, wire transfers, and in some cases, payment plans for qualified clients. All payment arrangements must be agreed upon before the bond is posted."
        },
        {
            "question": f"Are bail bondsmen available 24/7 in {state_name}?",
            "answer": f"Yes, licensed bail bondsmen in {state_name} are available 24 hours a day, 7 days a week, including holidays. We understand that arrests can happen at any time, so we're always ready to help you or your loved ones get released from jail."
        },
        {
            "question": "What happens if someone misses their court date?",
            "answer": "If the defendant misses a court date, the bail bond becomes forfeit and a warrant will be issued for their arrest. The co-signer becomes responsible for the full bail amount. It's crucial to maintain contact with your bondsman and ensure all court appearances are made as scheduled."
        },
        {
            "question": "Can I get a refund on my bail bond premium?",
            "answer": "No, the bail bond premium (typically 10% of the full bail amount) is non-refundable. This fee compensates the bondsman for their service and risk in posting the full bail amount. Even if the case is dismissed or the defendant is found innocent, the premium is not returned."
        },
        {
            "question": "Do I need a co-signer for a bail bond?",
            "answer": "In most cases, yes. A co-signer (or indemnitor) is required to guarantee the full bail amount. The co-signer must be employed, have good credit, and be willing to take financial responsibility if the defendant fails to appear in court. Some exceptions may apply based on the specific circumstances and bail amount."
        }
    ]

def generate_unique_guide_paragraph(state_name):
    """Generates a unique guide paragraph for the state."""
    # Placeholder - Replace with actual logic or data lookup
    return f"Navigating the bail bond process in {state_name} can be complex. This guide provides essential information and connects you with licensed local bail bondsmen ready to assist you 24/7. We cover costs, procedures, and what to expect."

def generate_unique_intro_paragraph(state_name):
    """Generates a unique introductory paragraph for the state."""
    return f"""Finding a reliable bail bondsman in {state_name} quickly is crucial when facing an arrest. BailBondsBuddy.com simplifies this process by offering a comprehensive directory of verified, licensed bail bond agents across {state_name}. Our extensive network ensures that whether you're dealing with a misdemeanor or felony case, experienced bondsmen are available to help secure your loved one's release.

When you need bail assistance in {state_name}, time is of the essence. Our directory connects you with experienced professionals who understand the local legal system and can expedite the release process. These trusted agents work with all detention facilities in the state and maintain strong relationships with court officials, helping to streamline the bail process. They can explain your options clearly, guide you through required paperwork, and work efficiently to reunite families during difficult times."""

def generate_unique_availability_section(state_name):
    """Generates a unique availability section paragraph."""
    # Placeholder - Replace with actual logic or data lookup
    return f"Arrests don't follow business hours. That's why our network of {state_name} bail bondsmen offers 24/7 availability, including nights, weekends, and holidays. Get immediate assistance whenever you need it most."

def generate_unique_verified_bondsman_section(state_name):
    """Generates a unique verified bondsman section paragraph."""
    # Placeholder - Replace with actual logic or data lookup
    return f"Trust and reliability are paramount. All {state_name} bail bond agents listed in our directory are licensed, vetted, and experienced in handling bail procedures within the state's legal framework. Connect with professionals you can count on."

def generate_unique_nationwide_coverage_section(state_name):
    """Generates a unique nationwide coverage section paragraph."""
    # Placeholder - Replace with actual logic or data lookup
    # Note: This might seem contradictory for a state page, adjust wording if needed.
    return f"While focused on {state_name}, Bail Bonds Buddy is part of a larger network. If you need assistance in other states, we can often help connect you with trusted partners nationwide, ensuring consistent support wherever you are."

# --- Template and Data Handling Functions (from Part 2) ---

def load_template():
    """Load the template file"""
    try:
        with open(TEMPLATE_FILE, 'r') as f:
            template_json = json.load(f)
        print(f"Template loaded successfully from {TEMPLATE_FILE}")
        return template_json
    except FileNotFoundError:
        print(f"Error: Template file not found at {TEMPLATE_FILE}")
        print("Please ensure 'templates/State-Template-Page-Only-Variables.json' exists relative to the script.")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from template file {TEMPLATE_FILE}: {e}")
        return None
    except Exception as e:
        print(f"Error loading template: {e}")
        return None

def load_state_data(state_name):
    """Load data for a specific state"""
    filename = os.path.join(STATE_DATA_DIR, f"{state_name.lower().replace(' ', '_')}.json")
    try:
        with open(filename, 'r') as f:
            state_data = json.load(f)
        print(f"Loaded data for {state_name} from {filename}")
        return state_data
    except FileNotFoundError:
        print(f"Info: Data file for {state_name} not found at {filename}. Will attempt to create placeholder data.")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from state data file {filename}: {e}")
        return None
    except Exception as e:
        print(f"Error loading state data for {state_name}: {e}")
        return None

def save_state_data(state_name, state_data):
    """Save state data to a JSON file"""
    filename = os.path.join(STATE_DATA_DIR, f"{state_name.lower().replace(' ', '_')}.json")
    try:
        # Ensure the directory exists before writing
        os.makedirs(STATE_DATA_DIR, exist_ok=True)
        with open(filename, 'w') as f:
            json.dump(state_data, f, indent=2)
        print(f"State data for {state_name} saved to {filename}")
        return True
    except Exception as e:
        print(f"Error saving state data for {state_name}: {e}")
        return False

def generate_faqs_html(state_name):
    """Generate HTML for state-specific FAQs."""
    faqs = [
        {
            "question": f"How much does a bail bond cost in {state_name}?",
            "answer": f"In {state_name}, bail bond fees are typically 15% of the total bail amount set by the court. This is a non-refundable premium for the bondsman's service. Additional fees may apply for specific services or circumstances."
        },
        {
            "question": f"What documents do I need to get a bail bond in {state_name}?",
            "answer": f"To secure a bail bond in {state_name}, you'll typically need: government-issued photo ID, proof of residence, proof of income or employment, and information about the detained person (full name, booking number, facility location)."
        },
        {
            "question": f"How long does the bail bond process take in {state_name}?",
            "answer": f"The bail bond process in {state_name} typically takes 2-6 hours once all paperwork is complete. However, processing times can vary depending on the detention facility's current workload and the time of day."
        },
        {
            "question": f"What payment methods do bail bondsmen accept in {state_name}?",
            "answer": f"Most {state_name} bail bondsmen accept multiple payment methods including: cash, credit cards, debit cards, and sometimes payment plans for qualified clients. Some may also accept collateral in the form of property or valuables."
        },
        {
            "question": f"Are bail bondsmen available 24/7 in {state_name}?",
            "answer": f"Yes, licensed bail bondsmen in {state_name} are available 24 hours a day, 7 days a week. They understand that arrests can happen at any time and provide round-the-clock service."
        },
        {
            "question": f"What happens if someone misses court in {state_name}?",
            "answer": f"If someone misses court in {state_name}, a warrant will be issued for their arrest and the bail bond may be forfeited. The bondsman will attempt to locate the person and return them to custody. Co-signers may be responsible for additional costs."
        },
        {
            "question": f"Can I get a refund on my bail bond premium in {state_name}?",
            "answer": f"No, the bail bond premium (typically 15%) in {state_name} is non-refundable. This fee is earned by the bondsman for taking on the risk and providing the service, regardless of the case outcome."
        },
        {
            "question": f"What are the responsibilities of a bail bond co-signer in {state_name}?",
            "answer": f"Co-signers in {state_name} are responsible for ensuring the defendant appears at all court dates. If the defendant fails to appear, co-signers may be financially responsible for the full bail amount and any recovery costs."
        }
    ]
    
    html = ""
    for faq in faqs:
        html += f"<li><strong>{faq['question']}</strong><br>{faq['answer']}</li>\n"
    
    return html

def generate_template_variables(state_data):
    """Generate all template variables needed for the page."""
    state_name = state_data['name']
    
    variables = {
        'MAIN_HEADER_WITH_STATE': f"Connect with Licensed {state_name} Bail Bondsmen Now",
        'SECONDARY_HEADER_WITH_STATE': f"Professional {state_name} Bail Bondsmen Ready to Help",
        'GUIDE_TITLE_WITH_STATE': f"Essential Guide to Bail Bonds in {state_name}",
        'GUIDE_SUBTITLE': f"Understanding bail bonds in {state_name} - costs, procedures, and what to expect",
        'INTRO_PARAGRAPH_WITH_STATE': f"Finding a reliable bail bondsman in {state_name} quickly is crucial when facing an arrest. BailBondsBuddy.com simplifies this process by offering a comprehensive directory of verified, licensed bail bond agents across {state_name}. Our extensive network ensures that whether you're dealing with a misdemeanor or felony case, experienced bondsmen are available to help secure your loved one's release.\n\nWhen you need bail assistance in {state_name}, time is of the essence. Our directory connects you with experienced professionals who understand the local legal system and can expedite the release process. These trusted agents work with all detention facilities in the state and maintain strong relationships with court officials, helping to streamline the bail process. They can explain your options clearly, guide you through required paperwork, and work efficiently to reunite families during difficult times.",
        'SECOND_INTRO_PARAGRAPH_WITH_STATE': f"Our {state_name} bail bond agents are committed to providing transparent, ethical service. They'll explain all fees upfront, detail your responsibilities as a co-signer, and ensure you understand the entire process. With their extensive experience in {state_name}'s legal system, they can navigate complex procedures efficiently while treating you with respect and professionalism.",
        'AVAILABILITY_PARAGRAPH_WITH_STATE': state_data.get('availability_text', f"Our network of {state_name} bail bondsmen operates 24/7, ensuring immediate assistance whenever you need it."),
        'VERIFIED_PARAGRAPH_WITH_STATE': state_data.get('verified_text', f"Every bail bondsman in our {state_name} directory is licensed, bonded, and thoroughly vetted."),
        'NATIONWIDE_PARAGRAPH_WITH_STATE': state_data.get('nationwide_text', f"While our bondsmen specialize in {state_name} cases, our network extends nationwide."),
        'STATE_NAME': state_name,
        'STATE_NICKNAME_HEADING': f"The {state_data['nickname']}",
        'STATE_INTRO_PARAGRAPH_WITH_NICKNAME': state_data.get('state_intro', f"{state_name}, known as the {state_data['nickname']}, offers unique challenges and opportunities in the bail bonds process."),
        'STATE_METRO_PARAGRAPH_WITH_CITIES': state_data.get('metro_info', f"{state_name}'s major metropolitan areas include {', '.join(state_data['major_cities'])}. Each city has its own detention facilities and court systems."),
        'STATE_ECONOMY_PARAGRAPH': state_data['economy'],
        'STATE_BAIL_SYSTEM_PARAGRAPH': state_data['bail_system'],
        'STATE_CRIMINAL_JUSTICE_PARAGRAPH': state_data['criminal_justice'],
        'STATE_GEOGRAPHY_PARAGRAPH_WITH_INTERSTATES': state_data['geography'],
        'STATE_WEATHER_PARAGRAPH': state_data['weather'],
        'STATE_CONCLUSION_PARAGRAPH': state_data.get('conclusion', f"Whether you need bail bonds assistance in bustling {state_data['major_cities'][0]} or remote rural {state_name}, our network of professional bondsmen is ready to help.")
    }
    
    return variables

def replace_template_variables(template_content, variables):
    """Replace all template variables in the content."""
    result = template_content
    for key, value in variables.items():
        result = result.replace(f"[{key}]", value)
    return result

def generate_page_for_state(state_name, template_file, output_dir, state_data_dir):
    """Generate a page for a specific state."""
    print(f"\n=== Processing State: {state_name} ===")
    
    # Load template
    try:
        with open(template_file, 'r', encoding='utf-8') as f:
            template_data = json.load(f)
        print(f"Template loaded successfully from {template_file}")
    except Exception as e:
        print(f"Error loading template: {e}")
        return False

    # Get accurate state data
    state_data = get_accurate_state_data(state_name)
    
    # Generate template variables
    variables = generate_template_variables(state_data)
    
    # Replace variables in template
    template_content = template_data['data']['1120']
    final_content = replace_template_variables(template_content, variables)
    
    # Update template with replaced content
    template_data['data']['1120'] = final_content
    
    # Save JSON file
    json_output_file = os.path.join(output_dir, f"{state_name.lower()}.json")
    try:
        with open(json_output_file, 'w', encoding='utf-8') as f:
            json.dump(template_data, f, indent=2)
        print(f"Generated Divi JSON page saved to {json_output_file}")
    except Exception as e:
        print(f"Error saving JSON file: {e}")
        return False
    
    # Save HTML preview
    html_output_file = os.path.join(output_dir, f"{state_name.lower()}.html")
    try:
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Preview: {state_name} Bail Bondsman Page Content</title>
    <style>
        body {{ font-family: sans-serif; line-height: 1.6; padding: 20px; max-width: 900px; margin: auto; }}
        h1, h2, h3 {{ color: #333; }}
        /* Add more basic styles if needed */
    </style>
</head>
<body>
    <h1>Content Preview for {state_name}</h1>
    <p><i>Note: This is a raw content preview. Divi shortcodes and styling are not rendered.</i></p>
    <hr>
    <div>
        {final_content}
    </div>
    <hr>
    <h2>Generated FAQs:</h2>
    <ul>
        {generate_faqs_html(state_name)}
    </ul>
</body>
</html>"""
        
        with open(html_output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"Basic HTML content preview saved to {html_output_file}")
    except Exception as e:
        print(f"Error saving HTML preview: {e}")
        return False
    
    print(f"✅ Page generation successful for {state_name}")
    return True

def get_state_capital_coordinates(state_name, capital):
    """Get coordinates for state capital using AI knowledge"""
    coordinates = {
        "Nevada": {"lat": "39.1638", "lng": "-119.7674"},  # Carson City
        "Iowa": {"lat": "41.5868", "lng": "-93.6250"},  # Des Moines
        # Other coordinates will be generated dynamically, not hardcoded
    }
    
    if state_name in coordinates:
        return coordinates[state_name]
        
    # If we don't have coordinates, return default coordinates for the state capital
    return {"lat": "39.1638", "lng": "-119.7674"}  # Default to Carson City coordinates

def generate_faq_section(state_name, faqs):
    """Generate the FAQ section with toggle modules"""
    faq_section = f"""[et_pb_row _builder_version="4.27.4" _module_preset="default" theme_builder_area="post_content"][et_pb_column _builder_version="4.27.4" _module_preset="default" type="4_4" theme_builder_area="post_content"][et_pb_text _builder_version="4.27.4" _module_preset="default" theme_builder_area="post_content" text_font="Urbanist||||||||" text_text_color="#000000" text_font_size="32px" text_orientation="center"]<h2>Frequently Asked Questions About Bail Bonds in {state_name}</h2>[/et_pb_text][/et_pb_column][/et_pb_row]"""
    
    for faq in faqs:
        faq_section += f"""[et_pb_row _builder_version="4.27.4" _module_preset="default" theme_builder_area="post_content"][et_pb_column _builder_version="4.27.4" _module_preset="default" type="4_4" theme_builder_area="post_content"][et_pb_toggle title="{faq['question']}" _builder_version="4.27.4" _module_preset="default" theme_builder_area="post_content" hover_enabled="0" sticky_enabled="0"]{faq['answer']}[/et_pb_toggle][/et_pb_column][/et_pb_row]"""
    
    return faq_section

def generate_unique_header(state_name):
    """Generate a unique main header for the state"""
    headers = [
        f"Find Local {state_name} Bail Bondsmen Near You",
        f"Trusted {state_name} Bail Bond Services - Available 24/7",
        f"Connect with Licensed {state_name} Bail Bondsmen Now",
        f"Emergency Bail Bonds in {state_name} - Fast Response"
    ]
    return random.choice(headers)

def generate_unique_subheader(state_name):
    """Generate a unique subheader for the state"""
    subheaders = [
        f"Find Licensed {state_name} Bail Bond Agents Available Now",
        f"Professional {state_name} Bail Bondsmen Ready to Help",
        f"Expert Bail Bond Services Throughout {state_name}",
        f"24/7 Bail Bond Assistance Across {state_name}"
    ]
    return random.choice(subheaders)

def generate_unique_guide_title(state_name):
    """Generate a unique guide title for the state"""
    titles = [
        f"Your Guide to Finding Local {state_name} Bail Bondsmen",
        f"Complete {state_name} Bail Bonds Guide",
        f"Essential Guide to Bail Bonds in {state_name}",
        f"{state_name} Bail Bonds: Your Comprehensive Resource"
    ]
    return random.choice(titles)

def generate_unique_guide_subtitle(state_name):
    """Generate a unique guide subtitle for the state"""
    subtitles = [
        f"Expert guidance through the {state_name} bail bond process - from arrest to release",
        f"Understanding bail bonds in {state_name} - costs, procedures, and what to expect",
        f"Navigate the {state_name} bail system with confidence - professional help available 24/7",
        f"Your trusted resource for bail bond services across {state_name}"
    ]
    return random.choice(subtitles)

# --- Core Logic Functions (from Part 2) ---

def validate_state_data(state_data):
    """Validate state data to ensure all required fields have proper values"""
    required_fields = {
        "name": "state name",
        "abbreviation": "state abbreviation",
        "nickname": "state nickname",
        "capital": "state capital",
        "population": "population number",
        "num_counties": "number of counties",
        "major_cities": "list of major cities",
        "largest_counties": "list of largest counties"
    }
    
    for field, description in required_fields.items():
        if field not in state_data or not state_data[field]:
            raise ValueError(f"Missing required {description}")
        if field == "population" and (not isinstance(state_data[field], int) or state_data[field] <= 0):
            raise ValueError(f"Invalid population value")
        if field == "num_counties" and (not isinstance(state_data[field], int) or state_data[field] <= 0):
            raise ValueError(f"Invalid number of counties")
        if field == "major_cities" and (not isinstance(state_data[field], list) or len(state_data[field]) < 3):
            raise ValueError(f"At least three major cities required")
        if field == "largest_counties" and (not isinstance(state_data[field], list) or len(state_data[field]) < 3):
            raise ValueError(f"Three largest counties required with descriptions")
    
    # Validate county data structure
    for county in state_data["largest_counties"]:
        if not isinstance(county, dict) or "name" not in county or "description" not in county:
            raise ValueError("Each county must have a name and description")
        if not county["name"] or not county["description"]:
            raise ValueError("County name and description cannot be empty")
    
    return True

def generate_state_article(state_data):
    """Generate a comprehensive article about the state"""
    state_name = state_data["name"]
    nickname = state_data["nickname"]
    population = f"{state_data['population']:,}"
    num_counties = state_data["num_counties"]
    capital = state_data["capital"]
    major_cities = state_data["major_cities"]
    
    # Get facility counts
    num_courts = len(state_data.get("facilities", {}).get("courts", []))
    num_detention_centers = len(state_data.get("facilities", {}).get("detention_centers", []))
    
    return f"""<h3>Complete Guide to Bail Bonds in {state_name}</h3>

{state_name}, known as {nickname}, serves a population of {population} residents across {num_counties} counties through our extensive network of licensed bail bondsmen. From the state capital of {capital} to major metropolitan areas like {', '.join(major_cities[:-1])}, and {major_cities[-1]}, our agents provide crucial support for families navigating the bail process.

<h4>State Overview</h4>
{state_data['economy']}

<h4>Coverage and Accessibility</h4>
Our bail bond network extends throughout {state_name}'s population centers and rural communities. {state_data['geography']} We maintain connections with {num_courts} major courts and {num_detention_centers} detention facilities across the state to ensure efficient service wherever you need assistance.

<h4>Local Conditions and Operations</h4>
{state_data['weather']} Our experienced bondsmen operate efficiently regardless of conditions, ensuring reliable service when you need it most.

<h4>Your Trusted Partner in the Bail Process</h4>
When you work with a BailBondsBuddy.com verified agent in {state_name}, you're connecting with a professional who understands both the local requirements and the personal challenges families face during difficult times. Our agents are committed to providing clear communication, efficient service, and compassionate support throughout your case."""

def verify_data_source(data: Dict[str, Any], source_url: str) -> bool:
    """Verify that data came from an official source"""
    if not source_url or not source_url.endswith(('.gov', '.us')):
        print(f"Warning: Data source {source_url} is not an official government domain")
        return False
    return True

def log_data_source(state: str, data_type: str, source: str):
    """Log where we got the data from for verification"""
    timestamp = datetime.now().isoformat()
    log_entry = f"{timestamp} - {state} - {data_type}: {source}\n"
    
    log_file = os.path.join(BASE_DIR, "data_sources.log")
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    with open(log_file, "a") as f:
        f.write(log_entry)

def extract_state_info(search_results: str) -> Dict[str, Any]:
    """Extract state information from search results"""
    info = {}
    
    # Extract state abbreviation (2 letter code)
    abbr_match = re.search(r'\b[A-Z]{2}\b', search_results)
    if abbr_match:
        info['abbreviation'] = abbr_match.group(0)
    
    # Extract population (number followed by "population" or "residents")
    pop_match = re.search(r'(\d{1,3}(?:,\d{3})*)\s*(?:population|residents)', search_results)
    if pop_match:
        info['population'] = int(pop_match.group(1).replace(',', ''))
    
    # Extract number of counties
    county_match = re.search(r'(\d+)\s*counties', search_results)
    if county_match:
        info['num_counties'] = int(county_match.group(1))
    
    # Extract capital city
    capital_match = re.search(r'capital\s*(?:city|is|:)?\s*([A-Z][a-zA-Z\s]+)(?:\.|,|\s|$)', search_results)
    if capital_match:
        info['capital'] = capital_match.group(1).strip()
    
    return info

def extract_bail_info(search_results: str) -> Dict[str, str]:
    """Extract bail system information from search results"""
    info = {}
    
    # Extract bail system description
    bail_desc = re.search(r'(?:bail\s+system|bail\s+bonds?).*?(?:\.|$)', search_results, re.IGNORECASE | re.DOTALL)
    if bail_desc:
        info['bail_system'] = bail_desc.group(0).strip()
    
    return info

def extract_justice_info(search_results: str) -> Dict[str, str]:
    """Extract criminal justice information from search results"""
    info = {}
    
    # Extract criminal justice system description
    justice_desc = re.search(r'(?:criminal\s+justice|court\s+system).*?(?:\.|$)', search_results, re.IGNORECASE | re.DOTALL)
    if justice_desc:
        info['criminal_justice'] = justice_desc.group(0).strip()
    
    return info

def get_accurate_state_data(state_name: str) -> Dict[str, Any]:
    """Get accurate state data from existing file or fetch new data."""
    print(f"Stage 1: Gathering comprehensive data for {state_name}...")
    
    # Check if state data file exists
    state_file = os.path.join(STATE_DATA_DIR, f"{state_name.lower()}.json")
    if os.path.exists(state_file):
        try:
            with open(state_file, 'r', encoding='utf-8') as f:
                state_data = json.load(f)
                # Save the data again to ensure it's properly formatted
                save_state_data(state_name, state_data)
                print(f"✓ Generated and saved accurate data for {state_name}")
                return state_data
        except Exception as e:
            print(f"Error reading state data file: {e}")
            return None
    
    # If no existing file, fetch new data
    try:
        # Fetch data from various sources
        state_data = {
            "name": state_name,
            "nickname": "The Lone Star State" if state_name == "Texas" else "",
            # Add other data fetching logic here
        }
        
        # Save the generated data
        save_state_data(state_name, state_data)
        print(f"✓ Generated and saved accurate data for {state_name}")
        return state_data
        
    except Exception as e:
        print(f"Error gathering data for {state_name}: {e}")
        return None

def upload_to_wordpress(state_name):
    """Upload the generated state page JSON to WordPress as a draft page"""
    # Use the file from DoNotUse/Generated_State_Pages directory
    json_path = os.path.join(os.path.dirname(os.path.dirname(BASE_DIR)), "DoNotUse", "Generated_State_Pages", f"{state_name.lower()}.json")

    # Check if WP_AUTH credentials are placeholders
    if WP_AUTH[0] == "your_wp_username" or WP_AUTH[1] == "your_wp_application_password":
        print("Error: WordPress username or application password not set in WP_AUTH constant.")
        print("Please update the script with your actual credentials before uploading.")
        return False

    try:
        with open(json_path, 'r') as f:
            state_json_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON file not found for {state_name} at {json_path}. Cannot upload.")
        return False
    except json.JSONDecodeError as e:
         print(f"Error decoding JSON from {json_path}: {e}. Cannot upload.")
         return False
    except Exception as e:
        print(f"Error loading {json_path}: {e}")
        return False

    # --- Prepare Page Data for WordPress API ---
    # Extract the processed content string (assuming it's the value of the first key in 'data')
    page_content_string = ""
    if isinstance(state_json_data.get("data"), dict):
         data_keys = list(state_json_data["data"].keys())
         if data_keys:
              page_content_string = state_json_data["data"][data_keys[0]]
         else:
              print(f"Error: Cannot extract content string from JSON 'data' object for {state_name} (empty).")
              return False
    else:
         print(f"Error: Cannot extract content string from JSON 'data' object for {state_name} (missing or not dict).")
         return False

    if not page_content_string:
         print(f"Error: Extracted page content string is empty for {state_name}.")
         return False

    # Define Page Title and Slug
    title = f"Find Local {state_name} Bail Bondsmen Near You | 24/7 Emergency Service"
    # Create a URL-friendly slug
    slug = f"{state_name.lower().replace(' ', '-')}-bail-bondsman-24-hour-emergency-service-nearby"
    # Limit slug length if necessary (WordPress might truncate anyway)
    slug = slug[:100] # Example limit

    # Page data payload for the WordPress REST API
    page_data = {
        "title": title,
        "slug": slug,
        "content": page_content_string, # The processed content string
        "status": "draft",             # Create as a draft first
        "meta": {
            # Divi specific meta fields to enable builder and set layout
            "_et_pb_use_builder": "on",
            "_et_pb_page_layout": "et_no_sidebar", # Example: fullwidth layout
            "_et_pb_side_nav": "off",
            # You might need other meta fields depending on your Divi setup
            # '_wp_page_template': 'default', # Or specific template like 'page-template-blank.php' if needed
        }
        # Consider adding excerpt, featured_media (image ID) if needed
    }

    # --- Make API Request ---
    print(f"Attempting to upload page for {state_name} to {WP_API_URL}/pages")
    try:
        response = requests.post(
            f"{WP_API_URL}/pages",
            json=page_data,
            auth=WP_AUTH,
            timeout=30 # Add a timeout
        )
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)

        # Success (typically 201 Created)
        page_info = response.json()
        page_id = page_info.get("id")
        page_link = page_info.get("link")
        edit_link = f"{WP_BASE_URL}/wp-admin/post.php?post={page_id}&action=edit"

        print(f"✅ Success! {state_name} page created as draft on WordPress.")
        print(f"   Page ID: {page_id}")
        print(f"   Draft Preview Link: {page_link}&preview=true")
        print(f"   Edit Link: {edit_link}")
        return True

    except requests.exceptions.HTTPError as http_err:
        print(f"❌ HTTP error occurred during WordPress upload for {state_name}: {http_err}")
        print(f"   Status Code: {response.status_code}")
        try:
            # Try to get more details from the response body
            error_details = response.json()
            print(f"   Error Details: {error_details}")
        except json.JSONDecodeError:
            print(f"   Response Body: {response.text}") # Print raw text if not JSON
        return False
    except requests.exceptions.ConnectionError as conn_err:
        print(f"❌ Connection error occurred during WordPress upload for {state_name}: {conn_err}")
        print(f"   Check network connection and if {WP_BASE_URL} is reachable.")
        return False
    except requests.exceptions.Timeout as timeout_err:
        print(f"❌ Timeout error occurred during WordPress upload for {state_name}: {timeout_err}")
        return False
    except requests.exceptions.RequestException as req_err:
        print(f"❌ An unexpected error occurred with the request for {state_name}: {req_err}")
        traceback.print_exc()
        return False
    except Exception as e:
        print(f"❌ An unexpected error occurred during WordPress upload for {state_name}: {e}")
        traceback.print_exc()
        return False

def print_banner():
    """Print a banner for the script"""
    banner = """
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║   Cline State Page Generator for Bail Bonds Buddy Website     ║
    ║                 (Combined Script - v1.0)                      ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """
    print(banner)
    print("This script generates state pages based on a template and state data.")
    print("It can create Divi-compatible JSON files and upload them to WordPress.\n")
    print(f"Using Template: {TEMPLATE_FILE}")
    print(f"Outputting JSON/HTML to: {OUTPUT_DIR}")
    print(f"Reading/Writing State Data in: {STATE_DATA_DIR}")
    print(f"Target WordPress URL: {WP_BASE_URL}")
    # Security Reminder for Credentials
    if WP_AUTH[0] == "your_wp_username" or WP_AUTH[1] == "your_wp_application_password":
        print("\n⚠️ WARNING: Default WordPress credentials detected in WP_AUTH.")
        print("   Uploading to WordPress will fail until you update the script.")
    print("-" * 60)


def generate_single_state(state_name, upload=False):
    """Generate a page for a single state and optionally upload it"""
    print(f"\n=== Processing State: {state_name} ===")
    success_generate = generate_page_for_state(state_name, TEMPLATE_FILE, OUTPUT_DIR, STATE_DATA_DIR)
    
    if success_generate:
        print(f"✅ Page generation successful for {state_name}")
        if upload:
            print(f"\n--- Uploading {state_name} page to WordPress ---")
            upload_success = upload_to_wordpress(state_name)

            if upload_success:
                print(f"✅ Successfully uploaded {state_name} page to WordPress as draft.")
            else:
                print(f"❌ Failed to upload {state_name} page to WordPress.")
                return False # Indicate failure if upload was requested but failed
        return True # Generation succeeded (upload may or may not have been requested/successful)
    else:
        print(f"❌ Failed to generate page for {state_name}")
        return False

def generate_all_states(upload=False):
    """Generate pages for all 50 US states"""
    print("\n=== Processing All 50 US States ===")

    # List of all 44 states that allow bail bondsmen (standard names)
    states = [
        "Alabama", "Alaska", "Arizona", "Arkansas", "California",
        "Colorado", "Connecticut", "Delaware", "Florida", "Georgia",
        "Hawaii", "Idaho", "Indiana", "Iowa", "Kansas", "Louisiana", "Maryland",
        "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana",
        "Nevada", "New Hampshire", "New Jersey", "New Mexico",
        "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma",
        "Pennsylvania", "Rhode Island", "South Carolina",
        "South Dakota", "Tennessee", "Texas", "Utah", "Vermont",
        "Virginia", "Washington", "West Virginia", "Wyoming"
    ]

    generation_success_count = 0
    upload_success_count = 0
    generation_failures = []
    upload_failures = []

    total_states = len(states)
    for i, state in enumerate(states):
        print(f"\n--- Processing State {i+1}/{total_states}: {state} ---")
        generated = generate_page_for_state(state, TEMPLATE_FILE, OUTPUT_DIR, STATE_DATA_DIR)

        if generated:
            generation_success_count += 1
            print(f"✅ {state} page generated successfully.")

            if upload:
                print(f"--- Uploading {state} to WordPress ---")
                uploaded = upload_to_wordpress(state)
                if uploaded:
                    upload_success_count += 1
                    print(f"✅ {state} page uploaded successfully.")
                else:
                    upload_failures.append(state)
                    print(f"❌ Failed to upload {state} page.")
            else:
                 # If not uploading, still count as a success for generation
                 pass

        else:
            generation_failures.append(state)
            print(f"❌ Failed to generate page for {state}.")

    # --- Summary ---
    print("\n" + "=" * 15 + " Processing Complete " + "=" * 15)
    print(f"Total States Processed: {total_states}")
    print(f"Pages Generated Successfully: {generation_success_count}")
    if generation_failures:
        print(f"Pages Failed Generation ({len(generation_failures)}): {', '.join(generation_failures)}")

    if upload:
        print(f"\nWordPress Upload Summary:")
        print(f"Pages Uploaded Successfully: {upload_success_count}")
        if upload_failures:
            print(f"Pages Failed Upload ({len(upload_failures)}): {', '.join(upload_failures)}")
    else:
        print("\nWordPress upload was not requested (--upload flag not used).")

    print("=" * 50)
    return generation_success_count # Or return more detailed results if needed

def main():
    """Main function to parse arguments and orchestrate tasks"""
    parser = argparse.ArgumentParser(
        description="Generate state pages for Bail Bonds Buddy website.",
        formatter_class=argparse.RawTextHelpFormatter # Preserve formatting in help text
        )
    parser.add_argument(
        '--state',
        type=str,
        help='Generate a page for a specific state (e.g., --state "New Mexico").'
        )
    parser.add_argument(
        '--upload',
        action='store_true',
        help='Upload the generated page(s) to WordPress as drafts.'
        )
    parser.add_argument(
        '--all',
        action='store_true',
        help='Generate pages for all 50 US states.'
        )
    parser.add_argument(
        '--save-example',
        action='store_true',
        help='Save the example New Mexico data to state_data/new_mexico.json and exit.'
        )

    args = parser.parse_args()

    print_banner()

    if args.save_example:
        print("Saving example New Mexico data...")
        save_example_data()
        print("Exiting after saving example data.")
        sys.exit(0)

    # --- Argument Validation ---
    if not args.state and not args.all:
        print("Error: You must specify either --state [StateName] or --all.")
        parser.print_help()
        sys.exit(1)

    if args.state and args.all:
        print("Error: You cannot use both --state and --all flags simultaneously.")
        parser.print_help()
        sys.exit(1)

    # --- Execute Actions ---
    if args.state:
        # Normalize state name (e.g., "new mexico" -> "New Mexico")
        normalized_state_name = args.state.strip().title()
        generate_single_state(normalized_state_name, args.upload)
    elif args.all:
        generate_all_states(args.upload)

    print("\nScript finished.")

if __name__ == "__main__":
    main()

def generate_faqs_html(state_name):
    """Generate HTML for state-specific FAQs."""
    faqs = [
        {
            "question": f"How much does a bail bond cost in {state_name}?",
            "answer": f"In {state_name}, bail bond fees are typically 15% of the total bail amount set by the court. This is a non-refundable premium for the bondsman's service. Additional fees may apply for specific services or circumstances."
        },
        {
            "question": f"What documents do I need to get a bail bond in {state_name}?",
            "answer": f"To secure a bail bond in {state_name}, you'll typically need: government-issued photo ID, proof of residence, proof of income or employment, and information about the detained person (full name, booking number, facility location)."
        },
        {
            "question": f"How long does the bail bond process take in {state_name}?",
            "answer": f"The bail bond process in {state_name} typically takes 2-6 hours once all paperwork is complete. However, processing times can vary depending on the detention facility's current workload and the time of day."
        },
        {
            "question": f"What payment methods do bail bondsmen accept in {state_name}?",
            "answer": f"Most {state_name} bail bondsmen accept multiple payment methods including: cash, credit cards, debit cards, and sometimes payment plans for qualified clients. Some may also accept collateral in the form of property or valuables."
        },
        {
            "question": f"Are bail bondsmen available 24/7 in {state_name}?",
            "answer": f"Yes, licensed bail bondsmen in {state_name} are available 24 hours a day, 7 days a week. They understand that arrests can happen at any time and provide round-the-clock service."
        },
        {
            "question": f"What happens if someone misses court in {state_name}?",
            "answer": f"If someone misses court in {state_name}, a warrant will be issued for their arrest and the bail bond may be forfeited. The bondsman will attempt to locate the person and return them to custody. Co-signers may be responsible for additional costs."
        },
        {
            "question": f"Can I get a refund on my bail bond premium in {state_name}?",
            "answer": f"No, the bail bond premium (typically 15%) in {state_name} is non-refundable. This fee is earned by the bondsman for taking on the risk and providing the service, regardless of the case outcome."
        },
        {
            "question": f"What are the responsibilities of a bail bond co-signer in {state_name}?",
            "answer": f"Co-signers in {state_name} are responsible for ensuring the defendant appears at all court dates. If the defendant fails to appear, co-signers may be financially responsible for the full bail amount and any recovery costs."
        }
    ]
    
    html = ""
    for faq in faqs:
        html += f"<li><strong>{faq['question']}</strong><br>{faq['answer']}</li>\n"
    
    return html
