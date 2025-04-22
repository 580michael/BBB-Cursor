#!/usr/bin/env python3
"""
Improved Page Generator for Bail Bonds Buddy State Pages (Part 2 of 3)

This script contains the content replacement and generation functions
for creating WordPress/Divi-compatible pages for all 50 states.

This file works together with improved_page_generator_part1.py and
improved_page_generator_part3.py to generate state pages.
"""

import re
import json
import random
import time
import os
from improved_page_generator_part1 import load_template, load_state_data, save_state_page, replace_state_references, replace_county_references, replace_city_references, replace_nickname_references, replace_population_references
from content_generator_utils_part1 import generate_unique_intro_paragraph, generate_unique_guide_paragraph
from content_generator_utils_part2 import generate_unique_availability_section, generate_unique_verified_bondsman_section, generate_unique_nationwide_coverage_section, generate_unique_county_intro
from content_generator_utils_part3 import generate_unique_faqs

def update_page_title(template_json, state_name):
    """Update the page title with the new state name"""
    if "title" in template_json:
        template_json["title"] = template_json["title"].replace("Oklahoma", state_name)
    return template_json

def update_content_sections(content, state_data):
    """Process the JSON structure and update with state-specific data"""
    print(f"Replacing content references for state: {state_data['name']}")
    
    old_state = "Oklahoma"
    new_state = state_data["name"]
    
    # Debug: Print original content keys
    if "data" in content:
        first_content_key = list(content["data"].keys())[0]
        print(f"Found content key: {first_content_key} in content data")
        
        # Extract HTML content from the post_content field
        if "post_content" in content["data"][first_content_key]:
            html_content = content["data"][first_content_key]["post_content"]
        else:
            # If structure is different, content may be the HTML content itself
            html_content = content["data"][first_content_key]
            if not isinstance(html_content, str):
                print(f"Warning: Content is not a string, content type: {type(html_content)}")
                return content
        
        # Replace map marker with state capital or first major city
        capital = state_data.get("capital", "")
        major_cities = state_data.get("major_cities", "")
        if isinstance(major_cities, list):
            cities = major_cities
        else:
            cities = major_cities.split(", ")
        
        # Use capital for map marker, fallback to first major city if available
        map_marker = f"{capital}, {new_state}, USA" if capital else f"{cities[0]}, {new_state}, USA" if cities else f"{new_state}, USA"
        print(f"Setting map marker to: {map_marker}")
        
        # Replace old map address with the new one
        html_content = re.sub(r'address="[^"]*"', f'address="{map_marker}"', html_content)
        
        # Update county references
        counties = state_data.get("largest_counties", [])
        if counties and len(counties) >= 3:
            # Replace county titles with actual counties from the state data
            county_html = f'<et_pb_heading title="{counties[0]}" _builder_version="4.27.4" _module_preset="default" title_text_align="center" global_colors_info="{{}}"></et_pb_heading>'
            html_content = re.sub(r'<et_pb_heading title="Ohio County"[^>]*>[^<]*</et_pb_heading>', county_html, html_content)
            
            # Second county (already correct for Ohio as Franklin County)
            if "Franklin County" not in html_content and len(counties) >= 2:
                county_html = f'<et_pb_heading title="{counties[1]}" _builder_version="4.27.4" _module_preset="default" title_text_align="center" global_colors_info="{{}}"></et_pb_heading>'
                html_content = re.sub(r'<et_pb_heading title="Franklin County"[^>]*>[^<]*</et_pb_heading>', county_html, html_content)
            
            # Third county (already correct for Ohio as Hamilton County)
            if "Hamilton County" not in html_content and len(counties) >= 3:
                county_html = f'<et_pb_heading title="{counties[2]}" _builder_version="4.27.4" _module_preset="default" title_text_align="center" global_colors_info="{{}}"></et_pb_heading>'
                html_content = re.sub(r'<et_pb_heading title="Hamilton County"[^>]*>[^<]*</et_pb_heading>', county_html, html_content)
        
        # Replace title and state name references
        html_content = html_content.replace(f"{old_state} Bail Bondsman", f"{new_state} Bail Bondsman")
        html_content = html_content.replace(f"{old_state}:", f"{new_state}:")
        
        # Replace nickname - handle "The" properly
        nickname = state_data.get("nickname", "")
        if nickname:
            if nickname.startswith("The "):
                nickname_pattern = "The .*? State"
                replacement = nickname
            else:
                nickname_pattern = "The .*? State"
                replacement = f"The {nickname}"
            
            html_content = re.sub(nickname_pattern, replacement, html_content)
        
        # Handle population
        population = state_data.get("population", "")
        if population:
            html_content = re.sub(r'\d+(\.\d+)? million residents', f"{population} residents", html_content)
        
        # Update number of counties
        county_count = state_data.get("counties", 0)
        if county_count > 0:
            html_content = re.sub(r'\d+ counties', f"{county_count} counties", html_content)
        
        # Replace city references
        if isinstance(cities, list) and len(cities) >= 2:
            largest_city = cities[0]
            second_city = cities[1]
            
            # Replace Oklahoma City with the largest city of the new state
            html_content = html_content.replace("Oklahoma City", largest_city)
            html_content = html_content.replace("Tulsa", second_city)
            
            # Replace the pattern "largest metropolitan areas – Oklahoma City and Tulsa"
            html_content = re.sub(r'largest metropolitan areas – .*? and .*? –', f'largest metropolitan areas – {largest_city} and {second_city} –', html_content)
        
        # Replace references to Oklahoma laws and regulations
        if "bail_system" in state_data:
            # Replace "Oklahoma Bail Bondsmen Act" with state-specific reference
            html_content = re.sub(r'Oklahoma Bail Bondsmen Act', f"{new_state} Bail Bondsmen Act", html_content)
            
            # Update bail system description if provided
            if state_data["bail_system"]:
                bail_system_pattern = r'The state maintains a robust bail system governed by the .*?\..*?vulnerable times\.'
                bail_system_replacement = f"The state maintains a robust bail system governed by the {new_state} Bail Bondsmen Act, which requires all bondsmen to be licensed through the {new_state} Insurance Department. {new_state} law establishes standard premium rates (typically 10% of the bail amount) and regulates bondsman practices to protect consumers during vulnerable times."
                html_content = re.sub(bail_system_pattern, bail_system_replacement, html_content)
        
        # Replace interstate references completely with Ohio's major interstates
        if new_state == "Ohio":
            interstate_pattern = r'geographical positioning along major interstate highways \(I-35, I-40, and I-44\)'
            interstate_replacement = 'geographical positioning along major interstate highways (I-70, I-71, and I-75)'
            html_content = re.sub(interstate_pattern, interstate_replacement, html_content)
        
        # Weather information
        if "weather" in state_data and state_data["weather"]:
            # Fix duplicate text in weather section
            weather_pattern = r'during winter months\., can occasionally impact'
            weather_replacement = 'during winter months can occasionally impact'
            html_content = re.sub(weather_pattern, weather_replacement, html_content)
        
        # Update the content in the dictionary
        if "post_content" in content["data"][first_content_key]:
            content["data"][first_content_key]["post_content"] = html_content
        else:
            content["data"][first_content_key] = html_content
        print(f"Updated content with {new_state} specifics")
    else:
        print("Warning: Expected 'data' key not found in content structure")
    
    return content

