#!/usr/bin/env python3
"""
Cline State Page Generator for Bail Bonds Buddy (Combined Script)

This script combines the functionality of cline_state.py, cline_state_part2.py,
and cline_state_part3.py into a single file. It defines state data structures,
provides example data, generates state-specific pages based on a template,
and can upload these pages to a WordPress site.

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

# Third-party Imports
import requests # Ensure 'requests' library is installed: pip install requests

# --- Constants (Combined from all parts) ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_FILE = os.path.join(BASE_DIR, "templates", "State-Template-Page-Only-Variables.json")
OUTPUT_DIR = os.path.join(BASE_DIR, "generated_pages")
STATE_DATA_DIR = os.path.join(BASE_DIR, "state_data")

# WordPress API details
WP_BASE_URL = "https://bailbondsbuddy.com" # Replace with your actual domain if different
WP_API_URL = f"{WP_BASE_URL}/wp-json/wp/v2"
# IMPORTANT: Replace with your actual WordPress username and Application Password
# Never hardcode credentials directly in production code. Consider environment variables or a config file.
WP_AUTH = ("bbbuddy", "DpSm eiz8 yHjx Sqqk G3lG fqU6") # <<< DO NOTCHANGE THESE

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

# --- Helper Functions (Combined from Parts 1 & 2) ---

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
    """Generate unique FAQs for a state page"""
    # FAQ 1: Release time
    faq1_questions = [
        f"How long does it take to get released using a bail bond in {state_name}?",
        f"What's the typical release timeframe after posting bail in {state_name}?",
        f"How quickly can someone be released from jail in {state_name} after a bail bond is posted?",
        f"What's the average processing time for bail bonds in {state_name}?",
        f"How soon can I expect release after a bail bondsman posts bail in {state_name}?"
    ]

    faq1_answers = [
        f"After a bail bond is posted in {state_name}, release times typically range from 2-8 hours depending on the facility's processing speed and how busy they are. Weekend and holiday arrests may take longer to process. The bondsman will keep you updated on the progress.",
        f"In {state_name}, once a bail bond is posted, release processing usually takes between 3-6 hours, though this varies by facility and current booking volume. During busy periods or weekends, processing may take longer. Your bail agent will provide regular updates throughout the process.",
        f"Release times in {state_name} detention facilities typically range from 4-10 hours after a bail bond is posted, depending on the facility's size, staffing levels, and current occupancy. Releases during nights, weekends, or holidays may experience additional delays. Your bondsman will monitor the process and keep you informed.",
        f"In {state_name}, the release process after posting a bail bond generally takes 2-6 hours, though this timeframe can vary significantly based on the detention facility, time of day, and current processing volume. Your bail bondsman will track the progress and provide updates throughout the process.",
        f"After a bail bond is posted in {state_name}, release typically occurs within 3-8 hours, though processing times vary by facility and current conditions. Factors affecting release speed include the detention center's size, current occupancy, staffing levels, and time of day. Your bail agent will monitor the situation and keep you informed."
    ]

    # FAQ 2: Collateral
    faq2_questions = [
        f"What kind of collateral is accepted for bail bonds in {state_name}?",
        f"What assets can be used as collateral for a {state_name} bail bond?",
        f"What types of property can secure a bail bond in {state_name}?",
        f"What collateral options are available for bail bonds in {state_name}?",
        f"What can I use as security for a bail bond in {state_name}?"
    ]

    faq2_answers = [
        f"In {state_name}, bail bondsmen typically accept various forms of collateral including real estate (homes, land, investment properties), vehicles with clear titles, jewelry, electronics, firearms, and in some cases, credit card payments or cash. The specific collateral requirements depend on the bond amount, the defendant's history, and the bondsman's policies. Some bonds may require multiple forms of collateral to secure the full amount.",
        f"{state_name} bail bond agencies generally accept several types of collateral including real property (houses, land, commercial buildings), vehicles, valuable jewelry, electronic equipment, and sometimes investment accounts or certificates of deposit. The value of collateral typically needs to exceed the bond amount, and requirements vary based on the defendant's risk assessment and the bondsman's specific policies.",
        f"Bail bondsmen in {state_name} commonly accept various forms of collateral such as real estate titles, vehicle ownership documents, valuable jewelry, electronics, firearms (where legal), and sometimes bank account holds or credit card authorizations. The specific requirements vary by agency and depend on factors like the bond amount, the defendant's background, and the perceived flight risk.",
        f"For bail bonds in {state_name}, acceptable collateral typically includes real property deeds, vehicle titles, valuable jewelry and watches, electronic equipment, firearms (with proper documentation), and sometimes bank accounts or investment portfolios. Most bondsmen require collateral valued higher than the actual bond amount to protect against potential losses if the defendant fails to appear.",
        f"{state_name} bail bond agencies generally accept collateral in forms such as real estate equity, vehicle titles, valuable personal property (jewelry, electronics, collectibles), and sometimes financial instruments like certificates of deposit. The specific requirements vary by bondsman and depend on the bond amount, the defendant's history, and the assessed flight risk."
    ]

    # FAQ 3: Cost
    faq3_questions = [
        f"What is the typical cost of a bail bond in {state_name}?",
        f"How much do bail bondsmen charge in {state_name}?",
        f"What fees do bail bond services charge in {state_name}?",
        f"How is the cost of a bail bond calculated in {state_name}?",
        f"What should I expect to pay for a bail bond in {state_name}?"
    ]

    faq3_answers = [
        f"In {state_name}, bail bond fees typically range from 10-15% of the total bail amount, though this can vary by county and individual bondsman. For example, a $10,000 bail would cost $1,000-$1,500 in non-refundable fees. Some bondsmen offer payment plans for larger amounts. Additional costs may include court filing fees, travel expenses for out-of-county service, or credit card processing fees.",
        f"{state_name} law typically sets bail bond premiums at 10% of the total bail amount, though some bondsmen may charge up to 15% depending on risk factors and bond size. This fee is non-refundable regardless of case outcome. For example, a $5,000 bail would require a $500 premium payment. Some agencies offer financing options for larger bonds, and additional fees may apply for special circumstances.",
        f"Bail bond costs in {state_name} are generally set at 10% of the total bail amount as a standard premium rate. For instance, a $20,000 bail would require a $2,000 non-refundable payment to the bondsman. Higher-risk cases or specialized bonds may incur additional fees. Many bondsmen offer payment plans for larger amounts, though this typically requires a larger initial payment and verified income.",
        f"The standard rate for bail bonds in {state_name} is typically 10% of the full bail amount, which serves as the bondsman's non-refundable fee. For example, securing release on a $15,000 bail would cost approximately $1,500. Some bondsmen may charge additional fees for high-risk defendants or unusual circumstances. Many agencies offer payment plans, though these often require good credit history or additional collateral.",
        f"In {state_name}, bail bondsmen typically charge a premium of 10% of the total bail amount. This fee is non-refundable and represents the cost of the bondsman's service. For instance, a $25,000 bail would require a $2,500 payment. Some agencies may offer discounts for military personnel, union members, or clients with private attorneys. Payment plans are often available but may require additional collateral or co-signers."
    ]

    # FAQ 4: Information needed
    faq4_questions = [
        f"What information do I need when contacting a bail bondsman in {state_name}?",
        f"What details should I have ready when calling a {state_name} bail bonds service?",
        f"What information will a {state_name} bail bondsman ask for?",
        f"What should I prepare before contacting a bail bonds agency in {state_name}?",
        f"What information is required to arrange a bail bond in {state_name}?"
    ]

    faq4_answers = [
        f"When contacting a bail bondsman in {state_name}, you should have the following information ready: the full legal name of the detained person, their date of birth, the facility where they're being held, the booking or case number if available, the charge(s), the bail amount if set, and your relationship to the defendant. Additionally, having information about the defendant's employment, community ties, and residence in {state_name} can help expedite the process.",
        f"To efficiently arrange bail in {state_name}, prepare these details before contacting a bondsman: the defendant's complete legal name and birth date, which detention facility they're in, their booking number, the nature of the charges, the bail amount (if determined), and your relationship to the person. Information about the defendant's employment status, length of residence in {state_name}, and family connections can also help the bondsman assess the situation more effectively.",
        f"When calling a bail bondsman in {state_name}, have this essential information ready: the defendant's full name and date of birth, the detention facility's name and location, the booking number (if known), what charges they face, the bail amount if already set, and how you're related to the defendant. Details about the person's job stability, {state_name} residency history, and community connections will also help the bondsman evaluate the case.",
        f"Before contacting a {state_name} bail bonds service, gather these key details: the defendant's complete legal name and birth date, which jail or detention center they're in, their booking or case number, the specific charges, the bail amount (if determined by the court), and your relationship to the detained person. Information about the defendant's employment, {state_name} residence history, and family ties can also facilitate the process.",
        f"To arrange bail bond services in {state_name}, you'll need to provide: the defendant's full legal name and date of birth, the detention facility where they're held, any booking or case numbers, the specific charges, the bail amount if set, and your relationship to the person. The bondsman may also ask about the defendant's employment status, length of residence in {state_name}, and family connections to assess flight risk."
    ]

    # FAQ 5: Payment methods
    faq5_questions = [
        f"What types of payments do bail bondsmen accept in {state_name}?",
        f"How can I pay for a bail bond in {state_name}?",
        f"What payment methods are available for bail bonds in {state_name}?",
        f"What payment options do {state_name} bail bond agencies offer?",
        f"How do I pay a bail bondsman in {state_name}?"
    ]

    faq5_answers = [
        f"Bail bondsmen in {state_name} typically accept multiple payment methods including credit/debit cards, cash, bank transfers, money orders, and personal checks (from established clients). Many agencies also offer payment plans for larger bonds, though these usually require a substantial down payment and may involve additional fees or interest. Some bondsmen also accept various forms of collateral in lieu of full cash payment, such as property, vehicles, or valuable items.",
        f"{state_name} bail bond agencies generally offer flexible payment options including major credit cards, debit cards, cash, electronic transfers, certified checks, and money orders. For larger bail amounts, most bondsmen provide financing options with manageable down payments and installment plans. Some agencies may charge processing fees for credit card transactions or offer discounts for cash payments. Always get a detailed receipt for any payments made.",
        f"Most bail bond services in {state_name} accept various payment methods including cash, credit cards (Visa, MasterCard, American Express, Discover), debit cards, bank transfers, money orders, and cashier's checks. Many bondsmen also offer payment plans for clients who can't pay the full premium upfront, though these arrangements typically require good credit or additional collateral. Some agencies provide online payment options for added convenience.",
        f"Bail bondsmen in {state_name} typically accept multiple payment forms including cash, all major credit and debit cards, electronic bank transfers, money orders, and cashier's checks. For larger bonds, most agencies offer financing options with reasonable down payments and structured payment plans. Some bondsmen provide mobile payment services and can process transactions remotely. Always ensure you receive proper documentation for all payments.",
        f"{state_name} bail bond agencies generally accept various payment methods including cash, credit cards, debit cards, electronic transfers, money orders, and cashier's checks. Many bondsmen offer flexible payment plans for clients unable to pay the full premium immediately. These financing arrangements typically require a down payment (often 25-35% of the premium) and verifiable income or additional collateral. Some agencies charge convenience fees for certain payment methods."
    ]

    # Select random questions and answers for variety
    faqs = [
        {"question": random.choice(faq1_questions), "answer": random.choice(faq1_answers)},
        {"question": random.choice(faq2_questions), "answer": random.choice(faq2_answers)},
        {"question": random.choice(faq3_questions), "answer": random.choice(faq3_answers)},
        {"question": random.choice(faq4_questions), "answer": random.choice(faq4_answers)},
        {"question": random.choice(faq5_questions), "answer": random.choice(faq5_answers)},
    ]
    return faqs

# --- Unique Content Generation Functions (Placeholder - Adapt as needed) ---
# These functions were referenced but not fully defined in the original scripts.
# Provide actual logic here or replace calls with static text/data lookups.

def generate_unique_guide_paragraph(state_name):
    """Generates a unique guide paragraph for the state."""
    # Placeholder - Replace with actual logic or data lookup
    return f"Navigating the bail bond process in {state_name} can be complex. This guide provides essential information and connects you with licensed local bail bondsmen ready to assist you 24/7. We cover costs, procedures, and what to expect."

def generate_unique_intro_paragraph(state_name):
    """Generates a unique introductory paragraph for the state."""
    # Placeholder - Replace with actual logic or data lookup
    return f"Finding a reliable bail bondsman in {state_name} quickly is crucial when facing an arrest. Bail Bonds Buddy simplifies this process by offering a comprehensive directory of verified, licensed bail bond agents across {state_name}. Whether you're in a major city or a rural county, help is available."

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

def replace_template_variables(template_content, state_data):
    """Replace template variables with state-specific content"""
    state_name = state_data.get("name", "Unknown State")
    nickname = state_data.get("nickname", "Unknown Nickname")
    population = state_data.get("population", "N/A")
    num_counties = state_data.get("num_counties", "N/A")
    major_cities = state_data.get("major_cities", ["Unknown City 1", "Unknown City 2"])
    economy = state_data.get("economy", f"Details about the economy of {state_name} are being compiled.")
    bail_system = state_data.get("bail_system", f"Information on the specific bail system in {state_name} is being updated.")
    criminal_justice = state_data.get("criminal_justice", f"Context regarding criminal justice in {state_name} is under review.")
    geography = state_data.get("geography", f"Geographical factors affecting bail in {state_name} are being analyzed.")
    weather = state_data.get("weather", f"Weather patterns in {state_name} and their potential impact are noted.")

    # Format population if it's a number
    try:
        pop_num = int(population)
        population_str = f"{pop_num:,}" # Add commas
    except (ValueError, TypeError):
        population_str = str(population) # Keep as string if not a number

    # Basic templating using string replacement (consider Template class for complex cases)
    content = template_content

    # Replace specific placeholders found in the template JSON
    content = content.replace("[MAIN_HEADER_WITH_STATE]", f"Find Local {state_name} Bail Bondsmen Near You")
    content = content.replace("[SECONDARY_HEADER_WITH_STATE]", f"Find Licensed {state_name} Bail Bond Agents Available Now")
    content = content.replace("[GUIDE_TITLE_WITH_STATE]", f"Your Guide to Finding Local {state_name} Bail Bondsmen")
    content = content.replace("[GUIDE_SUBTITLE]", generate_unique_guide_paragraph(state_name))

    content = content.replace("[INTRO_PARAGRAPH_WITH_STATE]", generate_unique_intro_paragraph(state_name))
    second_intro = f"When you need bail assistance in {state_name}, time is of the essence. Our directory connects you with experienced professionals who understand the local legal system and can expedite the release process."
    content = content.replace("[SECOND_INTRO_PARAGRAPH_WITH_STATE]", second_intro)

    content = content.replace("[AVAILABILITY_PARAGRAPH_WITH_STATE]", generate_unique_availability_section(state_name))
    content = content.replace("[VERIFIED_PARAGRAPH_WITH_STATE]", generate_unique_verified_bondsman_section(state_name))
    content = content.replace("[NATIONWIDE_PARAGRAPH_WITH_STATE]", generate_unique_nationwide_coverage_section(state_name))

    content = content.replace("[STATE_NAME]", state_name)
    content = content.replace("[STATE_NICKNAME_HEADING]", f"{state_name}: The {nickname}")

    state_intro = f"{state_name}, known as the {nickname}, has a population of approximately {population_str} residents across {num_counties} counties. The state's bail system operates under specific regulations that local bondsmen understand thoroughly."
    content = content.replace("[STATE_INTRO_PARAGRAPH_WITH_NICKNAME]", state_intro)

    # Format major cities list
    if major_cities and len(major_cities) >= 2:
        cities_str = f"{major_cities[0]} and {major_cities[1]}"
        if len(major_cities) > 2:
             cities_str = f"{', '.join(major_cities[:2])}, and others" # Adjust as needed
    elif major_cities and len(major_cities) == 1:
        cities_str = major_cities[0]
    else:
        cities_str = "major metropolitan areas"

    metro_paragraph = f"The largest metropolitan areas in {state_name} include {cities_str}, which account for a significant portion of bail bond services. However, our network extends to all counties throughout the state."
    content = content.replace("[STATE_METRO_PARAGRAPH_WITH_CITIES]", metro_paragraph)

    content = content.replace("[STATE_ECONOMY_PARAGRAPH]", economy)
    content = content.replace("[STATE_BAIL_SYSTEM_PARAGRAPH]", bail_system)
    content = content.replace("[STATE_CRIMINAL_JUSTICE_PARAGRAPH]", criminal_justice)
    content = content.replace("[STATE_GEOGRAPHY_PARAGRAPH_WITH_INTERSTATES]", geography) # Placeholder name might need adjustment
    content = content.replace("[STATE_WEATHER_PARAGRAPH]", weather)

    conclusion = f"For families seeking to secure a loved one's release from any of {state_name}'s detention facilities, working with a {state_name}-based bail bondsman who understands the state's unique characteristics provides the most efficient path to reunion and beginning the next steps in the legal process."
    content = content.replace("[STATE_CONCLUSION_PARAGRAPH]", conclusion)

    # --- FAQ Replacement ---
    # Assuming the template has placeholders like [FAQ_1_QUESTION], [FAQ_1_ANSWER], etc.
    faqs = state_data.get("faqs", [])
    for i, faq in enumerate(faqs):
        q_placeholder = f"[FAQ_{i+1}_QUESTION]"
        a_placeholder = f"[FAQ_{i+1}_ANSWER]"
        content = content.replace(q_placeholder, faq.get("question", f"Question {i+1} not available."))
        content = content.replace(a_placeholder, faq.get("answer", f"Answer {i+1} not available."))

     # Replace any remaining FAQ placeholders if fewer than 5 FAQs were provided
    for i in range(len(faqs), 5):
        q_placeholder = f"[FAQ_{i+1}_QUESTION]"
        a_placeholder = f"[FAQ_{i+1}_ANSWER]"
        content = content.replace(q_placeholder, "") # Remove placeholder if no data
        content = content.replace(a_placeholder, "") # Remove placeholder if no data


    return content

# --- Core Logic Functions (from Part 2) ---

def generate_page_for_state(state_name):
    """Generate a complete page JSON and HTML preview for a specific state"""
    # Ensure output directories exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(STATE_DATA_DIR, exist_ok=True)

    # Load template
    template_json = load_template()
    if not template_json:
        print(f"Halting generation for {state_name} due to template loading error.")
        return False

    # Load state data
    state_data = load_state_data(state_name)
    if not state_data:
        print(f"Creating placeholder state data for {state_name} as no file was found.")
        # Create basic placeholder data if none exists
        state_data = {
            "name": state_name,
            "abbreviation": state_name[:2].upper(), # Simple guess
            "nickname": f"{state_name} State", # Placeholder
            "capital": "State Capital",
            "population": "N/A",
            "num_counties": "N/A",
            "largest_counties": [
                {"name": "Largest County", "description": "Description needed"},
                {"name": "Second County", "description": "Description needed"},
                {"name": "Third County", "description": "Description needed"}
            ],
            "major_cities": ["Major City 1", "Major City 2"],
            "economy": f"Economic details for {state_name} to be added.",
            "bail_system": f"Bail system information for {state_name} to be added.",
            "criminal_justice": f"Criminal justice context for {state_name} to be added.",
            "geography": f"Geographical notes for {state_name} to be added.",
            "weather": f"Weather considerations for {state_name} to be added.",
            "faqs": generate_unique_faqs(state_name) # Generate dynamic FAQs
        }
        # Attempt to save this placeholder data
        save_state_data(state_name, state_data)
    elif "faqs" not in state_data or not state_data["faqs"]:
         # If data exists but FAQs are missing, generate them
         print(f"Generating missing FAQs for {state_name}.")
         state_data["faqs"] = generate_unique_faqs(state_name)
         # Save the updated data with FAQs
         save_state_data(state_name, state_data)


    # Get the template content string (assuming Divi structure)
    template_content = ""
    if isinstance(template_json.get("data"), dict):
        data_keys = list(template_json["data"].keys())
        if data_keys:
            # Assuming the main content is under the first key in 'data'
            template_content = template_json["data"][data_keys[0]]
        else:
             print(f"Error: Template JSON for {state_name} has 'data' object but it's empty.")
             return False
    else:
        print(f"Error: Template JSON for {state_name} is missing 'data' object or it's not a dictionary.")
        return False

    if not template_content:
        print(f"Error: Could not extract content string from template for {state_name}")
        return False

    # Replace variables in the template content
    try:
        page_content_processed = replace_template_variables(template_content, state_data)
    except Exception as e:
        print(f"Error during template variable replacement for {state_name}: {e}")
        traceback.print_exc()
        return False

    # Create the final page JSON structure for Divi import
    # Use the structure from the loaded template as a base
    page_json = template_json # Start with the original template structure
    # Update the 'data' part with the processed content
    if isinstance(page_json.get("data"), dict) and list(page_json["data"].keys()):
        first_key = list(page_json["data"].keys())[0]
        page_json["data"][first_key] = page_content_processed
    else:
        # Fallback if structure was unexpected, create a basic one
        page_json = {
            "context": "et_builder",
            "data": {
                "placeholder_key": page_content_processed # Use a placeholder key
            },
             # Carry over other potential template elements
            "presets": template_json.get("presets", {}),
            "global_colors": template_json.get("global_colors", []),
            "images": template_json.get("images", {}),
            "thumbnails": template_json.get("thumbnails", [])
        }
        print(f"Warning: Used fallback JSON structure for {state_name} due to unexpected template format.")


    # --- Save Generated Files ---
    state_file_base = state_name.lower().replace(' ', '_')
    output_file_json = os.path.join(OUTPUT_DIR, f"{state_file_base}.json")
    output_file_html = os.path.join(OUTPUT_DIR, f"{state_file_base}.html")

    # Save the generated JSON page
    try:
        with open(output_file_json, 'w') as f:
            json.dump(page_json, f, indent=2)
        print(f"Generated Divi JSON page saved to {output_file_json}")
    except Exception as e:
        print(f"Error saving generated JSON page for {state_name}: {e}")
        traceback.print_exc()
        # Don't necessarily return False, maybe HTML can still be saved
        # return False # Uncomment if JSON save failure should stop the process

    # Save an HTML preview (basic rendering of the processed content)
    try:
        # Basic HTML structure for previewing the content string
        # Note: This will NOT render Divi shortcodes correctly, it's just for text preview.
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
        {page_content_processed}
    </div>
    <hr>
    <h2>Generated FAQs:</h2>
    <ul>
"""
        faqs = state_data.get("faqs", [])
        for faq in faqs:
            html_content += f"<li><strong>{faq.get('question', 'N/A')}</strong><br>{faq.get('answer', 'N/A')}</li>"

        html_content += """
    </ul>
</body>
</html>"""
        with open(output_file_html, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"Basic HTML content preview saved to {output_file_html}")
    except Exception as e:
        print(f"Error saving HTML preview for {state_name}: {e}")
        traceback.print_exc()
        # Decide if this failure is critical
        # return False

    return True # Return True if JSON saved successfully, even if HTML failed


def upload_to_wordpress(state_name):
    """Upload the generated state page JSON to WordPress as a draft page"""
    json_path = os.path.join(OUTPUT_DIR, f"{state_name.lower().replace(' ', '_')}.json")

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


# --- Main Execution Logic (from Part 3) ---

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
    success_generate = generate_page_for_state(state_name)

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

    # List of all 50 states (standard names)
    states = [
        "Alabama", "Alaska", "Arizona", "Arkansas", "California",
        "Colorado", "Connecticut", "Delaware", "Florida", "Georgia",
        "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas",
        "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts",
        "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana",
        "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico",
        "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma",
        "Oregon", "Pennsylvania", "Rhode Island", "South Carolina",
        "South Dakota", "Tennessee", "Texas", "Utah", "Vermont",
        "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"
    ]

    generation_success_count = 0
    upload_success_count = 0
    generation_failures = []
    upload_failures = []

    total_states = len(states)
    for i, state in enumerate(states):
        print(f"\n--- Processing State {i+1}/{total_states}: {state} ---")
        generated = generate_page_for_state(state)

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
