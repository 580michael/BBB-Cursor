#!/usr/bin/env python3
"""
State Page Creator for Bail Bonds Buddy
This script creates state pages with modular components and dynamic FAQ content.
"""

import requests
import random
import os
import re
import time
import json
import markdown

# API Constants
BASE_URL = "https://bailbondsbuddy.com"
AUTH = ("bbbuddy", "DpSm eiz8 yHjx Sqqk G3lG fqU6")

# State Data
STATE_DATA = {
    "Oklahoma": {
        "abbreviation": "OK",
        "capital": {
            "name": "Oklahoma City",
            "address": "Oklahoma State Capitol, Oklahoma City, OK 73105",
            "lat": "35.492207",
            "lng": "-97.503342"
        },
        "counties": ["Oklahoma County", "Tulsa County", "Cleveland County"],
        "sample_cities": ["Oklahoma City", "Tulsa", "Norman", "Edmond", "Lawton"]
    },
    "Texas": {
        "abbreviation": "TX",
        "capital": {
            "name": "Austin",
            "address": "Texas State Capitol, 1100 Congress Ave, Austin, TX 78701",
            "lat": "30.274702",
            "lng": "-97.740341"
        },
        "counties": ["Harris County", "Dallas County", "Bexar County"],
        "sample_cities": ["Houston", "Dallas", "San Antonio", "Austin", "Fort Worth"]
    },
    "Florida": {
        "abbreviation": "FL",
        "capital": {
            "name": "Tallahassee",
            "address": "Florida State Capitol, 400 S Monroe St, Tallahassee, FL 32399",
            "lat": "30.438118",
            "lng": "-84.281296"
        },
        "counties": ["Miami-Dade County", "Broward County", "Orange County"],
        "sample_cities": ["Miami", "Orlando", "Tampa", "Jacksonville", "Fort Lauderdale"]
    }
}

# SEO Keywords
KEYWORDS = [
    "bail bonds", "bail bondsman", "bail bond services", 
    "bail bond agent", "bail bonds company", "24/7 bail bonds",
    "local bail bonds", "affordable bail bonds", "fast bail bonds"
]

MODIFIERS = [
    "best", "top", "trusted", "reliable", "professional", 
    "experienced", "licensed", "expert", "24 hour", "local"
]

def select_keywords():
    """Select a random keyword and modifier for SEO purposes"""
    keyword = random.choice(KEYWORDS)
    modifier = random.choice(MODIFIERS)
    return {
        "keyword": keyword,
        "modifier": modifier
    }

def format_title(keyword_data, location_name):
    """Format the page title with location and keywords"""
    return f"Bail Bonds in {location_name} | {keyword_data['modifier'].title()} {keyword_data['keyword'].title()}"

def create_slug(keyword_data, location_name, location_type="state"):
    """Create a URL slug for the page"""
    # Get state abbreviation if available
    abbr = ""
    if location_type == "state" and location_name in STATE_DATA:
        abbr = STATE_DATA[location_name]["abbreviation"].lower()
        abbr = f"-{abbr}"
    
    base_slug = f"bail-bonds-in-{location_name.lower().replace(' ', '-')}{abbr}"
    return base_slug

def generate_meta_description(keyword_data, location_name):
    """Generate a meta description for SEO"""
    templates = [
        f"Find {keyword_data['modifier']} {keyword_data['keyword']} in {location_name}. 24/7 service, fast release, flexible payment options. Licensed bail bond agents ready to help.",
        f"Need a bail bondsman in {location_name}? Our {keyword_data['modifier']} {keyword_data['keyword']} provide immediate assistance with jail release. Available 24/7.",
        f"{location_name} {keyword_data['keyword']} services you can trust. Our {keyword_data['modifier']} agents help with quick jail release and affordable rates."
    ]
    return random.choice(templates)

