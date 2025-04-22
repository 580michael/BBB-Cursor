#!/usr/bin/env python3
"""
Cline State Page Generator for Bail Bonds Buddy (Part 2)

This script continues the implementation from cline_state.py.
It contains the remaining functions for state page generation and WordPress upload.

This file works together with cline_state.py to provide a complete solution.
"""

import os
import json
import re
import argparse
import random
import requests
import sys
import traceback
from string import Template

# Constants
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_FILE = os.path.join(BASE_DIR, "templates", "State-Template-Page-Only-Variables.json")
OUTPUT_DIR = os.path.join(BASE_DIR, "generated_pages")
STATE_DATA_DIR = os.path.join(BASE_DIR, "state_data")

# WordPress API details
WP_BASE_URL = "https://bailbondsbuddy.com"
WP_API_URL = f"{WP_BASE_URL}/wp-json/wp/v2"
WP_AUTH = ("bbbuddy", "DpSm eiz8 yHjx Sqqk G3lG fqU6")

# FAQ generation functions (continued from cline_state.py)
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
    
    # Select random questions and answers
    faq1 = {
        "question": random.choice(faq1_questions),
        "answer": random.choice(faq1_answers)
    }
    
    faq2 = {
        "question": random.choice(faq2_questions),
        "answer": random.choice(faq2_answers)
    }
    
    faq3 = {
        "question": random.choice(faq3_questions),
        "answer": random.choice(faq3_answers)
    }
    
    faq4 = {
        "question": random.choice(faq4_questions),
        "answer": random.choice(faq4_answers)
    }
    
    faq5 = {
        "question": random.choice(faq5_questions),
        "answer": random.choice(faq5_answers)
    }
    
    return [faq1, faq2, faq3, faq4, faq5]

# Template processing functions
def load_template():
    """Load the template file"""
    try:
        with open(TEMPLATE_FILE, 'r') as f:
            template_json = json.load(f)
        print(f"Template loaded successfully from {TEMPLATE_FILE}")
        return template_json
    except Exception as e:
        print(f"Error loading template: {e}")
        return None

def load_state_data(state_name):
    """Load data for a specific state"""
    filename = os.path.join(STATE_DATA_DIR, f"{state_name.lower().replace(' ', '_')}.json")
    try:
        with open(filename, 'r') as f:
            state_data = json.load(f)
        return state_data
    except FileNotFoundError:
        print(f"Error: Data file for {state_name} not found at {filename}")
        return None

def save_state_data(state_name, state_data):
    """Save state data to a JSON file"""
    filename = os.path.join(STATE_DATA_DIR, f"{state_name.lower().replace(' ', '_')}.json")
    try:
        with open(filename, 'w') as f:
            json.dump(state_data, f, indent=2)
        print(f"State data for {state_name} saved to {filename}")
        return True
    except Exception as e:
        print(f"Error saving state data: {e}")
        return False

