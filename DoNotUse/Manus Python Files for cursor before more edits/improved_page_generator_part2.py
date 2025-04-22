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
from improved_page_generator_part1 import load_template, load_state_data, save_state_page
from content_generator_utils_part1 import generate_unique_intro_paragraph
from content_generator_utils_part1 import generate_unique_guide_paragraph
from content_generator_utils_part2 import generate_unique_availability_section
from content_generator_utils_part2 import generate_unique_verified_bondsman_section
from content_generator_utils_part2 import generate_unique_nationwide_coverage_section
from content_generator_utils_part2 import generate_unique_county_intro
from content_generator_utils_part3 import generate_unique_faqs

def update_page_title(template_json, state_name):
    """Update the page title with the new state name"""
    if "title" in template_json:
        template_json["title"] = template_json["title"].replace("Oklahoma", state_name)
    return template_json

def update_content_sections(template_json, state_data):
    """Update all content sections with state-specific information"""
    state_name = state_data["name"]
    old_state = "Oklahoma"
    
    # Process all content sections
    if "content" in template_json:
        content = template_json["content"]
        
        # Replace state name in all content
        content = replace_state_references(content, old_state, state_name)
        
        # Replace county references
        old_counties = ["Oklahoma County", "Tulsa County", "Cleveland County"]
        new_counties = state_data["largest_counties"]
        content = replace_county_references(content, old_counties, new_counties)
        
        # Replace city references
        old_cities = ["Oklahoma City", "Tulsa"]
        new_cities = state_data["major_cities"][:2]  # Take first two cities
        content = replace_city_references(content, old_cities, new_cities)
        
        # Replace nickname references
        old_nickname = "Sooner State"
        new_nickname = state_data["nickname"]
        content = replace_nickname_references(content, old_nickname, new_nickname)
        
        # Replace population references
        old_population = "4 million"
        new_population = state_data["population"]
        content = replace_population_references(content, old_population, new_population)
        
        # Update state-specific content sections
        content = update_state_specific_sections(content, state_data)
        
        template_json["content"] = content
    
    return template_json

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
        
        # Create a deep copy of the template
        state_page = json.loads(json.dumps(template_json))
        
        # Update page title
        state_page = update_page_title(state_page, state_name)
        
        # Update content sections
        state_page = update_content_sections(state_page, state_data)
        
        # Save the generated page
        save_state_page(state_name, state_page, 'json')
        
        # Also save as HTML for preview
        save_state_page(state_name, state_page, 'html')
        
        return True
    except Exception as e:
        print(f"Error generating page for {state_name}: {e}")
        return False
