#!/usr/bin/env python3
"""
Improved Texas Page Generator for BailBondsBuddy.com

This script addresses all issues with the previous version by ensuring
all Oklahoma references are replaced and proper unique content is generated
for Texas throughout the entire page.
"""

import os
import json
import sys
import re
import random
import requests
from datetime import datetime

# Constants for local system
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_FILE = os.path.join(BASE_DIR, "Oklahoma Bail Bondsman Emergency 24_7 Service.json")
OUTPUT_DIR = os.path.join(BASE_DIR, "generated_pages")
OUTPUT_JSON = os.path.join(OUTPUT_DIR, "texas_unique_v2.json")
OUTPUT_HTML = os.path.join(OUTPUT_DIR, "texas_unique_v2.html")

# WordPress API configuration
WP_BASE_URL = "https://bailbondsbuddy.com"
WP_API_URL = f"{WP_BASE_URL}/wp-json/wp/v2"
WP_AUTH = ("bbbuddy", "DpSm eiz8 yHjx Sqqk G3lG fqU6")

# Texas specific data
TEXAS_DATA = {
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
    "criminal_justice": "Recent criminal justice reform initiatives in Texas have aimed to improve the state's bail system, focusing on risk assessment rather than financial ability. These reforms have modified certain bail procedures, especially for non-violent offenses.",
    "geography": "Texas's vast size, international border with Mexico, and Gulf Coast create unique jurisdictional challenges for bail bondsmen. The state's diverse geography, from urban centers to rural communities spanning hundreds of miles, requires bondsmen to navigate varying county procedures.",
    "weather": "Weather emergencies, from hurricanes and tropical storms to tornadoes and flooding, can occasionally impact court schedules and bail processing timelines."
}

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

def replace_state_references(content, old_state, new_state):
    """Replace all references to the old state with the new state"""
    if not isinstance(content, str):
        return content
    
    # Replace state name with proper capitalization
    content = re.sub(r'\b' + re.escape(old_state) + r'\b', new_state, content, flags=re.IGNORECASE)
    
    # Replace state abbreviation
    old_abbr = "OK"
    new_abbr = TEXAS_DATA["abbreviation"]
    content = re.sub(r'\b' + re.escape(old_abbr) + r'\b', new_abbr, content)
    
    return content

def replace_nickname_references(content, old_nickname, new_nickname):
    """Replace state nickname references"""
    if not isinstance(content, str):
        return content
    
    content = re.sub(r'\b' + re.escape(old_nickname) + r'\b', new_nickname, content, flags=re.IGNORECASE)
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

def create_unique_intro(state_name):
    """Generate unique intro paragraph"""
    intro_templates = [
        f"We understand that finding a reliable bail bondsman in {state_name} can be stressful, especially in urgent situations. BailBondsBuddy.com simplifies the process by connecting you with trusted bail bond professionals in your local area who understand {state_name}'s specific laws and court requirements. Our network of licensed agents provides immediate assistance when you need it most, helping your loved ones return home quickly and safely.",
        f"When you're searching for a dependable bail bondsman in {state_name}, the process can feel overwhelming. BailBondsBuddy.com makes it easier by providing connections to verified bail bond professionals who are familiar with {state_name}'s legal system and local court procedures. Our network of experienced agents is ready to provide prompt assistance, helping to reunite families during difficult times.",
        f"Finding a trustworthy bail bondsman in {state_name} during a crisis can be challenging. BailBondsBuddy.com offers a streamlined solution by connecting you with pre-screened bail bond professionals who specialize in {state_name}'s bail regulations and courthouse protocols. Our extensive network of licensed agents stands ready to provide the immediate help needed to secure a fast release."
    ]
    
    return random.choice(intro_templates)