def update_state_specific_sections(content, state_data):
    """Update state-specific content sections with unique content"""
    state_name = state_data["name"]
    
    # Find and replace the main heading
    main_heading_pattern = r'(Find Local) Oklahoma (Bail Bondsmen Near You)'
    content = re.sub(main_heading_pattern, f'\\1 {state_name} \\2', content)
    
    # Find and replace the subheading
    subheading_pattern = r'(Find Licensed) Oklahoma (Bail Bond Agents Available Now)'
    content = re.sub(subheading_pattern, f'\\1 {state_name} \\2', content)
    
    # Find and replace the guide heading
    guide_heading_pattern = r'(Your Guide to Finding Local) Oklahoma (Bail Bondsmen)'
    content = re.sub(guide_heading_pattern, f'\\1 {state_name} \\2', content)
    
    # Replace the intro paragraph with unique content
    intro_paragraph_pattern = r'We understand that finding a reliable bail bondsman can be stressful.*?matters most\.'
    new_intro = generate_unique_intro_paragraph(state_name)
    content = re.sub(intro_paragraph_pattern, new_intro, content, flags=re.DOTALL)
    
    # Replace the guide paragraph with unique content
    guide_paragraph_pattern = r'Find trusted bail bondsmen in your area, available 24/7\.'
    new_guide = generate_unique_guide_paragraph(state_name)
    content = re.sub(guide_paragraph_pattern, new_guide, content)
    
    # Replace the 24/7 Availability section with unique content
    availability_pattern = r'Emergency bail bond services available any time.*?get help now\.'
    new_availability = generate_unique_availability_section(state_name)
    content = re.sub(availability_pattern, new_availability, content, flags=re.DOTALL)
    
    # Replace the Verified Bondsman section with unique content
    verified_pattern = r'Emergency bail bond services available from pre-screened.*?business practices\.'
    new_verified = generate_unique_verified_bondsman_section(state_name)
    content = re.sub(verified_pattern, new_verified, content, flags=re.DOTALL)
    
    # Replace the Nationwide Coverage section with unique content
    nationwide_pattern = r'From small towns to major cities, find bail bondsmen across all 50 states.*?wherever you need it\.'
    new_nationwide = generate_unique_nationwide_coverage_section(state_name)
    content = re.sub(nationwide_pattern, new_nationwide, content, flags=re.DOTALL)
    
    # Replace the state description section
    state_desc_pattern = r'Oklahoma: The Sooner State'
    content = re.sub(state_desc_pattern, f'{state_name}: The {state_data["nickname"]}', content)
    
    # Replace the state info paragraph
    state_info_pattern = r'Oklahoma, known as the Sooner State.*?justice system\.'
    new_state_info = f'{state_name}, known as the {state_data["nickname"]}, combines rich Native American heritage, pioneering spirit, and modern economic growth across its diverse landscape. With a population of approximately {state_data["population"]} residents spread throughout {state_data["num_counties"]} counties, {state_name} presents unique challenges and opportunities within its criminal justice system.'
    content = re.sub(state_info_pattern, new_state_info, content, flags=re.DOTALL)
    
    # Replace the metropolitan areas paragraph
    metro_pattern = r'The state\'s largest metropolitan areas.*?navigate daily\.'
    new_metro = f'The state\'s largest metropolitan areas – {state_data["major_cities"][0]} and {state_data["major_cities"][1]} – account for the highest concentration of arrests and bail needs, but {state_name}\'s extensive rural communities also require specialized bail bond services. {state_name}\'s county jail system operates under state supervision while maintaining individual county administration, creating a patchwork of procedures that experienced bail bondsmen must navigate daily.'
    content = re.sub(metro_pattern, new_metro, content, flags=re.DOTALL)
    
    # Replace the economy paragraph
    economy_pattern = r'Oklahoma\'s economy has traditionally centered around energy production.*?communities\.'
    new_economy = f'{state_name}\'s economy has traditionally centered around {state_data["economic_info"]} This economic evolution has affected crime patterns and bail requirements throughout the state, with growing urban centers experiencing different needs than rural communities.'
    content = re.sub(economy_pattern, new_economy, content, flags=re.DOTALL)
    
    # Replace the bail system paragraph
    bail_system_pattern = r'The state maintains a robust bail system governed by the Oklahoma Bail Bondsmen Act.*?vulnerable times\.'
    new_bail_system = f'The state maintains a robust bail system governed by {state_data["bail_system"]} {state_name} law establishes standard premium rates (typically 10% of the bail amount) and regulates bondsman practices to protect consumers during vulnerable times.'
    content = re.sub(bail_system_pattern, new_bail_system, content, flags=re.DOTALL)
    
    # Replace the criminal justice paragraph
    criminal_justice_pattern = r'Recent criminal justice reform initiatives in Oklahoma have aimed.*?landscape\.'
    new_criminal_justice = f'{state_data["criminal_justice"]} making professional guidance from experienced bondsmen even more valuable for navigating the changing legal landscape.'
    content = re.sub(criminal_justice_pattern, new_criminal_justice, content, flags=re.DOTALL)
    
    # Replace the geographical paragraph
    geographical_pattern = r'Oklahoma\'s geographical positioning along major interstate highways.*?understand\.'
    new_geographical = f'{state_data["geography"]} Meanwhile, the state\'s diverse population introduces jurisdictional complexities that knowledgeable bail bondsmen must understand.'
    content = re.sub(geographical_pattern, new_geographical, content, flags=re.DOTALL)
    
    # Replace the weather paragraph
    weather_pattern = r'Weather emergencies, from tornadoes to ice storms.*?obligations\.'
    new_weather = f'{state_data["weather"]} Local bondsmen familiar with {state_name}\'s systems know how to manage these disruptions while ensuring clients meet all legal obligations.'
    content = re.sub(weather_pattern, new_weather, content, flags=re.DOTALL)
    
    # Replace the conclusion paragraph
    conclusion_pattern = r'For families seeking to secure a loved one\'s release from any of Oklahoma\'s detention facilities.*?process\.'
    new_conclusion = f'For families seeking to secure a loved one\'s release from any of {state_name}\'s detention facilities, working with a {state_name}-based bail bondsman who understands the state\'s unique characteristics provides the most efficient path to reunion and beginning the next steps in the legal process.'
    content = re.sub(conclusion_pattern, new_conclusion, content, flags=re.DOTALL)
    
    # Replace the Major Counties section
    counties_pattern = r'Major Counties in Oklahoma'
    content = re.sub(counties_pattern, f'Major Counties in {state_name}', content)
    
    # Replace the county sections
    for i, county in enumerate(state_data["largest_counties"]):
        if i < 3:  # We only have 3 county sections in the template
            county_name = county.split(" County")[0]  # Extract county name without "County"
            county_pattern = r'Oklahoma County|Tulsa County|Cleveland County'
            content = re.sub(county_pattern, county, content, count=1)
            
            # Replace the county intro paragraph
            county_intro_pattern = r'When you or a loved one is arrested, time is of the essence.*?responsibilities\.'
            new_county_intro = generate_unique_county_intro(state_name, county_name)
            content = re.sub(county_intro_pattern, new_county_intro, content, flags=re.DOTALL, count=1)
    
    # Replace the FAQ sections with unique FAQs
    faqs = generate_unique_faqs(state_name)
    
    # Replace FAQ 1
    faq1_pattern = r'How long does it take to get released using a bail bond\?.*?progress\.'
    content = re.sub(faq1_pattern, faqs[0], content, flags=re.DOTALL)
    
    # Replace FAQ 2
    faq2_pattern = r'What kind of collateral is accepted for bail bonds\?'
    content = re.sub(faq2_pattern, faqs[1]["question"], content)
    
    # Replace FAQ 3
    faq3_pattern = r'What is the typical cost of a bail bond\?'
    content = re.sub(faq3_pattern, faqs[2]["question"], content)
    
    # Replace FAQ 4
    faq4_pattern = r'What information do I need when contacting a bail bondsman\?'
    content = re.sub(faq4_pattern, faqs[3]["question"], content)
    
    # Replace FAQ 5
    faq5_pattern = r'What types of payments do bail bondsmen accept\?'
    content = re.sub(faq5_pattern, faqs[4]["question"], content)
    
    return content

