"""
Page Generator for Bail Bonds Buddy Website

This script generates unique content for each state page on BailBondsBuddy.com
while preserving the WordPress/Divi formatting.
"""

import os
import json
import re
import random
from string import Template

# Constants
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE_DATA_DIR = os.path.join(BASE_DIR, "state_data")
GENERATED_PAGES_DIR = os.path.join(BASE_DIR, "generated_pages")

# Create directory for generated pages if it doesn't exist
os.makedirs(GENERATED_PAGES_DIR, exist_ok=True)

# Template for state page content with WordPress/Divi formatting preserved
STATE_PAGE_TEMPLATE = """
<!-- wp:heading {"level":1} -->
<h1>${state_name}: The ${state_nickname}</h1>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>${state_name}, known as the ${state_nickname}, combines rich ${state_heritage} heritage, pioneering spirit, and modern economic growth across its diverse landscape. With a population of approximately ${state_population} residents spread throughout ${state_counties} counties, ${state_name} presents unique challenges and opportunities within its criminal justice system.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>The state's largest metropolitan areas – ${major_city_1} and ${major_city_2} – account for the highest concentration of arrests and bail needs, but ${state_name}'s extensive rural communities also require specialized bail bond services. ${state_name}'s county jail system operates under state supervision while maintaining individual county administration, creating a patchwork of procedures that experienced bail bondsmen must navigate daily.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>${economic_info}</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>${bail_system_info}</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>${criminal_justice_info}</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>${geographical_info}</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>${weather_info}</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>For families seeking to secure a loved one's release from any of ${state_name}'s detention facilities, working with a ${state_name}-based bail bondsman who understands the state's unique characteristics provides the most efficient path to reunion and beginning the next steps in the legal process.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":2} -->
<h2>Major Counties in ${state_name}</h2>
<!-- /wp:heading -->

<!-- wp:heading {"level":3} -->
<h3>${county_1_name}</h3>
<!-- /wp:heading -->

<!-- wp:heading {"level":3} -->
<h3>${county_2_name}</h3>
<!-- /wp:heading -->

<!-- wp:heading {"level":3} -->
<h3>${county_3_name}</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>When you or a loved one is arrested, time is of the essence. The jail system can be overwhelming and confusing, especially during such a stressful time. That's why connecting with a local bail bondsman immediately is crucial - they understand the specific procedures of your county jail, have established relationships with local law enforcement, and can navigate the release process efficiently. A local bondsman from your community knows exactly how to expedite paperwork through the local court system, potentially reducing jail time from days to just hours.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>BailBondsBuddy.com gives you instant access to trusted bondsmen throughout America, from small towns to major cities. Our network of licensed professionals offers 24/7 service, affordable payment plans, and complete confidentiality. They can explain local specific bail laws and requirements in plain language, help with paperwork, and even provide transportation from jail when needed. Don't waste precious time behind bars - use our simple search tool to find a local bondsman in your area who can get you or your loved one home quickly, allowing you to prepare for your case while maintaining your job and family responsibilities.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":4} -->
<h4>${faq_1_question}</h4>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>${faq_1_answer}</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":4} -->
<h4>${faq_2_question}</h4>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>${faq_2_answer}</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":4} -->
<h4>${faq_3_question}</h4>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>${faq_3_answer}</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":4} -->
<h4>${faq_4_question}</h4>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>${faq_4_answer}</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":4} -->
<h4>${faq_5_question}</h4>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>${faq_5_answer}</p>
<!-- /wp:paragraph -->
"""

def load_state_data(state_name):
    """Load state data from JSON file"""
    filename = os.path.join(STATE_DATA_DIR, f"{state_name.lower().replace(' ', '_')}.json")
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Data file for {state_name} not found at {filename}")
        return None