def create_unique_availability_section(state_name):
    """Create unique 24/7 Availability section"""
    availability_templates = [
        f"Emergency bail bond services available any time, day or night, when you need help the most in {state_name}. Our bail agents answer calls around the clock and can immediately begin the release process, even on weekends and holidays. {state_name}'s jail system operates 24/7, and so do we - don't wait until morning to get help.",
        f"24/7 bail bond services throughout {state_name}, ensuring help is always available when you need it most. Our network of agents works around the clock to secure releases from any {state_name} detention facility. We understand that arrests don't just happen during business hours, which is why our bondsmen are available nights, weekends, and holidays.",
        f"Immediate bail bond assistance available 24 hours a day, 7 days a week across {state_name}. Our dedicated agents respond to calls any time of day or night and can begin the release process immediately. When every hour counts, our {state_name} bondsmen are ready to help get your loved ones out of jail as quickly as possible."
    ]
    
    return random.choice(availability_templates)

def create_unique_verified_section(state_name):
    """Create unique Verified Bondsman section"""
    verified_templates = [
        f"Emergency bail bond services available from pre-screened, licensed professionals who meet our strict standards in {state_name}. Each verified bondsman in our network is fully licensed through the {state_name} Department of Insurance, insured, and has a proven track record of reliable service and ethical business practices throughout the state.",
        f"Connect with thoroughly vetted bail bondsmen throughout {state_name} who maintain all required state licenses and insurance. Our verification process ensures you're working with trusted professionals who follow {state_name}'s regulations and industry best practices. Every bondsman in our network maintains a strong reputation for ethical service and client satisfaction.",
        f"All {state_name} bail bondsmen in our directory are carefully screened to verify their licensing, insurance coverage, and business practices. We only include professionals who demonstrate a commitment to ethical service and comply with all {state_name} state regulations. This careful selection process ensures you receive reliable assistance during a difficult time."
    ]
    
    return random.choice(verified_templates)

def create_unique_nationwide_section(state_name):
    """Create unique Nationwide Coverage section"""
    nationwide_templates = [
        f"From small towns to major cities, find bail bondsmen across all of {state_name}'s {TEXAS_DATA['num_counties']} counties. Our extensive network ensures coverage throughout the state, from the largest county detention centers to the smallest municipal jails, giving you immediate access to local expertise wherever you need it in {state_name}.",
        f"Our bail bondsman network spans the entirety of {state_name}, covering all {TEXAS_DATA['num_counties']} counties from the largest metropolitan areas to the smallest rural communities. Whether you need assistance in {TEXAS_DATA['major_cities'][0]}, {TEXAS_DATA['major_cities'][1]}, or a small town, we can connect you with local bail bond professionals who understand the specific procedures of your county.",
        f"Comprehensive bail bond coverage throughout {state_name}, including all major cities and rural areas across the state's {TEXAS_DATA['num_counties']} counties. No matter where in {state_name} you need assistance, our network provides immediate access to local bondsmen who understand the specific requirements of your county jail and court system."
    ]
    
    return random.choice(nationwide_templates)

def create_unique_counties_section(state_data):
    """Create unique counties introduction section"""
    state_name = state_data["name"]
    counties = state_data["largest_counties"]
    major_cities = state_data["major_cities"]
    
    counties_templates = [
        f"When you or a loved one is arrested in {state_name}, time is of the essence. The {state_name} jail system can be overwhelming and confusing, especially during such a stressful time. That's why connecting with a local bail bondsman immediately is crucial - they understand the specific procedures of your county jail, have established relationships with local law enforcement, and can navigate the release process efficiently in {counties[0]}, {counties[1]}, or anywhere in {state_name}. A local bondsman from your community knows exactly how to expedite paperwork through the {state_name} court system, potentially reducing jail time from days to just hours.",
        
        f"Navigating the {state_name} criminal justice system after an arrest can be complicated and time-sensitive. Local bail bondsmen are familiar with the specific protocols of {state_name}'s various county detention facilities, including the busiest jails in {counties[0]} and {counties[1]}. Their established connections with {state_name} law enforcement and court officials often allow them to process paperwork more efficiently, helping to secure a faster release so your loved one can return home quickly.",
        
        f"The bail process varies across {state_name}'s {TEXAS_DATA['num_counties']} counties, making local expertise invaluable during the stressful time following an arrest. Whether you're dealing with {counties[0]}, {counties[1]}, or any local jail facility, a {state_name} bail bondsman understands the specific procedures and paperwork required. Their familiarity with local courts and detention facilities helps streamline the release process, potentially reducing waiting time significantly."
    ]
    
    return random.choice(counties_templates)