def generate_page_for_state(state_name, template_json):
    """Generate a complete page for a specific state"""
    try:
        # Load state data
        state_data = load_state_data(state_name)
        if not state_data:
            print(f"Error: Could not load data for {state_name}")
            return False
        
        print(f"DEBUG: State data loaded for {state_name}")
        print(f"DEBUG: State data: {state_data}")
        
        # Create a deep copy of the template
        state_page = json.loads(json.dumps(template_json))
        
        # Update page title
        state_page, _ = update_title_sections(state_page, state_name)
        print(f"DEBUG: Title updated for {state_name}")
        
        # Update content sections
        state_page = update_content_sections(state_page, state_data)
        print(f"DEBUG: Content sections updated for {state_name}")
        
        # Save the generated page
        save_state_page(state_name, state_page, 'json')
        
        # Also save as HTML for preview
        save_state_page(state_name, state_page, 'html')
        
        return True
    except Exception as e:
        print(f"Error generating page for {state_name}: {e}")
        import traceback
        traceback.print_exc()
        return False

# Function to generate a unique availability paragraph
def generate_unique_availability_paragraph(state_name):
    availability_options = [
        f"Emergency bail bond services available 24/7 in {state_name} when you need help the most. Our {state_name} bail agents answer calls around the clock and can immediately begin the release process, even on weekends and holidays. Don't wait until morning - get help now.",
        f"In {state_name}, our bail bondsmen are available 24 hours a day, 7 days a week. Arrests happen at all hours, so our agents provide round-the-clock assistance to ensure you or your loved one doesn't spend more time in jail than necessary.",
        f"Bail bondsmen in {state_name} understand that arrests don't follow business hours. That's why our network maintains constant availability - day or night, weekday or weekend, our agents are ready to take your call and start the release process immediately.",
        f"When someone you care about is arrested in {state_name}, every minute counts. Our bondsmen provide true 24/7 service with no answering services or callbacks - speak directly to a licensed {state_name} bail agent any time, day or night.",
        f"{state_name} bail agents in our network commit to around-the-clock availability because they understand the urgency of jail release. Call any time - 3AM on a Sunday or noon on a Tuesday - and connect with a bondsman ready to help immediately."
    ]
    return random.choice(availability_options)

