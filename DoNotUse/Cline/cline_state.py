#!/usr/bin/env python3
"""
Cline State Page Generator for Bail Bonds Buddy (Part 1)

This script defines the state data structure and provides example data for New Mexico.
It works together with cline_state_part2.py and cline_state_part3.py to provide a complete solution.

Usage:
  python3 cline_state_part3.py --state [StateName]         # Generate a state page
  python3 cline_state_part3.py --state [StateName] --upload # Generate and upload to WordPress
  python3 cline_state_part3.py --all                       # Generate all state pages
"""

import os
import json

# Constants
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_FILE = os.path.join(BASE_DIR, "templates", "State-Template-Page-Only-Variables.json")
OUTPUT_DIR = os.path.join(BASE_DIR, "generated_pages")
STATE_DATA_DIR = os.path.join(BASE_DIR, "state_data")

# WordPress API details
WP_BASE_URL = "https://bailbondsbuddy.com"
WP_API_URL = f"{WP_BASE_URL}/wp-json/wp/v2"
WP_AUTH = ("bbbuddy", "DpSm eiz8 yHjx Sqqk G3lG fqU6")

# Create output directories if they don't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(STATE_DATA_DIR, exist_ok=True)

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
    "population": 2100000,
    "num_counties": 33,
    "largest_counties": [
        {"name": "Bernalillo County", "description": "Home to Albuquerque, the state's largest city"},
        {"name": "Doña Ana County", "description": "Contains Las Cruces, the state's second-largest city"},
        {"name": "Santa Fe County", "description": "Home to the state capital"}
    ],
    "major_cities": ["Albuquerque", "Las Cruces", "Rio Rancho", "Santa Fe"],
    "economy": "New Mexico's economy is based on oil and gas production, tourism, and federal government spending. The state is home to several national laboratories and military bases, which contribute significantly to its economy.",
    "bail_system": "New Mexico underwent significant bail reform in 2016 when voters approved a constitutional amendment that changed how courts determine which defendants stay in jail before trial. The system now relies more on risk assessments than on a defendant's ability to pay.",
    "criminal_justice": "New Mexico has been working on criminal justice reforms to address its high crime rates, particularly in urban areas like Albuquerque. These reforms focus on reducing recidivism and addressing substance abuse issues that contribute to criminal behavior.",
    "geography": "New Mexico's vast, rural landscape with significant distances between population centers can create challenges for the bail system. The state's position along the U.S.-Mexico border also results in specific types of cases related to immigration and cross-border activities.",
    "weather": "New Mexico's climate varies dramatically from desert to alpine conditions. Severe weather, particularly winter storms in mountainous regions, can occasionally impact court schedules and bail processing timelines.",
    "faqs": [
        {
            "question": "How long does it take to get released using a bail bond in New Mexico?",
            "answer": "After a bail bond is posted in New Mexico, release times typically range from 2-8 hours depending on the facility's processing speed and how busy they are. Weekend and holiday arrests may take longer to process. The bondsman will keep you updated on the progress."
        },
        {
            "question": "What kind of collateral is accepted for bail bonds in New Mexico?",
            "answer": "Common forms of collateral accepted by New Mexico bail bondsmen include real estate, vehicles, jewelry, stocks, and bonds. The value of the collateral should generally exceed the bail amount. For real estate, you'll need to provide property deeds, recent appraisals, and proof that your equity exceeds the bail amount."
        },
        {
            "question": "What is the typical cost of a bail bond in New Mexico?",
            "answer": "The standard premium for a bail bond in New Mexico is 10% of the full bail amount, which is non-refundable. For example, if the court sets bail at $10,000, you would pay approximately $1,000 to a bail bondsman. Some New Mexico bondsmen offer payment plans or accept collateral for larger bail amounts."
        },
        {
            "question": "What information do I need when contacting a New Mexico bail bondsman?",
            "answer": "When calling a New Mexico bail bondsman, you should have the defendant's full name, where they're being held (which New Mexico jail or detention facility), their booking number, what charges they're facing, and the bail amount if it's been set. Having this information ready helps the bondsman start the process immediately, saving valuable time."
        },
        {
            "question": "What types of payments do New Mexico bail bondsmen accept?",
            "answer": "Most New Mexico bail bondsmen accept various payment methods including cash, credit/debit cards, money orders, and sometimes property as collateral. Many offer payment plans for larger bail amounts and now accept digital payment options such as Venmo, PayPal, or Cash App for convenience."
        }
    ]
}

def save_example_data():
    """Save the example New Mexico data to a JSON file"""
    filename = os.path.join(STATE_DATA_DIR, "new_mexico.json")
    try:
        with open(filename, 'w') as f:
            json.dump(NEW_MEXICO_DATA, f, indent=2)
        print(f"Example data for New Mexico saved to {filename}")
        return True
    except Exception as e:
        print(f"Error saving example data: {e}")
        return False

if __name__ == "__main__":
    # Create the output directories
    print(f"Creating output directories...")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(STATE_DATA_DIR, exist_ok=True)
    
    # Save the example data
    save_example_data()
    
    print(f"State data template and example data initialized.")
    print(f"Use cline_state_part3.py to generate state pages.")
