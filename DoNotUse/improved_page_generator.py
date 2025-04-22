"""
Improved Page Generator for Bail Bonds Buddy Website

This script generates unique content for each state page on BailBondsBuddy.com
while preserving the exact WordPress/Divi formatting from the JSON template.
"""

import os
import json
import re
import random
from string import Template

# Create directories if they don't exist
os.makedirs('/home/ubuntu/bailbonds/state_data', exist_ok=True)
os.makedirs('/home/ubuntu/bailbonds/generated_pages', exist_ok=True)

# Load the Oklahoma JSON template
def load_oklahoma_template():
    try:
        with open('/home/ubuntu/upload/Oklahoma Bail Bondsman Emergency 24_7 Service.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: Oklahoma template JSON file not found")
        return None

# Function to replace state-specific content in the template
def replace_state_content(template_json, state_data):
    # Make a deep copy of the template to avoid modifying the original
    modified_json = json.loads(json.dumps(template_json))
    
    # Extract the data section which contains the page content
    data = modified_json.get('data', {})
    
    # Replace state name in all text fields
    for key, value in data.items():
        if isinstance(value, str):
            # Replace "Oklahoma" with the new state name
            value = re.sub(r'\bOklahoma\b', state_data['name'], value)
            
            # Replace "Sooner State" with the new state nickname
            value = re.sub(r'\bSooner State\b', state_data['nickname'], value)
            
            # Replace county names
            value = re.sub(r'\bOklahoma County\b', state_data['largest_counties'][0], value)
            value = re.sub(r'\bTulsa County\b', state_data['largest_counties'][1], value)
            value = re.sub(r'\bCleveland County\b', state_data['largest_counties'][2], value)
            
            # Replace city names
            for i, city in enumerate(state_data['major_cities']):
                if i == 0:
                    value = re.sub(r'\bOklahoma City\b', city, value)
                elif i == 1:
                    value = re.sub(r'\bTulsa\b', city, value)
            
            # Update the value in the data dictionary
            data[key] = value
    
    # Find and replace the state-specific content sections
    for key, value in data.items():
        if isinstance(value, str) and "Oklahoma: The Sooner State" in value:
            # Replace the state description section
            state_section = f"{state_data['name']}: The {state_data['nickname']}\n\n"
            state_section += f"{state_data['name']}, known as the {state_data['nickname']}, combines rich Native American heritage, pioneering spirit, and modern economic growth across its diverse landscape. With a population of approximately {state_data['population']} residents spread throughout {state_data['num_counties']} counties, {state_data['name']} presents unique challenges and opportunities within its criminal justice system.\n\n"
            state_section += f"The state's largest metropolitan areas – {state_data['major_cities'][0]} and {state_data['major_cities'][1]} – account for the highest concentration of arrests and bail needs, but {state_data['name']}'s extensive rural communities also require specialized bail bond services. {state_data['name']}'s county jail system operates under state supervision while maintaining individual county administration, creating a patchwork of procedures that experienced bail bondsmen must navigate daily.\n\n"
            state_section += f"{state_data['economic_info']}\n\n"
            state_section += f"{state_data['bail_system_info']}\n\n"
            state_section += f"{state_data['criminal_justice_info']}\n\n"
            state_section += f"{state_data['geographical_info']}\n\n"
            state_section += f"{state_data['weather_info']}\n\n"
            state_section += f"For families seeking to secure a loved one's release from any of {state_data['name']}'s detention facilities, working with a {state_data['name']}-based bail bondsman who understands the state's unique characteristics provides the most efficient path to reunion and beginning the next steps in the legal process."
            
            # Update the value in the data dictionary
            data[key] = value.replace("Oklahoma: The Sooner State", state_section)
    
    # Replace FAQ content
    for key, value in data.items():
        if isinstance(value, str) and "How long does it take to get released using a bail bond?" in value:
            # Find the accordion items and replace them with new FAQs
            for i, faq in enumerate(state_data['faqs']):
                if i == 0:
                    value = re.sub(r'title="How long does it take to get released using a bail bond\?"[^>]*>.*?<\/et_pb_accordion_item>', 
                                  f'title="{faq["question"]}" open="on" _builder_version="4.27.4" _module_preset="default" global_colors_info={{}}><div>\n<div><span>{faq["answer"]}</span></div>\n</div></et_pb_accordion_item>', 
                                  value, flags=re.DOTALL)
                elif i == 1:
                    value = re.sub(r'title="What kind of collateral is accepted for bail bonds\?"[^>]*>.*?<\/et_pb_accordion_item>', 
                                  f'title="{faq["question"]}" _builder_version="4.27.4" _module_preset="default" global_colors_info={{}} open="off"><div>\n<div><span>{faq["answer"]}</span></div>\n</div></et_pb_accordion_item>', 
                                  value, flags=re.DOTALL)
                elif i == 2:
                    value = re.sub(r'title="What is the typical cost of a bail bond\?"[^>]*>.*?<\/et_pb_accordion_item>', 
                                  f'title="{faq["question"]}" _builder_version="4.27.4" _module_preset="default" global_colors_info={{}} open="off"><div>\n<div><span>{faq["answer"]}</span></div>\n</div></et_pb_accordion_item>', 
                                  value, flags=re.DOTALL)
                elif i == 3:
                    value = re.sub(r'title="What information do I need when contacting a bail bondsman\?"[^>]*>.*?<\/et_pb_accordion_item>', 
                                  f'title="{faq["question"]}" _builder_version="4.27.4" _module_preset="default" global_colors_info={{}} open="off"><div>\n<div><span>{faq["answer"]}</span></div>\n</div></et_pb_accordion_item>', 
                                  value, flags=re.DOTALL)
                elif i == 4:
                    value = re.sub(r'title="What types of payments do bail bondsmen accept\?"[^>]*>.*?<\/et_pb_accordion_item>', 
                                  f'title="{faq["question"]}" _builder_version="4.27.4" _module_preset="default" global_colors_info={{}} open="off"><div>\n<div><span>{faq["answer"]}</span></div>\n</div></et_pb_accordion_item>', 
                                  value, flags=re.DOTALL)
            
            # Update the value in the data dictionary
            data[key] = value
    
    # Replace "Major Counties in Oklahoma" heading
    for key, value in data.items():
        if isinstance(value, str) and "Major Counties in Oklahoma" in value:
            value = value.replace("Major Counties in Oklahoma", f"Major Counties in {state_data['name']}")
            data[key] = value
    
    # Update the modified JSON with the new data
    modified_json['data'] = data
    
    return modified_json

# Function to load state data from JSON file
def load_state_data(state_name):
    """Load state data from JSON file"""
    filename = f"/home/ubuntu/bailbonds/state_data/{state_name.lower().replace(' ', '_')}.json"
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Data file for {state_name} not found at {filename}")
        return None

# Function to generate a page for a specific state
def generate_page_for_state(state_name, template_json):
    """Generate a complete page for a specific state"""
    print(f"Generating page for {state_name}...")
    
    # Load state data
    state_data = load_state_data(state_name)
    if not state_data:
        print(f"Failed to generate page for {state_name}: No data available")
        return False
    
    # Replace state content in the template
    modified_json = replace_state_content(template_json, state_data)
    if not modified_json:
        print(f"Failed to generate page for {state_name}: Content replacement error")
        return False
    
    # Save to file
    filename = f"/home/ubuntu/bailbonds/generated_pages/{state_name.lower().replace(' ', '_')}.json"
    with open(filename, 'w') as f:
        json.dump(modified_json, f, indent=2)
    
    print(f"Page for {state_name} generated successfully and saved to {filename}")
    return True

# Function to generate a sample state for testing
def generate_sample_state_data():
    """Generate sample data for Texas to test the script"""
    print("Generating sample data for Texas...")
    
    texas_data = {
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
            "Dallas"
        ],
        "economic_info": "Texas's economy has traditionally centered around energy production and technology, with oil and natural gas remaining significant industries. However, recent economic diversification has expanded into aerospace, biotechnology, telecommunications, and healthcare. This economic evolution has affected crime patterns and bail requirements throughout the state, with growing urban centers experiencing different needs than rural communities.",
        "bail_system_info": "The state maintains a robust bail system governed by the Texas Occupations Code Chapter 1704 (Bail Bond Sureties), which requires all bondsmen to be licensed through the Texas Department of Insurance. Texas law establishes standard premium rates (typically 10% of the bail amount) and regulates bondsman practices to protect consumers during vulnerable times.",
        "criminal_justice_info": "Recent criminal justice reform initiatives in Texas have aimed to improve the state's bail system, focusing on risk assessment rather than financial ability. These reforms have modified certain bail procedures, especially for non-violent offenses, making professional guidance from experienced bondsmen even more valuable for navigating the changing legal landscape.",
        "geographical_info": "Texas's vast size, international border with Mexico, and Gulf Coast create unique jurisdictional challenges for bail bondsmen. The state's diverse geography, from urban centers to rural communities spanning hundreds of miles, requires bondsmen to navigate varying county procedures and sometimes coordinate across long distances.",
        "weather_info": "Weather emergencies, from hurricanes and tropical storms to tornadoes and flooding, can occasionally impact court schedules and bail processing timelines. Local bondsmen familiar with Texas's systems know how to manage these disruptions while ensuring clients meet all legal obligations.",
        "faqs": [
            {
                "question": "How long does it take to get released using a bail bond in Texas?",
                "answer": "After a bail bond is posted in Texas, release times typically range from 4-12 hours depending on the facility's processing speed and how busy they are. In larger counties like Harris or Dallas, processing can take longer than in smaller counties. Weekend and holiday arrests may take additional time to process. The bondsman will keep you updated on the progress throughout the release process."
            },
            {
                "question": "What kind of collateral is accepted for bail bonds in Texas?",
                "answer": "Bail bondsmen in Texas typically accept various forms of collateral including real estate, vehicles, jewelry, electronics, and other valuable assets. Texas has specific regulations regarding property bonds, particularly for real estate collateral. Some bondsmen may also accept co-signers with good credit as an alternative to physical collateral. The specific requirements vary by bondsman and the amount of the bail."
            },
            {
                "question": "What is the typical cost of a bail bond in Texas?",
                "answer": "In Texas, bail bond fees typically range from 8-10% of the total bail amount, though this can vary by county and bondsman. For example, if bail is set at $10,000, you would pay $800-1,000 to the bondsman. This fee is non-refundable as it represents the bondsman's service fee for posting the full bail amount. Some Texas bondsmen offer payment plans for those who cannot pay the full premium upfront."
            },
            {
                "question": "What happens if someone fails to appear in court after posting bail in Texas?",
                "answer": "If a defendant fails to appear in court after posting bail in Texas, the court issues a bench warrant for their immediate arrest and the bail bond is forfeited. Texas law gives bondsmen a specific time period (typically 120-180 days) to locate and surrender the defendant before paying the full bond amount. Recovery agents may be employed to find the defendant, and the person who signed for the bond may lose any collateral provided and become responsible for the full bail amount plus recovery costs."
            },
            {
                "question": "How can I find a reputable bail bondsman in Texas?",
                "answer": "To find a reputable bail bondsman in Texas, start by verifying their license through the Texas Department of Insurance or your county's bail bond board. Look for bondsmen with positive reviews, several years of experience, and 24/7 availability. Ask about their fee structure, payment options, and any additional requirements upfront. BailBondsBuddy.com provides access to pre-screened, licensed bail bond professionals throughout Texas who meet our strict standards for reliability and ethical business practices."
            }
        ]
    }
    
    # Save Texas data to JSON file
    filename = "/home/ubuntu/bailbonds/state_data/texas.json"
    with open(filename, 'w') as f:
        json.dump(texas_data, f, indent=2)
    
    print(f"Sample data for Texas saved to {filename}")
    return texas_data

# Main function to test the script with a sample state
def test_with_sample_state():
    """Test the script with a sample state (Texas)"""
    print("Testing page generation with sample state (Texas)...")
    
    # Load the Oklahoma template
    template_json = load_oklahoma_template()
    if not template_json:
        print("Failed to load Oklahoma template")
        return False
    
    # Generate sample state data for Texas
    generate_sample_state_data()
    
    # Generate page for Texas
    success = generate_page_for_state("Texas", template_json)
    
    if success:
        print("Test successful! The script can now be used to generate pages for all 49 remaining states.")
        return True
    else:
        print("Test failed. Please check the error messages above.")
        return False

# Function to generate pages for all states
def generate_all_state_pages():
    """Generate pages for all 50 states"""
    print("Starting page generation for all states...")
    
    # Load the Oklahoma template
    template_json = load_oklahoma_template()
    if not template_json:
        print("Failed to load Oklahoma template")
        return False
    
    # Get list of all state data files
    state_data_dir = "/home/ubuntu/bailbonds/state_data"
    state_files = [f for f in os.listdir(state_d
(Content truncated due to size limit. Use line ranges to read in chunks)