# Function to generate a unique verified bondsman paragraph
def generate_unique_verified_bondsman_paragraph(state_name):
    verified_options = [
        f"All {state_name} bail bondsmen in our network are pre-screened, licensed professionals who meet our strict standards. Each verified bondsman is fully licensed by the {state_name} Department of Insurance, insured, and has a proven track record of reliable service and ethical business practices.",
        f"We verify the credentials of every {state_name} bail agent in our directory to ensure they maintain active licensing with proper {state_name} authorities. Our verification process confirms their good standing, financial stability, and commitment to ethical practices.",
        f"Finding a trustworthy bail bondsman during a crisis shouldn't be a gamble. That's why we verify all {state_name} bail agents in our network, checking their licensing status, professional history, and client satisfaction records to ensure you receive quality service.",
        f"The {state_name} bail bond industry is heavily regulated to protect consumers. Our directory includes only verified professionals who maintain proper licensing through the {state_name} Department of Insurance and adhere to all state regulations regarding bail practices.",
        f"Our verification process for {state_name} bail bondsmen includes confirming active licensing, checking disciplinary records, verifying insurance coverage, and reviewing client feedback. Only those meeting our strict standards appear in our directory."
    ]
    return random.choice(verified_options)

# Function to generate a unique nationwide coverage paragraph
def generate_unique_nationwide_coverage_paragraph(state_name):
    nationwide_options = [
        f"While our bail bondsmen are locally based in {state_name}, our network extends nationwide. This allows us to coordinate bail for {state_name} residents arrested in other states, or help loved ones from across the country secure release for someone detained in {state_name}.",
        f"Our {state_name} bail bond agents maintain relationships with trusted bondsmen throughout America. This nationwide network proves invaluable when dealing with out-of-state arrests or when family members live far from where the arrest occurred.",
        f"From the smallest towns to major cities across {state_name} and beyond, our nationwide network ensures you'll find bail help wherever needed. This extensive coverage is particularly valuable for travelers, college students, or anyone away from home when an arrest occurs.",
        f"Whether you need a bail bondsman in rural {state_name} or its busiest cities, our comprehensive coverage ensures help is available. Our network spans from coast to coast, making us an ideal resource for both local needs and complex interstate situations.",
        f"Our {state_name} bail agents are part of a trusted national network, allowing them to assist with complex cases involving multiple jurisdictions. This nationwide reach provides peace of mind that professional help is available regardless of location."
    ]
    return random.choice(nationwide_options)