def replace_template_variables(template_content, state_data):
    """Replace template variables with state-specific content"""
    state_name = state_data["name"]
    
    # Replace main header
    content = template_content.replace("%91MAIN_HEADER_WITH_STATE%93", f"Find Local {state_name} Bail Bondsmen Near You")
    
    # Replace secondary header
    content = content.replace("%91SECONDARY_HEADER_WITH_STATE%93", f"Find Licensed {state_name} Bail Bond Agents Available Now")
    
    # Replace guide title
    content = content.replace("%91GUIDE_TITLE_WITH_STATE%93", f"Your Guide to Finding Local {state_name} Bail Bondsmen")
    
    # Replace guide subtitle
    content = content.replace("%91GUIDE_SUBTITLE%93", generate_unique_guide_paragraph(state_name))
    
    # Replace intro paragraphs
    intro_paragraph = generate_unique_intro_paragraph(state_name)
    content = content.replace("[INTRO_PARAGRAPH_WITH_STATE]", intro_paragraph)
    
    second_intro = f"When you need bail assistance in {state_name}, time is of the essence. Our directory connects you with experienced professionals who understand the local legal system and can expedite the release process."
    content = content.replace("[SECOND_INTRO_PARAGRAPH_WITH_STATE]", second_intro)
    
    # Replace feature sections
    content = content.replace("[AVAILABILITY_PARAGRAPH_WITH_STATE]", generate_unique_availability_section(state_name))
    content = content.replace("[VERIFIED_PARAGRAPH_WITH_STATE]", generate_unique_verified_bondsman_section(state_name))
    content = content.replace("[NATIONWIDE_PARAGRAPH_WITH_STATE]", generate_unique_nationwide_coverage_section(state_name))
    
    # Replace state information
    content = content.replace("[STATE_NAME]", state_name)
    content = content.replace("[STATE_NICKNAME_HEADING]", f"{state_name}: The {state_data['nickname']}")
    
    # Replace state intro paragraph
    state_intro = f"{state_name}, known as the {state_data['nickname']}, has a population of approximately {state_data['population']} residents across {state_data['num_counties']} counties. The state's bail system operates under specific regulations that local bondsmen understand thoroughly."
    content = content.replace("[STATE_INTRO_PARAGRAPH_WITH_NICKNAME]", state_intro)
    
    # Replace metro paragraph
    metro_paragraph = f"The largest metropolitan areas in {state_name} include {', '.join(state_data['major_cities'][:2])}, which account for a significant portion of bail bond services. However, our network extends to all counties throughout the state."
    content = content.replace("[STATE_METRO_PARAGRAPH_WITH_CITIES]", metro_paragraph)
    
    # Replace economy paragraph
    content = content.replace("[STATE_ECONOMY_PARAGRAPH]", state_data["economy"])
    
    # Replace bail system paragraph
    content = content.replace("[STATE_BAIL_SYSTEM_PARAGRAPH]", state_data["bail_system"])
    
    # Replace criminal justice paragraph
    content = content.replace("[STATE_CRIMINAL_JUSTICE_PARAGRAPH]", state_data["criminal_justice"])
    
    # Replace geography paragraph
    content = content.replace("[STATE_GEOGRAPHY_PARAGRAPH_WITH_INTERSTATES]", state_data["geography"])
    
    # Replace weather paragraph
    content = content.replace("[STATE_WEATHER_PARAGRAPH]", state_data["weather"])
    
    # Replace conclusion paragraph
    conclusion = f"For families seeking to secure a loved one's release from any of {state_name}'s detention facilities, working with a {state_name}-based bail bondsman who understands the state's unique characteristics provides the most efficient path to reunion and beginning the next steps in the legal process."
    content = content.replace("[STATE_CONCLUSION_PARAGRAPH]", conclusion)
    
    return content

def generate_page_for_state(state_name):
    """Generate a complete page for a specific state"""
    # Load template
    template_json = load_template()
    if not template_json:
        return False
    
    # Load or create state data
    state_data = load_state_data(state_name)
    if not state_data:
        print(f"Creating new state data for {state_name}")
        # In a real implementation, you would gather this data from reliable sources
        # For this example, we'll use a placeholder
        state_data = {
            "name": state_name,
            "abbreviation": state_name[:2].upper(),
            "nickname": "Sunshine State",  # This would be specific to each state
            "capital": "Capital City",
            "population": "5 million",
            "num_counties": "67",
            "largest_counties": [
                {"name": "County One", "description": "Largest county"},
                {"name": "County Two", "description": "Second largest county"},
                {"name": "County Three", "description": "Third largest county"}
            ],
            "major_cities": ["City One", "City Two", "City Three"],
            "economy": "The state has a diverse economy based on agriculture, manufacturing, and services.",
            "bail_system": "The state maintains a robust bail system governed by state regulations.",
            "criminal_justice": "Recent criminal justice reform initiatives have aimed to improve the system.",
            "geography": "The state's geography includes mountains, plains, and coastal areas.",
            "weather": "Weather conditions vary throughout the year and can impact court schedules.",
            "faqs": generate_unique_faqs(state_name)
        }
        save_state_data(state_name, state_data)
    
    # Get the template content
    template_content = ""
    if "data" in template_json:
        data_keys = list(template_json["data"].keys())
        if data_keys:
            template_content = template_json["data"][data_keys[0]]
    
    if not template_content:
        print("Error: Could not extract content from template")
        return False
    
    # Replace variables in the template
    page_content = replace_template_variables(template_content, state_data)
    
    # Create the final page JSON
    page_json = {
        "context": "et_builder",
        "data": {
            "1120": page_content
        },
        "presets": {},
        "global_colors": template_json.get("global_colors", []),
        "images": template_json.get("images", {}),
        "thumbnails": template_json.get("thumbnails", [])
    }
    
    # Save the generated page
    output_file = os.path.join(OUTPUT_DIR, f"{state_name.lower().replace(' ', '_')}.json")
    try:
        with open(output_file, 'w') as f:
            json.dump(page_json, f, indent=2)
        print(f"Generated page saved to {output_file}")
        
        # Also save as HTML for preview
        html_file = os.path.join(OUTPUT_DIR, f"{state_name.lower().replace(' ', '_')}.html")
        with open(html_file, 'w') as f:
            html = f"""<!DOCTYPE html>
<html>
<head>
    <title>{state_name} Bail Bondsman</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; margin: 0; padding: 20px; }}
        h1, h2, h3 {{ color: #0066cc; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{state_name} Bail Bondsman</h1>
        {page_content}
    </div>
</body>
</html>"""
            f.write(html)
        print(f"HTML preview saved to {html_file}")
        
        return True
    except Exception as e:
        print(f"Error saving generated page: {e}")
        traceback.print_exc()
        return False