def load_faqs(state_name):
    """Load and customize FAQs for a specific state"""
    try:
        # Path to FAQ file
        faq_file = "FAQ.md"
        
        # Check if file exists
        if not os.path.exists(faq_file):
            # Create a sample FAQ file if it doesn't exist
            sample_faqs = """
# Bail Bonds FAQ

## What is a bail bond?
A bail bond is a financial guarantee that an arrested person will appear for their court dates. In [state_name], bail bond agents typically charge a [premium_rate]% fee of the total bail amount.

## How much does a bail bond cost in [state_name]?
In [state_name], bail bond companies usually charge [premium_rate]% of the total bail amount as a non-refundable fee. For example, if the bail is set at $10,000, you'll pay $[premium_rate * 100] for the bond.

## How quickly can someone be released on bail in [state_name]?
Release times vary by jail and case complexity, but in [state_name], most defendants are released within 2-8 hours after posting bail. Larger facilities may take longer.

## What forms of payment do bail bondsmen accept in [state_name]?
Most [state_name] bail bond agencies accept credit cards, debit cards, cash, and sometimes payment plans. Some may also accept collateral like property or vehicles for larger bonds.

## Can I get a bail bond refunded in [state_name]?
No, the premium paid to a bail bondsman (typically [premium_rate]% of the bail amount) is non-refundable in [state_name]. This is the fee for their service of posting the full bail amount.

## What happens if someone misses court after getting a bail bond?
If the defendant misses court, the bail bond may be forfeited and the full bail amount becomes due. The bondsman will try to locate the defendant, and a bench warrant will be issued.

## Do I need collateral for a bail bond in [state_name]?
Not always. For smaller bail amounts in [state_name], many bondsmen don't require collateral. For larger amounts, they may ask for collateral equal to the bond amount.

## Are there special bail bond requirements in [state_name]?
Yes, [state_name] has [recent_state_change] that affects how bail bonds work. Additionally, [state_specific_factor] may impact certain cases.

## Can bail bond agents arrest someone who skips court?
Yes, in [state_name], licensed bail bond agents have the authority to arrest their clients who fail to appear in court and return them to custody.

## How do I find a reputable bail bondsman in [state_name]?
Look for licensed, experienced bail bond agents in [state_name] with good reviews. Verify their license with the [state_name] Department of Insurance or regulatory agency.
"""
            with open(faq_file, "w") as f:
                f.write(sample_faqs)
        
        # Read the FAQ file
        with open(faq_file, "r") as f:
            content = f.read()
        
        # Extract questions and answers
        faqs = []
        sections = re.split(r'\n## ', content)
        
        # Skip the header section
        for section in sections[1:]:
            parts = section.split('\n', 1)
            if len(parts) == 2:
                question = parts[0]
                answer = parts[1].strip()
                
                # Replace placeholders
                question = question.replace('[state_name]', state_name)
                answer = answer.replace('[state_name]', state_name)
                
                # Replace premium rate (use 10% for some states, 15% for others)
                premium_rate = "10" if state_name in ["Texas", "Florida", "California"] else "15"
                question = question.replace('[premium_rate]', premium_rate)
                answer = answer.replace('[premium_rate]', premium_rate)
                
                # State-specific replacements
                state_specifics = {
                    "Oklahoma": {
                        "recent_state_change": "recent reforms in bail procedures",
                        "state_specific_factor": "county-specific bail schedules"
                    },
                    "Texas": {
                        "recent_state_change": "the 2021 bail reform legislation",
                        "state_specific_factor": "different county bail practices"
                    },
                    "Florida": {
                        "recent_state_change": "updated pretrial release guidelines",
                        "state_specific_factor": "varying bail schedules by judicial circuit"
                    }
                }
                
                # Apply state-specific replacements if available
                if state_name in state_specifics:
                    for key, value in state_specifics[state_name].items():
                        answer = answer.replace(f'[{key}]', value)
                
                # Convert markdown to HTML for the answer
                answer_html = markdown.markdown(answer)
                
                faqs.append({
                    "question": question,
                    "answer": answer_html
                })
        
        # Select 5 random FAQs
        if len(faqs) > 5:
            faqs = random.sample(faqs, 5)
        
        return faqs
    
    except Exception as e:
        print(f"Error loading FAQs: {str(e)}")
        return []