# Function to generate county intro paragraph
def generate_county_intro_paragraph(state_name, counties):
    # Select the top three counties if available
    top_counties = counties[:3] if len(counties) >= 3 else counties
    counties_text = ", ".join(top_counties)
    
    county_intro_options = [
        f"When you or a loved one is arrested in {state_name}, time is of the essence. The jail system across counties like {counties_text} can be overwhelming and confusing, especially during such a stressful time. That's why connecting with a local bail bondsman immediately is crucial - they understand the specific procedures of your county jail, have established relationships with local law enforcement, and can navigate the release process efficiently. A local bondsman from your {state_name} community knows exactly how to expedite paperwork through the local court system, potentially reducing jail time from days to just hours.",
        f"Navigating the bail process in {state_name} counties like {counties_text} requires local expertise. Each county maintains its own procedures, paperwork requirements, and processing timelines. Local bail bondsmen have invaluable insights into these county-specific systems, allowing them to secure faster releases and provide accurate information about what to expect. Their established relationships with jail staff often help streamline what can otherwise be a confusing and time-consuming process.",
        f"The bail system varies significantly across {state_name}'s counties, including {counties_text}. These differences can impact everything from processing times to payment methods and release procedures. Working with a bail bondsman familiar with your specific county jail gives you a significant advantage - they've navigated these systems hundreds of times and know exactly what to do to secure the quickest possible release for you or your loved one.",
        f"Each {state_name} county - whether it's {counties_text} or any other - has its own unique jail procedures and bail processing systems. Local bail bondsmen bring invaluable knowledge about these county-specific processes, potentially saving hours or even days in release time. Their established connections with court clerks, jail staff, and local law enforcement help navigate bureaucratic hurdles that often delay the release process.",
        f"In {state_name}, counties like {counties_text} each operate their jail systems with different procedures and requirements. While the general bail process is similar statewide, these local variations can significantly impact processing times and requirements. A bail bondsman with specific experience in your county brings invaluable knowledge that can make the difference between a smooth, efficient release and a frustrating, delayed process."
    ]
    return random.choice(county_intro_options)