def upload_to_wordpress(state_name):
    """Upload the generated state page to WordPress as a draft"""
    json_path = os.path.join(OUTPUT_DIR, f"{state_name.lower().replace(' ', '_')}.json")
    try:
        with open(json_path, 'r') as f:
            state_json = json.load(f)
    except Exception as e:
        print(f"Error loading {json_path}: {e}")
        return False

    # Extract content from the WordPress/Divi JSON structure
    if not isinstance(state_json, dict) or "data" not in state_json:
        print(f"Error: Invalid JSON structure, missing 'data' key")
        return False
    
    data_keys = state_json["data"].keys()
    if not data_keys:
        print(f"Error: No keys found in 'data'")
        return False
    
    first_key = list(data_keys)[0]
    content = state_json["data"][first_key]
    
    # Configure page data
    title = f"Find Local {state_name} Bail Bondsmen Near You | 24/7 Emergency Service"
    slug = f"{state_name.lower().replace(' ', '-')}-bail-bondsman-24-hour-emergency-service-nearby"

    page_data = {
        "title": title,
        "slug": slug,
        "content": content,
        "status": "draft",
        "meta": {
            "_et_pb_page_layout": "et_no_sidebar",
            "_et_pb_side_nav": "off",
            "_et_pb_use_builder": "on",
            "_wp_page_template": "page-template-blank.php"
        }
    }

    try:
        response = requests.post(
            f"{WP_API_URL}/pages",
            json=page_data,
            auth=WP_AUTH
        )
        if response.status_code >= 200 and response.status_code < 300:
            page_id = response.json().get("id")
            page_link = response.json().get("link")
            print(f"Success! {state_name} page created on WordPress.")
            print(f"Page ID: {page_id}")
            print(f"Draft URL: {WP_BASE_URL}/?page_id={page_id}")
            print(f"Final URL (when published): {page_link}")
            return True
        else:
            print(f"Error creating page: {response.status_code}")
            print(response.text)
            return False
    except Exception as e:
        print(f"Exception while creating page: {e}")
        traceback.print_exc()
        return False

def main():
    """Main function to handle command line arguments"""
    parser = argparse.ArgumentParser(description="Generate state pages for Bail Bonds Buddy")
    parser.add_argument('--state', type=str, help='Generate a page for a specific state')
    parser.add_argument('--upload', action='store_true', help='Upload the generated page to WordPress')
    parser.add_argument('--all', action='store_true', help='Generate pages for all states')
    args = parser.parse_args()

    if args.state:
        print(f"Generating page for {args.state}...")
        success = generate_page_for_state(args.state)
        if success and args.upload:
            print(f"Uploading {args.state} page to WordPress...")
            upload_to_wordpress(args.state)
    elif args.all:
        # List of all 50 states
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
        
        success_count = 0
        for state in states:
            print(f"Generating page for {state}...")
            if generate_page_for_state(state):
                success_count += 1
        
        print(f"Successfully generated {success_count} out of 50 state pages.")
    else:
        print("No action specified. Use --state [StateName], --upload, or --all.")

if __name__ == "__main__":
    main()