def create_unique_service_section(state_data):
    """Create unique service description section"""
    state_name = state_data["name"]
    
    service_templates = [
        f"BailBondsBuddy.com gives you instant access to trusted bondsmen throughout {state_name}, from bustling cities to small towns. Our network of licensed professionals offers 24/7 service, affordable payment plans, and complete confidentiality. They can explain {state_name}'s specific bail laws and requirements in plain language, help with paperwork, and even provide transportation from jail when needed. Don't waste precious time behind bars - use our simple search tool to find a local bondsman in your area who can get you or your loved one home quickly, allowing you to prepare for your case while maintaining your job and family responsibilities.",
        
        f"Access our comprehensive network of reliable bail bondsmen serving all areas of {state_name} through BailBondsBuddy.com. These professionals provide around-the-clock assistance, flexible payment options, and confidential service tailored to {state_name}'s legal requirements. They'll guide you through {state_name}'s bail process step by step, assist with all necessary documentation, and may offer transportation services from detention facilities. Our easy-to-use search tool helps you quickly connect with a bondsman in your specific {state_name} location.",
        
        f"BailBondsBuddy.com connects you with experienced bail bond professionals throughout {state_name} who provide immediate assistance when you need it most. These licensed agents understand {state_name}'s unique bail procedures and can explain your options clearly. Many offer flexible payment arrangements, maintain strict confidentiality, and provide additional services like jail pickup. Finding the right bondsman in your {state_name} community is simple with our user-friendly search tool, helping you secure a fast release so life can return to normal as quickly as possible."
    ]
    
    return random.choice(service_templates)

def create_unique_faq(state_name):
    """Generate unique FAQ content for Texas"""
    faqs = [
        {
            "question": f"How long does it take to get released using a bail bond in {state_name}?",
            "answer": f"After a bail bond is posted in {state_name}, release times typically range from 4-12 hours depending on the facility's processing speed and how busy they are. In larger counties like Harris or Dallas, processing can take longer than in smaller counties. Weekend and holiday arrests may take additional time to process. The bondsman will keep you updated on the progress throughout the release process."
        },
        {
            "question": f"What kind of collateral is accepted for bail bonds in {state_name}?",
            "answer": f"Bail bondsmen in {state_name} typically accept various forms of collateral including real estate, vehicles, jewelry, electronics, and other valuable assets. {state_name} has specific regulations regarding property bonds, particularly for real estate collateral. Some bondsmen may also accept co-signers with good credit as an alternative to physical collateral. The specific requirements vary by bondsman and the amount of the bail."
        },
        {
            "question": f"What is the typical cost of a bail bond in {state_name}?",
            "answer": f"In {state_name}, bail bond fees typically range from 8-10% of the total bail amount, though this can vary by county and bondsman. For example, if bail is set at $10,000, you would pay $800-1,000 to the bondsman. This fee is non-refundable as it represents the bondsman's service fee for posting the full bail amount. Some {state_name} bondsmen offer payment plans for those who cannot pay the full premium upfront."
        },
        {
            "question": f"What happens if someone fails to appear in court after posting bail in {state_name}?",
            "answer": f"If a defendant fails to appear in court after posting bail in {state_name}, the court issues a bench warrant for their immediate arrest and the bail bond is forfeited. {state_name} law gives bondsmen a specific time period (typically 120-180 days) to locate and surrender the defendant before paying the full bond amount. Recovery agents may be employed to find the defendant, and the person who signed for the bond may lose any collateral provided and become responsible for the full bail amount plus recovery costs."
        },
        {
            "question": f"How can I find a reputable bail bondsman in {state_name}?",
            "answer": f"To find a reputable bail bondsman in {state_name}, start by verifying their license through the {state_name} Department of Insurance or your county's bail bond board. Look for bondsmen with positive reviews, several years of experience, and 24/7 availability. Ask about their fee structure, payment options, and any additional requirements upfront. BailBondsBuddy.com provides access to pre-screened, licensed bail bond professionals throughout {state_name} who meet our strict standards for reliability and ethical business practices."
        }
    ]
    
    return faqs