# Function to generate FAQ questions and answers
def generate_faq_items(state_name):
    # FAQ 1: Release time
    faq1_question = f"How long does it take to get released from jail using a bail bond in {state_name}?"
    faq1_answer = f"After a bail bond is posted in {state_name}, release times typically range from 2-8 hours depending on the facility's processing speed and how busy they are. Weekend and holiday arrests may take longer to process. The bondsman will keep you updated on the progress."
    
    # FAQ 2: Collateral
    faq2_question = f"What kind of collateral is accepted for bail bonds in {state_name}?"
    faq2_answer = f"Common forms of collateral accepted by {state_name} bail bondsmen include real estate, vehicles, jewelry, stocks, and bonds. The value of the collateral should generally exceed the bail amount. For real estate, you'll need to provide property deeds, recent appraisals, and proof that your equity exceeds the bail amount."
    
    # FAQ 3: Cost
    faq3_question = f"What is the typical cost of a bail bond in {state_name}?"
    faq3_answer = f"The standard premium for a bail bond in {state_name} is 10% of the full bail amount, which is non-refundable. For example, if the court sets bail at $10,000, you would pay approximately $1,000 to a bail bondsman. Some {state_name} bondsmen offer payment plans or accept collateral for larger bail amounts."
    
    # FAQ 4: Information needed
    faq4_question = f"What information do I need when contacting a {state_name} bail bondsman?"
    faq4_answer = f"When calling a {state_name} bail bondsman, you should have the defendant's full name, where they're being held (which {state_name} jail or detention facility), their booking number, what charges they're facing, and the bail amount if it's been set. Having this information ready helps the bondsman start the process immediately, saving valuable time."
    
    # FAQ 5: Payment methods
    faq5_question = f"What types of payments do {state_name} bail bondsmen accept?"
    faq5_answer = f"Most {state_name} bail bondsmen accept various payment methods including cash, credit/debit cards, money orders, and sometimes property as collateral. Many offer payment plans for larger bail amounts and now accept digital payment options such as Venmo, PayPal, or Cash App for convenience."
    
    return {
        "faq1_question": faq1_question,
        "faq1_answer": faq1_answer,
        "faq2_question": faq2_question,
        "faq2_answer": faq2_answer,
        "faq3_question": faq3_question,
        "faq3_answer": faq3_answer,
        "faq4_question": faq4_question,
        "faq4_answer": faq4_answer,
        "faq5_question": faq5_question,
        "faq5_answer": faq5_answer
    }