def generate_page_content(state_data):
    """Generate page content using the template and state data"""
    if not state_data:
        return None
    
    # Prepare template variables
    template_vars = {
        "state_name": state_data["name"],
        "state_nickname": state_data["nickname"],
        "state_heritage": "Native American" if random.random() < 0.5 else "diverse cultural",
        "state_population": state_data["population"],
        "state_counties": str(state_data["num_counties"]),
        "major_city_1": state_data["major_cities"][0] if len(state_data["major_cities"]) > 0 else f"{state_data['name']} City",
        "major_city_2": state_data["major_cities"][1] if len(state_data["major_cities"]) > 1 else "other urban centers",
        "economic_info": state_data["economic_info"],
        "bail_system_info": state_data["bail_system_info"],
        "criminal_justice_info": state_data["criminal_justice_info"],
        "geographical_info": state_data["geographical_info"],
        "weather_info": state_data["weather_info"],
        "county_1_name": state_data["largest_counties"][0] if len(state_data["largest_counties"]) > 0 else f"{state_data['name']} County",
        "county_2_name": state_data["largest_counties"][1] if len(state_data["largest_counties"]) > 1 else f"Central {state_data['name']} County",
        "county_3_name": state_data["largest_counties"][2] if len(state_data["largest_counties"]) > 2 else f"Eastern {state_data['name']} County",
    }
    
    # Add FAQ content
    for i, faq in enumerate(state_data["faqs"][:5], 1):
        template_vars[f"faq_{i}_question"] = faq["question"]
        template_vars[f"faq_{i}_answer"] = faq["answer"]
    
    # Fill in the template
    template = Template(STATE_PAGE_TEMPLATE)
    return template.substitute(template_vars)

def generate_page_for_state(state_name):
    """Generate a complete page for a specific state"""
    print(f"Generating page for {state_name}...")
    
    # Load state data
    state_data = load_state_data(state_name)
    if not state_data:
        print(f"Failed to generate page for {state_name}: No data available")
        return False
    
    # Generate page content
    content = generate_page_content(state_data)
    if not content:
        print(f"Failed to generate page for {state_name}: Content generation error")
        return False
    
    # Save to file
    filename = os.path.join(GENERATED_PAGES_DIR, f"{state_name.lower().replace(' ', '_')}.html")
    with open(filename, 'w') as f:
        f.write(content)
    
    print(f"Page for {state_name} generated successfully and saved to {filename}")
    return True

def generate_all_state_pages():
    """Generate pages for all 50 states"""
    print("Starting page generation for all states...")
    
    # Get list of all state data files
    state_files = [f for f in os.listdir(STATE_DATA_DIR) if f.endswith('.json') and f != 'all_states.json']
    
    success_count = 0
    failure_count = 0
    
    for state_file in state_files:
        state_name = state_file.replace('.json', '').replace('_', ' ').title()
        if generate_page_for_state(state_name):
            success_count += 1
        else:
            failure_count += 1
    
    print(f"Page generation complete: {success_count} successful, {failure_count} failed")

def generate_wordpress_import_file():
    """Generate a WordPress import file containing all state pages"""
    print("Generating WordPress import file...")
    
    # This would be implemented based on WordPress import format requirements
    # For now, we'll just create a simple index file
    
    state_files = [f for f in os.listdir(GENERATED_PAGES_DIR) if f.endswith('.html')]
    
    index_content = "# Bail Bonds Buddy State Pages\n\n"
    index_content += "The following state pages have been generated:\n\n"
    
    for state_file in sorted(state_files):
        state_name = state_file.replace('.html', '').replace('_', ' ').title()
        index_content += f"- [{state_name}]({state_file})\n"
    
    with open(os.path.join(GENERATED_PAGES_DIR, "index.md"), 'w') as f:
        f.write(index_content)
    
    print(f"WordPress import index created at {os.path.join(GENERATED_PAGES_DIR, 'index.md')}")

def main():
    """Main function to run the page generator"""
    # Check if state data exists
    if not os.path.exists(STATE_DATA_DIR):
        print("State data directory not found. Please run state_data_gatherer.py first.")
        return
    
    # Generate pages for all states
    generate_all_state_pages()
    
    # Generate WordPress import file
    generate_wordpress_import_file()
    
    print("Page generation process complete!")

if __name__ == "__main__":
    main()