def create_unique_state_description(state_data):
    """Create a unique state description section"""
    state_name = state_data["name"]
    nickname = state_data["nickname"]
    population = state_data["population"]
    num_counties = state_data["num_counties"]
    largest_counties = state_data["largest_counties"]
    major_cities = state_data["major_cities"]
    
    # Create paragraphs from state data
    paragraphs = [
        f"{state_name}, known as the {nickname}, combines rich heritage, pioneering spirit, and modern economic growth across its diverse landscape. With a population of approximately {population} residents spread throughout {num_counties} counties, {state_name} presents unique challenges and opportunities within its criminal justice system.",
        
        f"The state's largest metropolitan areas – {major_cities[0]} and {major_cities[1]} – account for the highest concentration of arrests and bail needs, but {state_name}'s extensive rural communities also require specialized bail bond services. {state_name}'s county jail system operates under state supervision while maintaining individual county administration, creating a patchwork of procedures that experienced bail bondsmen must navigate daily.",
        
        f"{state_data['economic_info']} This economic evolution has affected crime patterns and bail requirements throughout the state, with growing urban centers experiencing different needs than rural communities.",
        
        f"{state_data['bail_system']} {state_name} law establishes standard premium rates (typically 10% of the bail amount) and regulates bondsman practices to protect consumers during vulnerable times.",
        
        f"{state_data['criminal_justice']} making professional guidance from experienced bondsmen even more valuable for navigating the changing legal landscape.",
        
        f"{state_data['geography']} requires bondsmen to navigate varying county procedures and sometimes coordinate across long distances.",
        
        f"{state_data['weather']} Local bondsmen familiar with {state_name}'s systems know how to manage these disruptions while ensuring clients meet all legal obligations.",
        
        f"For families seeking to secure a loved one's release from any of {state_name}'s detention facilities, working with a {state_name}-based bail bondsman who understands the state's unique characteristics provides the most efficient path to reunion and beginning the next steps in the legal process."
    ]
    
    return "\n\n".join(paragraphs)

def update_map_coordinates(content, lat, lng, state_name):
    """Update the map coordinates in the content"""
    if not isinstance(content, str):
        return content
    
    # Replace map address, lat and lng
    content = re.sub(r'address="Oklahoma City, OK, USA"', f'address="{state_name}, USA"', content)
    content = re.sub(r'address_lat="[^"]+"', f'address_lat="{lat}"', content)
    content = re.sub(r'address_lng="[^"]+"', f'address_lng="{lng}"', content)
    
    return content

def replace_headers_and_titles(content, old_state, new_state):
    """Replace state names in headers, titles and specific elements"""
    if not isinstance(content, str):
        return content
    
    # Replace in h1, h2, h3 tags
    content = re.sub(
        r'<h1[^>]*>([^<]*?)' + re.escape(old_state) + r'([^<]*?)</h1>',
        lambda m: m.group(0).replace(old_state, new_state),
        content,
        flags=re.IGNORECASE
    )
    
    content = re.sub(
        r'<h2[^>]*>([^<]*?)' + re.escape(old_state) + r'([^<]*?)</h2>',
        lambda m: m.group(0).replace(old_state, new_state),
        content,
        flags=re.IGNORECASE
    )
    
    content = re.sub(
        r'<h3[^>]*>([^<]*?)' + re.escape(old_state) + r'([^<]*?)</h3>',
        lambda m: m.group(0).replace(old_state, new_state),
        content,
        flags=re.IGNORECASE
    )
    
    # Replace in specific section titles
    content = re.sub(
        r'Major Counties in ' + re.escape(old_state),
        f'Major Counties in {new_state}',
        content,
        flags=re.IGNORECASE
    )
    
    content = re.sub(
        r'Find Local ' + re.escape(old_state) + r' Bail Bondsmen Near You',
        f'Find Local {new_state} Bail Bondsmen Near You',
        content,
        flags=re.IGNORECASE
    )
    
    content = re.sub(
        r'Your Guide to Finding Local ' + re.escape(old_state) + r' Bail Bondsmen',
        f'Your Guide to Finding Local {new_state} Bail Bondsmen',
        content,
        flags=re.IGNORECASE
    )
    
    content = re.sub(
        r'Find Licensed ' + re.escape(old_state) + r' Bail Bond Agents Available Now',
        f'Find Licensed {new_state} Bail Bond Agents Available Now',
        content,
        flags=re.IGNORECASE
    )
    
    return content