# Function to update the title sections with state information
def update_title_sections(template_json, state_name):
    # Find the data key (either 908 or 1112)
    data_keys = list(template_json["data"].keys())
    content_key = None
    for key in data_keys:
        if key.isdigit():  # Look for numeric keys like "908" or "1112"
            content_key = key
            break
    
    if not content_key:
        raise KeyError("Could not find numeric content key in template data")
    
    content = template_json["data"][content_key]
    
    # Update title tag (for SEO)
    template_json["data"]["title"] = f"Find Bail Bondsmen in {state_name} - 24/7 Bail Bond Services"
    
    # Update meta description (for SEO)
    template_json["data"]["description"] = f"Connect with licensed {state_name} bail bondsmen available 24/7. Immediate assistance for jail release across all {state_name} counties. Low rates and payment plans available."
    
    print(f"Updated title sections with {state_name} information.")
    return template_json, content

# Function to update content sections with state information
def update_content_sections(template_json, state_data):
    state_name = state_data.get("name", "")
    capital = state_data.get("capital", "")
    state_abbr = state_data.get("abbreviation", "")
    state_nickname = state_data.get("nickname", "")
    population = state_data.get("population", "")
    counties = state_data.get("largest_counties", [])
    
    # Handle major_cities as either a string or a list
    major_cities = state_data.get("major_cities", "")
    if isinstance(major_cities, list):
        cities = major_cities
    else:
        cities = major_cities.split(", ")
    
    num_counties = state_data.get("counties", "")
    economy = state_data.get("economy", "")
    criminal_justice = state_data.get("criminal_justice", "")
    geography = state_data.get("geography", "")
    weather = state_data.get("weather", "")
    
    # Get the content from template_json - find the data key (either 908 or 1112)
    data_keys = list(template_json["data"].keys())
    content_key = None
    for key in data_keys:
        if key.isdigit():  # Look for numeric keys like "908" or "1112"
            content_key = key
            break
    
    if not content_key:
        raise KeyError("Could not find numeric content key in template data")
    
    content = template_json["data"][content_key]
    
    # Generate dynamic content
    intro_paragraph = generate_unique_intro_paragraph(state_name)
    guide_paragraph = generate_unique_guide_paragraph(state_name)
    availability_paragraph = generate_unique_availability_paragraph(state_name)
    verified_bondsman_paragraph = generate_unique_verified_bondsman_paragraph(state_name)
    nationwide_coverage_paragraph = generate_unique_nationwide_coverage_paragraph(state_name)
    county_intro_paragraph = generate_county_intro_paragraph(state_name, counties)
    faq_items = generate_faq_items(state_name)
    
    # Replace placeholders in the template
    content = content.replace("[STATE_NAME]", state_name)
    content = content.replace("[STATE_CAPITAL]", capital)
    content = content.replace("[STATE_ABBR]", state_abbr)
    content = content.replace("[STATE_NICKNAME]", state_nickname)
    content = content.replace("[STATE_POPULATION]", population)
    content = content.replace("[STATE_NUM_COUNTIES]", str(num_counties))
    content = content.replace("[STATE_ECONOMY]", economy)
    content = content.replace("[STATE_CRIMINAL_JUSTICE]", criminal_justice)
    content = content.replace("[STATE_GEOGRAPHY]", geography)
    content = content.replace("[STATE_WEATHER]", weather)
    
    # Replace city placeholders
    if len(cities) >= 2:
        content = content.replace("[STATE_CITY_1]", cities[0])
        content = content.replace("[STATE_CITY_2]", cities[1])
    elif len(cities) == 1:
        content = content.replace("[STATE_CITY_1]", cities[0])
        content = content.replace("[STATE_CITY_2]", "other communities")
    else:
        content = content.replace("[STATE_CITY_1]", "major cities")
        content = content.replace("[STATE_CITY_2]", "communities")
    
    # Replace county placeholders
    if len(counties) >= 3:
        content = content.replace("[COUNTY_1]", counties[0])
        content = content.replace("[COUNTY_2]", counties[1])
        content = content.replace("[COUNTY_3]", counties[2])
    elif len(counties) == 2:
        content = content.replace("[COUNTY_1]", counties[0])
        content = content.replace("[COUNTY_2]", counties[1])
        content = content.replace("[COUNTY_3]", "Other Counties")
    elif len(counties) == 1:
        content = content.replace("[COUNTY_1]", counties[0])
        content = content.replace("[COUNTY_2]", "Other Counties")
        content = content.replace("[COUNTY_3]", "")
    else:
        content = content.replace("[COUNTY_1]", "Major Counties")
        content = content.replace("[COUNTY_2]", "")
        content = content.replace("[COUNTY_3]", "")
    
    # Replace paragraphs
    content = content.replace("[INTRO_PARAGRAPH]", intro_paragraph)
    content = content.replace("[GUIDE_PARAGRAPH]", guide_paragraph)
    content = content.replace("[AVAILABILITY_SECTION]", availability_paragraph)
    content = content.replace("[VERIFIED_BONDSMAN_SECTION]", verified_bondsman_paragraph)
    content = content.replace("[NATIONWIDE_COVERAGE_SECTION]", nationwide_coverage_paragraph)
    content = content.replace("[COUNTY_INTRO_PARAGRAPH]", county_intro_paragraph)
    
    # Replace FAQ items
    content = content.replace("[FAQ_1_QUESTION]", faq_items["faq1_question"])
    content = content.replace("[FAQ_1_ANSWER]", faq_items["faq1_answer"])
    content = content.replace("[FAQ_2_QUESTION]", faq_items["faq2_question"])
    content = content.replace("[FAQ_2_ANSWER]", faq_items["faq2_answer"])
    content = content.replace("[FAQ_3_QUESTION]", faq_items["faq3_question"])
    content = content.replace("[FAQ_3_ANSWER]", faq_items["faq3_answer"])
    content = content.replace("[FAQ_4_QUESTION]", faq_items["faq4_question"])
    content = content.replace("[FAQ_4_ANSWER]", faq_items["faq4_answer"])
    content = content.replace("[FAQ_5_QUESTION]", faq_items["faq5_question"])
    content = content.replace("[FAQ_5_ANSWER]", faq_items["faq5_answer"])
    
    # Update the template_json with the modified content
    template_json["data"][content_key] = content
    
    return template_json