def create_state_page(state_name):
    """Create a state page with modular components"""
    if state_name not in STATE_DATA:
        print(f"Error: {state_name} data not available")
        return None
    
    try:
        # Get state data
        state_data = STATE_DATA[state_name]
        
        # Select keywords for SEO
        keyword_data = select_keywords()
        
        # Format title and slug
        page_title = format_title(keyword_data, state_name)
        page_slug = create_slug(keyword_data, state_name)
        
        # Generate meta description
        meta_description = generate_meta_description(keyword_data, state_name)
        
        # Load and customize FAQs
        faqs = load_faqs(state_name)
        
        # Create FAQ content
        faq_content = ""
        if faqs:
            faq_content = '[et_pb_section fb_built="1" _builder_version="4.14.7" _module_preset="default" background_color="#f4f4f4" custom_padding="50px|0px|50px|0px|false|false"][et_pb_row _builder_version="4.14.7" _module_preset="default"][et_pb_column type="4_4" _builder_version="4.14.7" _module_preset="default"][et_pb_text _builder_version="4.14.7" _module_preset="default" header_font="Montserrat|600|||||||" header_text_color="#0c71c3" header_font_size="32px" header_2_font="Montserrat|600|||||||" header_2_text_color="#333333" header_2_font_size="24px" text_orientation="center"]<h2>Frequently Asked Questions About Bail Bonds in {state_name}</h2>[/et_pb_text][et_pb_accordion open_toggle_text_color="#0c71c3" _builder_version="4.14.7" _module_preset="default" toggle_font="Montserrat|600|||||||" toggle_text_color="#333333" body_font="Open Sans||||||||" body_text_color="#666666" border_width_all="0px" custom_margin="20px||20px||false|false"]'
            
            for faq in faqs:
                faq_content += f'[et_pb_accordion_item title="{faq["question"]}" open="off" _builder_version="4.14.7" _module_preset="default"]{faq["answer"]}[/et_pb_accordion_item]'
            
            faq_content += '[/et_pb_accordion][/et_pb_column][/et_pb_row][/et_pb_section]'
        
        # Create modular content using Divi builder
        content = f"""
[et_pb_section fb_built="1" _builder_version="4.14.7" _module_preset="default" background_color="#ffffff" custom_padding="0px|0px|0px|0px|false|false" global_colors_info="{{}}"][et_pb_row _builder_version="4.14.7" _module_preset="default" width="100%" max_width="2560px" custom_margin="||||false|false" custom_padding="||||false|false" global_colors_info="{{}}"][et_pb_column type="4_4" _builder_version="4.14.7" _module_preset="default" global_colors_info="{{}}"][et_pb_text _builder_version="4.14.7" _module_preset="default" header_font="Montserrat|700|||||||" header_text_color="#0c71c3" header_font_size="36px" header_line_height="1.5em" text_line_height="1.8em" text_orientation="center" custom_margin="50px||20px||false|false" header_font_size_tablet="" header_font_size_phone="28px" header_font_size_last_edited="on|phone" global_colors_info="{{}}"]<h1>Bail Bonds in {state_name}</h1>
<p>Find trusted bail bond agents in {state_name} to help with fast jail release and affordable payment options.</p>[/et_pb_text][/et_pb_column][/et_pb_row][/et_pb_section]

[et_pb_section fb_built="1" _builder_version="4.14.7" _module_preset="default" background_color="#0c71c3" custom_padding="30px|0px|30px|0px|false|false" global_colors_info="{{}}"][et_pb_row _builder_version="4.14.7" _module_preset="default" custom_margin="||||false|false" custom_padding="||||false|false" global_colors_info="{{}}"][et_pb_column type="4_4" _builder_version="4.14.7" _module_preset="default" global_colors_info="{{}}"][et_pb_text _builder_version="4.14.7" _module_preset="default" text_font="Montserrat||||||||" text_text_color="#ffffff" text_font_size="22px" text_line_height="1.6em" text_orientation="center" global_colors_info="{{}}"]<p>Need a Bail Bondsman in {state_name}?</p>[/et_pb_text][et_pb_button button_url="tel:8887338710" button_text="Call (888) 733-8710" button_alignment="center" _builder_version="4.14.7" _module_preset="default" custom_button="on" button_text_color="#0c71c3" button_bg_color="#ffffff" button_border_width="0px" button_border_radius="30px" button_font="Montserrat|600||on|||||" button_use_icon="off" custom_margin="10px||||false|false" custom_padding="15px|30px|15px|30px|false|false" global_colors_info="{{}}"][/et_pb_button][/et_pb_column][/et_pb_row][/et_pb_section]

[et_pb_section fb_built="1" _builder_version="4.14.7" _module_preset="default" custom_padding="50px||50px||false|false" global_colors_info="{{}}"][et_pb_row _builder_version="4.14.7" _module_preset="default" global_colors_info="{{}}"][et_pb_column type="4_4" _builder_version="4.14.7" _module_preset="default" global_colors_info="{{}}"][et_pb_text _builder_version="4.14.7" _module_preset="default" header_2_font="Montserrat|600|||||||" header_2_text_color="#0c71c3" header_2_font_size="28px" global_colors_info="{{}}"]<h2>How Bail Bonds Work in {state_name}</h2>
<p>When someone is arrested in {state_name}, a judge sets a bail amount that must be paid for the defendant to be released from jail until their court date. Bail bond agents in {state_name} provide a service by posting the full bail amount in exchange for a non-refundable fee (typically 10-15% of the total bail).</p>
<p>Working with a {state_name} bail bondsman is straightforward:</p>
<ol>
<li>Contact a licensed bail bond agent in your area</li>
<li>Provide defendant information and the jail location</li>
<li>Pay the premium fee (10-15% of the total bail amount)</li>
<li>Complete paperwork and potentially provide collateral</li>
<li>The bondsman posts bail and the defendant is released</li>
</ol>
<p>For most {state_name} residents, using a bail bond service is the most affordable option when bail is set at a high amount.</p>[/et_pb_text][/et_pb_column][/et_pb_row][/et_pb_section]

[et_pb_section fb_built="1" _builder_version="4.14.7" _module_preset="default" custom_padding="20px||50px||false|false" global_colors_info="{{}}"][et_pb_row _builder_version="4.14.7" _module_preset="default" global_colors_info="{{}}"][et_pb_column type="4_4" _builder_version="4.14.7" _module_preset="default" global_colors_info="{{}}"][et_pb_text _builder_version="4.14.7" _module_preset="default" header_2_font="Montserrat|600|||||||" header_2_text_color="#0c71c3" header_2_font_size="28px" text_orientation="center" global_colors_info="{{}}"]<h2>Major Counties in {state_name}</h2>[/et_pb_text][/et_pb_column][/et_pb_row][et_pb_row column_structure="1_3,1_3,1_3" _builder_version="4.14.7" _module_preset="default" custom_padding="20px||||false|false" global_colors_info="{{}}"][et_pb_column type="1_3" _builder_version="4.14.7" _module_preset="default" global_colors_info="{{}}"][et_pb_blurb title="{state_data['counties'][0]}" use_icon="on" font_icon="%%277%%" icon_color="#0c71c3" _builder_version="4.14.7" _module_preset="default" header_font="Montserrat|600|||||||" header_text_color="#333333" body_font="Open Sans||||||||" text_alignment="center" custom_margin="||30px||false|false" global_colors_info="{{}}"]
<p>Find reliable bail bond services throughout {state_data['counties'][0]}. Our network includes experienced agents ready to help 24/7.</p>
[/et_pb_blurb][et_pb_button button_url="https://bailbondsbuddy.com/bail-bonds-in-{state_data['counties'][0].lower().replace(' ', '-').replace('-county', '')}-{state_data['abbreviation'].lower()}" button_text="View Bondsmen" button_alignment="center" _builder_version="4.14.7" _module_preset="default" custom_button="on" button_text_color="#ffffff" button_bg_color="#0c71c3" button_border_width="0px" button_border_radius="5px" button_font="Montserrat|600||on|||||" global_colors_info="{{}}"][/et_pb_button][/et_pb_column][et_pb_column type="1_3" _builder_version="4.14.7" _module_preset="default" global_colors_info="{{}}"][et_pb_blurb title="{state_data['counties'][1]}" use_icon="on" font_icon="%%277%%" icon_color="#0c71c3" _builder_version="4.14.7" _module_preset="default" header_font="Montserrat|600|||||||" header_text_color="#333333" body_font="Open Sans||||||||" text_alignment="center" custom_margin="||30px||false|false" global_colors_info="{{}}"]
<p>Connect with professional bail bond agents in {state_data['counties'][1]} for fast jail release and affordable payment plans.</p>
[/et_pb_blurb][et_pb_button button_url="https://bailbondsbuddy.com/bail-bonds-in-{state_data['counties'][1].lower().replace(' ', '-').replace('-county', '')}-{state_data['abbreviation'].lower()}" button_text="View Bondsmen" button_alignment="center" _builder_version="4.14.7" _module_preset="default" custom_button="on" button_text_color="#ffffff" button_bg_color="#0c71c3" button_border_width="0px" button_border_radius="5px" button_font="Montserrat|600||on|||||" global_colors_info="{{}}"][/et_pb_button][/et_pb_column][et_pb_column type="1_3" _builder_version="4.14.7" _module_preset="default" global_colors_info="{{}}"][et_pb_blurb title="{state_data['counties'][2]}" use_icon="on" font_icon="%%277%%" icon_color="#0c71c3" _builder_version="4.14.7" _module_preset="default" header_font="Montserrat|600|||||||" header_text_color="#333333" body_font="Open Sans||||||||" text_alignment="center" custom_margin="||30px||false|false" global_colors_info="{{}}"]
<p>Get immediate assistance from licensed bail bondsmen serving all areas of {state_data['counties'][2]}.</p>
[/et_pb_blurb][et_pb_button button_url="https://bailbondsbuddy.com/bail-bonds-in-{state_data['counties'][2].lower().replace(' ', '-').replace('-county', '')}-{state_data['abbreviation'].lower()}" button_text="View Bondsmen" button_alignment="center" _builder_version="4.14.7" _module_preset="default" custom_button="on" button_text_color="#ffffff" button_bg_color="#0c71c3" button_border_width="0px" button_border_radius="5px" button_font="Montserrat|600||on|||||" global_colors_info="{{}}"][/et_pb_button][/et_pb_column][/et_pb_row][/et_pb_section]

[et_pb_section fb_built="1" _builder_version="4.14.7" _module_preset="default" background_color="#f8f8f8" custom_padding="50px||50px||false|false" global_colors_info="{{}}"][et_pb_row _builder_version="4.14.7" _module_preset="default" global_colors_info="{{}}"][et_pb_column type="4_4" _builder_version="4.14.7" _module_preset="default" global_colors_info="{{}}"][et_pb_text _builder_version="4.14.7" _module_preset="default" header_2_font="Montserrat|600|||||||" header_2_text_color="#0c71c3" header_2_font_size="28px" text_orientation="center" global_colors_info="{{}}"]<h2>Bail Bond Services in {state_name}</h2>[/et_pb_text][/et_pb_column][/et_pb_row][et_pb_row column_structure="1_3,1_3,1_3" _builder_version="4.14.7" _module_preset="default" custom_padding="20px||||false|false" global_colors_info="{{}}"][et_pb_column type="1_3" _builder_version="4.14.7" _module_preset="default" global_colors_info="{{}}"][et_pb_blurb title="24/7 Availability" use_icon="on" font_icon="%%88%%" icon_color="#0c71c3" _builder_version="4.14.7" _module_preset="default" header_font="Montserrat|600|||||||" header_text_color="#333333" header_line_height="1.5em" body_font="Open Sans||||||||" text_alignment="center" custom_margin="||30px||false|false" global_colors_info="{{}}"]
<p>Our network of bail bondsmen in {state_name} are available 24 hours a day, 7 days a week, including holidays.</p>
[/et_pb_blurb][/et_pb_column][et_pb_column type="1_3" _builder_version="4.14.7" _module_preset="default" global_colors_info="{{}}"][et_pb_blurb title="Statewide Coverage" use_icon="on" font_icon="%%47%%" icon_color="#0c71c3" _builder_version="4.14.7" _module_preset="default" header_font="Montserrat|600|||||||" header_text_color="#333333" header_line_height="1.5em" body_font="Open Sans||||||||" text_alignment="center" custom_margin="||30px||false|false" global_colors_info="{{}}"]
<p>We connect you with licensed bail bond agents throughout {state_name}, serving all counties and local jails.</p>
[/et_pb_blurb][/et_pb_column][et_pb_column type="1_3" _builder_version="4.14.7" _module_preset="default" global_colors_info="{{}}"][et_pb_blurb title="Flexible Payment Options" use_icon="on" font_icon="%%253%%" icon_color="#0c71c3" _builder_version="4.14.7" _module_preset="default" header_font="Montserrat|600|||||||" header_text_color="#333333" header_line_height="1.5em" body_font="Open Sans||||||||" text_alignment="center" custom_margin="||30px||false|false" global_colors_info="{{}}"]
<p>Most bail bond agents in our {state_name} network offer payment plans and accept various payment methods.</p>
[/et_pb_blurb][/et_pb_column][/et_pb_row][et_pb_row column_structure="1_2,1_2" _builder_version="4.14.7" _module_preset="default" global_colors_info="{{}}"][et_pb_column type="1_2" _builder_version="4.14.7" _module_preset="default" global_colors_info="{{}}"][et_pb_blurb title="Fast Release Process" use_icon="on" font_icon="%%105%%" icon_color="#0c71c3" _builder_version="4.14.7" _module_preset="default" header_font="Montserrat|600|||||||" header_text_color="#333333" header_line_height="1.5em" body_font="Open Sans||||||||" text_alignment="center" custom_margin="||30px||false|false" global_colors_info="{{}}"]
<p>Our bail bondsmen work quickly to process paperwork and secure release from {state_name} jails as fast as possible.</p>
[/et_pb_blurb][/et_pb_column][et_pb_column type="1_2" _builder_version="4.14.7" _module_preset="default" global_colors_info="{{}}"][et_pb_blurb title="Licensed & Experienced" use_icon="on" font_icon="%%117%%" icon_color="#0c71c3" _builder_version="4.14.7" _module_preset="default" header_font="Montserrat|600|||||||" header_text_color="#333333" header_line_height="1.5em" body_font="Open Sans||||||||" text_alignment="center" custom_margin="||30px||false|false" global_colors_info="{{}}"]
<p>All bail bond agents in our {state_name} network are properly licensed, insured, and experienced in the local court system.</p>
[/et_pb_blurb][/et_pb_column][/et_pb_row][/et_pb_section]

[et_pb_section fb_built="1" _builder_version="4.14.7" _module_preset="default" custom_padding="50px||50px||false|false" global_colors_info="{{}}"][et_pb_row _builder_version="4.14.7" _module_preset="default" global_colors_info="{{}}"][et_pb_column type="4_4" _builder_version="4.14.7" _module_preset="default" global_colors_info="{{}}"][et_pb_text _builder_version="4.14.7" _module_preset="default" header_2_font="Montserrat|600|||||||" header_2_text_color="#0c71c3" header_2_font_size="28px" text_orientation="center" global_colors_info="{{}}"]<h2>Find Bail Bond Agents in {state_name}</h2>[/et_pb_text][/et_pb_column][/et_pb_row][et_pb_row column_structure="1_2,1_2" _builder_version="4.14.7" _module_preset="default" global_colors_info="{{}}"][et_pb_column type="1_2" _builder_version="4.14.7" _module_preset="default" global_colors_info="{{}}"][et_pb_map address="{state_data['capital']['address']}" zoom_level="10" mouse_wheel="on" mobile_dragging="on" use_grayscale_filter="off" center_lat="{state_data['capital']['lat']}" center_lng="{state_data['capital']['lng']}" _builder_version="4.14.7" _module_preset="default" width="100%" height="400px" custom_margin="||||false|false" custom_padding="||||false|false" z_index="10" global_colors_info="{{}}" google_api_key="AIzaSyDjw2Qcr2TIxzzLNYMKN3zDQaE9_uYbMwI" fullscreen="on" zoom_control="on"]
[/et_pb_map][/et_pb_column][et_pb_column type="1_2" _builder_version="4.14.7" _module_preset="default" global_colors_info="{{}}"][et_pb_text _builder_version="4.14.7" _module_preset="default" global_colors_info="{{}}"]<h3>Bail Bondsmen Near You</h3>
<p>When you're facing a difficult situation with a loved one in jail, finding a reliable bail bondsman quickly is essential. Our network includes licensed bail bond agents throughout {state_name} who are ready to help 24/7.</p>
<p>Most bail bondsmen in {state_name} offer:</p>
<ul>
<li>Free consultations</li>
<li>24/7 service</li>
<li>Quick jail release</li>
<li>Flexible payment options</li>
<li>Confidential service</li>
</ul>
<p>Call (888) 733-8710 to connect with a bail bondsman in your area of {state_name} right now.</p>[/et_pb_text][et_pb_button button_url="tel:8887338710" button_text="Call (888) 733-8710" button_alignment="center" _builder_version="4.14.7" _module_preset="default" custom_button="on" button_text_color="#ffffff" button_bg_color="#0c71c3" button_border_width="0px" button_border_radius="5px" button_font="Montserrat|600||on|||||" button_icon="%%264%%" custom_margin="20px||||false|false" custom_padding="12px|30px|12px|30px|false|false" global_colors_info="{{}}"][/et_pb_button][/et_pb_column][/et_pb_row][/et_pb_section]

{faq_content}
"""
        
        # Prepare data for the API request
        data = {
            'title': page_title,
            'content': content,
            'status': 'publish',
            'slug': page_slug,
            'excerpt': meta_description,
            'meta': {
                '_yoast_wpseo_metadesc': meta_description
            }
        }
        
        # Make the API request
        try:
            response = requests.post(
                f"{BASE_URL}/wp-json/wp/v2/pages",
                auth=AUTH,
                json=data
            )
            
            if response.status_code >= 200 and response.status_code < 300:
                result = response.json()
                page_id = result.get('id')
                page_link = result.get('link')
                print(f"Successfully created page for {state_name} with ID {page_id}")
                print(f"Page URL: {page_link}")
                return page_id
            else:
                print(f"Error creating page: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"API request error: {str(e)}")
            return None
    
    except Exception as e:
        print(f"Error creating state page: {str(e)}")
        return None

def test():
    """Test function to create a single state page"""
    # Create a page for Oklahoma
    create_state_page("Oklahoma")
    
    # To create pages for all states in the STATE_DATA dictionary, uncomment:
    # for state_name in STATE_DATA.keys():
    #     print(f"Creating page for {state_name}...")
    #     create_state_page(state_name)
    #     time.sleep(2)  # Pause between requests to avoid overwhelming the API

if __name__ == "__main__":
    test() 