def modify_divi_content(content, state_data):
    """Modify the DIVI content to create a unique page for Texas"""
    old_state = "Oklahoma"
    new_state = state_data["name"]
    old_nickname = "Sooner State"
    new_nickname = state_data["nickname"]
    old_counties = ["Oklahoma County", "Tulsa County", "Cleveland County"]
    new_counties = state_data["largest_counties"]
    old_cities = ["Oklahoma City", "Tulsa", "Norman"]
    new_cities = state_data["major_cities"]
    
    # First, update all basic text references
    content = replace_state_references(content, old_state, new_state)
    content = replace_nickname_references(content, old_nickname, new_nickname)
    content = replace_county_references(content, old_counties, new_counties)
    content = replace_city_references(content, old_cities, new_cities)
    
    # Update headers and titles specifically
    content = replace_headers_and_titles(content, old_state, new_state)
    
    # Update map coordinates and center
    content = update_map_coordinates(content, state_data["lat"], state_data["lng"], new_state)
    
    # Update the main title section
    content = re.sub(
        r'<h1[^>]*>Find Local Oklahoma[^<]*</h1>',
        f'<h1>Find Local {new_state} Bail Bondsmen Near You</h1>',
        content,
        flags=re.IGNORECASE
    )
    
    # Update the subtitle
    content = re.sub(
        r'<h2[^>]*>Find Licensed Oklahoma[^<]*</h2>',
        f'<h2>Find Licensed {new_state} Bail Bond Agents Available Now</h2>',
        content,
        flags=re.IGNORECASE
    )
    
    # Update the guide title
    content = re.sub(
        r'<h2[^>]*>Your Guide to Finding Local Oklahoma[^<]*</h2>',
        f'<h2>Your Guide to Finding Local {new_state} Bail Bondsmen</h2>',
        content,
        flags=re.IGNORECASE
    )
    
    # Replace the main hero text section (more specific pattern)
    unique_intro = create_unique_intro(new_state)
    content = re.sub(
        r'(<div class="et_pb_text_inner">)\s*<p[^>]*>We understand that finding a reliable bail bondsman[^<]+?matters most\.</p>',
        f'\\1<p>{unique_intro}</p>',
        content
    )
    
    # Replace the 24/7 Availability section (more specific pattern)
    unique_availability = create_unique_availability_section(new_state)
    content = re.sub(
        r'(<div class="et_pb_text_inner">\s*<p[^>]*>)Emergency bail bond services available any time[^<]+?help now\.</p>',
        f'\\1{unique_availability}</p>',
        content
    )
    
    # Replace the Verified Bondsman section (more specific pattern)
    unique_verified = create_unique_verified_section(new_state)
    content = re.sub(
        r'(<div class="et_pb_text_inner">\s*<p[^>]*>)Emergency bail bond services available from pre-screened[^<]+?business practices\.</p>',
        f'\\1{unique_verified}</p>',
        content
    )
    
    # Replace the Nationwide Coverage section (more specific pattern)
    unique_nationwide = create_unique_nationwide_section(new_state)
    content = re.sub(
        r'(<div class="et_pb_text_inner">\s*<p[^>]*>)From small towns to major cities[^<]+?you need it\.</p>',
        f'\\1{unique_nationwide}</p>',
        content
    )
    
    # Replace the Counties intro section (more specific pattern)
    unique_counties = create_unique_counties_section(state_data)
    content = re.sub(
        r'(<div class="et_pb_text_inner">\s*<p[^>]*>)When you or a loved one is arrested, time is of the essence[^<]+?just hours\.</p>',
        f'\\1{unique_counties}</p>',
        content
    )
    
    # Remove the Major Counties section entirely since we'll add county pages later
    content = re.sub(
        r'<div class="et_pb_section[^>]*>.*?Major Counties in Oklahoma.*?</div>\s*</div>\s*</div>',
        '',
        content,
        flags=re.DOTALL
    )
    
    # Replace the service section (more specific pattern)
    unique_service = create_unique_service_section(state_data)
    content = re.sub(
        r'(<div class="et_pb_text_inner">\s*<p[^>]*>)BailBondsBuddy\.com gives you instant access to trusted bondsmen throughout[^<]+?responsibilities\.</p>',
        f'\\1{unique_service}</p>',
        content
    )
    
    # Update state description section (more specific pattern)
    unique_description = create_unique_state_description(state_data)
    content = re.sub(
        r'(<div class="et_pb_text_inner">\s*<p[^>]*>)Oklahoma, known as the Sooner State,[^<]+?in the legal process\.</p>',
        f'\\1{unique_description}</p>',
        content
    )
    
    # Update FAQs with more specific patterns
    faqs = create_unique_faq(new_state)
    
    # Replace FAQ questions and answers with more specific patterns
    for i, faq in enumerate(faqs, 1):
        if i == 1:
            content = re.sub(
                r'(<div class="et_pb_toggle_title">)How long does it take to get released[^<]+?(</div>)',
                f'\\1{faq["question"]}\\2',
                content
            )
            content = re.sub(
                r'(<div class="et_pb_toggle_content clearfix">\s*<p>)After a bail bond is posted[^<]+?(</p>\s*</div>)',
                f'\\1{faq["answer"]}\\2',
                content
            )
        elif i == 2:
            content = re.sub(
                r'(<div class="et_pb_toggle_title">)What kind of collateral[^<]+?(</div>)',
                f'\\1{faq["question"]}\\2',
                content
            )
            content = re.sub(
                r'(<div class="et_pb_toggle_content clearfix">\s*<p>)Common forms of collateral[^<]+?(</p>\s*</div>)',
                f'\\1{faq["answer"]}\\2',
                content
            )
        elif i == 3:
            content = re.sub(
                r'(<div class="et_pb_toggle_title">)What is the typical cost[^<]+?(</div>)',
                f'\\1{faq["question"]}\\2',
                content
            )
            content = re.sub(
                r'(<div class="et_pb_toggle_content clearfix">\s*<p>)The standard premium[^<]+?(</p>\s*</div>)',
                f'\\1{faq["answer"]}\\2',
                content
            )
        elif i == 4:
            content = re.sub(
                r'(<div class="et_pb_toggle_title">)What information do I need[^<]+?(</div>)',
                f'\\1{faq["question"]}\\2',
                content
            )
            content = re.sub(
                r'(<div class="et_pb_toggle_content clearfix">\s*<p>)When calling a bail bondsman[^<]+?(</p>\s*</div>)',
                f'\\1{faq["answer"]}\\2',
                content
            )
        elif i == 5:
            content = re.sub(
                r'(<div class="et_pb_toggle_title">)What types of payments[^<]+?(</div>)',
                f'\\1{faq["question"]}\\2',
                content
            )
            content = re.sub(
                r'(<div class="et_pb_toggle_content clearfix">\s*<p>)Most bail bondsmen accept[^<]+?(</p>\s*</div>)',
                f'\\1{faq["answer"]}\\2',
                content
            )
    
    # Update the search placeholder text
    content = re.sub(
        r'placeholder="[^"]*Oklahoma[^"]*"',
        f'placeholder="Search any city in {new_state} to find a local bail bondsman"',
        content
    )
    
    return content

def generate_page():
    """Generate a customized Texas page"""
    # Create output directory if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Load the template
    template_json = load_template()
    if not template_json:
        print("Failed to load template")
        return False
    
    print(f"Generating unique content for {TEXAS_DATA['name']}...")
    
    # Get template content
    template_content = ""
    if "data" in template_json:
        for key, value in template_json["data"].items():
            template_content = value
            break
    
    if not template_content:
        print("Error: Could not extract content from template")
        return False
    
    # Modify content for Texas
    modified_content = modify_divi_content(template_content, TEXAS_DATA)
    
    # Create new JSON structure
    texas_json = template_json.copy()
    
    # Update the content
    for key in texas_json["data"]:
        texas_json["data"][key] = modified_content
        break
    
    # Save the modified JSON
    with open(OUTPUT_JSON, 'w') as f:
        json.dump(texas_json, f, indent=2)
    print(f"Generated JSON saved to {OUTPUT_JSON}")
    
    # Create an HTML preview
    title = f"{TEXAS_DATA['name']} Bail Bondsman 24/7 Emergency Service | BailBondsBuddy.com"
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>{title}</title>
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
        <h1>{title}</h1>
        <p><strong>Note:</strong> This is an HTML preview. The actual page will use Divi builder formatting.</p>
        <hr>
        {modified_content}
        <hr>
        <p>Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
</body>
</html>"""
    
    with open(OUTPUT_HTML, 'w') as f:
        f.write(html)
    print(f"HTML preview saved to {OUTPUT_HTML}")
    
    return True

def upload_to_wordpress():
    """Upload the generated page to WordPress"""
    # Load the generated JSON
    try:
        with open(OUTPUT_JSON, 'r') as f:
            texas_json = json.load(f)
            print(f"Successfully loaded {OUTPUT_JSON}")
    except Exception as e:
        print(f"Error loading {OUTPUT_JSON}: {e}")
        return False
    
    # Extract the content
    divi_content = ""
    if "data" in texas_json:
        for key, value in texas_json["data"].items():
            divi_content = value
            break
    
    if not divi_content:
        print("Error: Could not extract content from JSON file")
        return False
    
    # Prepare page data
    page_data = {
        "title": f"Find Local {TEXAS_DATA['name']} Bail Bondsmen Near You | 24/7 Emergency Service",
        "slug": f"{TEXAS_DATA['name'].lower()}-bail-bondsman-24-hour-emergency-service-nearby",
        "content": divi_content,
        "status": "draft",
        "meta": {
            "_et_pb_page_layout": "et_no_sidebar",  # Full width
            "_et_pb_side_nav": "off",  # No side nav
            "_et_pb_use_builder": "on",  # Enable DIVI
            "_wp_page_template": "page-template-blank.php"  # Blank template
        }
    }
    
    # Create the page on WordPress
    try:
        response = requests.post(
            f"{WP_API_URL}/pages",
            json=page_data,
            auth=WP_AUTH
        )
        
        if response.status_code >= 200 and response.status_code < 300:
            page_id = response.json().get("id")
            page_link = response.json().get("link")
            print(f"Success! {TEXAS_DATA['name']} page created on WordPress.")
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
        return False

def main():
    print("=== Improved Texas Page Generator ===")
    print("Generating a unique Texas page with customized content for ALL sections...")
    
    # Generate the page
    if generate_page():
        print("\nGeneration successful!")
        
        # Ask if user wants to upload to WordPress
        choice = input("\nDo you want to upload this improved page to WordPress? (y/n): ")
        if choice.lower() == 'y':
            if upload_to_wordpress():
                print("\nUpload successful! Check your WordPress admin to review and publish the page.")
            else:
                print("\nUpload failed. You can manually import the JSON file through WordPress.")
        else:
            print("\nPage not uploaded. You can manually import the JSON file or run this script again later.")
    else:
        print("\nGeneration failed. Check the error messages above.")

if __name__ == "__main__":
    main() 