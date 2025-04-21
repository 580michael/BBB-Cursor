import os
import re
import json
import random
import sys
import argparse
from content_generator_utils import ContentGeneratorUtils as utils

# Create output directory if it doesn't exist
os.makedirs("/home/ubuntu/bailbonds/generated_pages", exist_ok=True)
os.makedirs("/home/ubuntu/bailbonds/state_data", exist_ok=True)

# Function to load the Oklahoma template JSON
def load_oklahoma_template():
    """Load the Oklahoma template JSON file"""
    template_path = "/home/ubuntu/upload/Oklahoma Bail Bondsman Emergency 24_7 Service.json"
    try:
        with open(template_path, 'r') as f:
            template_json = json.load(f)
        print(f"Oklahoma template loaded successfully")
        return template_json
    except Exception as e:
        print(f"Error loading Oklahoma template: {e}")
        return None

# Function to replace state-specific content in the template
def replace_state_content(template_json, state_data):
    """Replace Oklahoma-specific content with content for the target state"""
    try:
        # Create a deep copy of the template
        data = json.loads(json.dumps(template_json))
        
        # Get state name and nickname
        state_name = state_data['name']
        
        # Replace all instances of "Oklahoma" with the target state name
        for key, value in data.items():
            if not isinstance(value, str):
                continue
                
            # Replace state name
            value = re.sub(r'\bOklahoma\b', state_name, value)
            value = re.sub(r'\bOK\b', state_data['abbreviation'], value)
            value = re.sub(r'\bSooner State\b', state_data['nickname'], value)
            
            # Replace county names
            value = re.sub(r'\bOklahoma County\b', state_data['largest_counties'][0] if len(state_data['largest_counties']) > 0 else f"{state_name} County", value)
            value = re.sub(r'\bTulsa County\b', state_data['largest_counties'][1] if len(state_data['largest_counties']) > 1 else f"Central {state_name} County", value)
            value = re.sub(r'\bCleveland County\b', state_data['largest_counties'][2] if len(state_data['largest_counties']) > 2 else f"Eastern {state_name} County", value)
            
            # Replace city names
            if len(state_data['major_cities']) > 0:
                value = re.sub(r'\bOklahoma City\b', state_data['major_cities'][0] if len(state_data['major_cities']) > 0 else state_name + ' City', value)
            if len(state_data['major_cities']) > 1:
                value = re.sub(r'\bTulsa\b', state_data['major_cities'][1], value)
            
            # Update the value in the data dictionary
            data[key] = value
    
        # Replace "Find Local Bail Bondsmen Near You" with "Find Local [STATE] Bail Bondsmen Near You"
        for key, value in data.items():
            if isinstance(value, str) and "Find Local Bail Bondsmen Near You" in value:
                data[key] = value.replace("Find Local Bail Bondsmen Near You", f"Find Local {state_name} Bail Bondsmen Near You")
        
        # Replace "Find Licensed Bail Bond Agents Nationwide Available Now" with "Find Licensed [STATE] Bail Bond Agents Available Now"
        for key, value in data.items():
            if isinstance(value, str) and "Find Licensed Bail Bond Agents Nationwide Available Now" in value:
                data[key] = value.replace("Find Licensed Bail Bond Agents Nationwide Available Now", f"Find Licensed {state_name} Bail Bond Agents Available Now")
        
        # Replace "Your Guide to Finding Local Bail Bondsmen Anywhere" with "Your Guide to Finding Local [STATE] Bail Bondsmen"
        for key, value in data.items():
            if isinstance(value, str) and "Your Guide to Finding Local Bail Bondsmen Anywhere" in value:
                data[key] = value.replace("Your Guide to Finding Local Bail Bondsmen Anywhere", f"Your Guide to Finding Local {state_name} Bail Bondsmen")
        
        # Replace "Major Counties in Oklahoma" with "Major Counties in [STATE]"
        for key, value in data.items():
            if isinstance(value, str) and "Major Counties in Oklahoma" in value:
                data[key] = value.replace("Major Counties in Oklahoma", f"Major Counties in {state_name}")
        
        # Replace "Oklahoma: The Sooner State" with "[STATE]: The [NICKNAME]"
        for key, value in data.items():
            if isinstance(value, str) and "Oklahoma: The Sooner State" in value:
                # Replace the state description section
                state_section = f"{state_name}: The {state_data['nickname']}\n\n"
                state_section += f"{state_name}, known as the {state_data['nickname']}, combines rich Native American heritage, pioneering spirit, and modern economic growth across its diverse landscape. With a population of approximately {state_data['population']} residents spread throughout {state_data['num_counties']} counties, {state_name} presents unique challenges and opportunities within its criminal justice system.\n\n"
                state_section += f"The state's largest metropolitan areas – {state_data['major_cities'][0] if len(state_data['major_cities']) > 0 else state_name + ' City'} and {state_data['major_cities'][1] if len(state_data['major_cities']) > 1 else 'other urban centers'} – account for the highest concentration of arrests and bail needs, but {state_name}'s extensive rural communities also require specialized bail bond services. {state_name}'s county jail system operates under state supervision while maintaining individual county administration, creating a patchwork of procedures that experienced bail bondsmen must navigate daily.\n\n"
                state_section += f"{state_data['economic_info']}\n\n"
                state_section += f"{state_data['bail_system_info']}\n\n"
                state_section += f"{state_data['criminal_justice_info']}\n\n"
                state_section += f"{state_data['geographical_info']}\n\n"
                state_section += f"{state_data['weather_info']}\n\n"
                state_section += f"For families seeking to secure a loved one's release from any of {state_name}'s detention facilities, working with a {state_name}-based bail bondsman who understands the state's unique characteristics provides the most efficient path to reunion and beginning the next steps in the legal process."
                
                data[key] = value.replace("Oklahoma: The Sooner State", state_section)
        
        # Replace the FAQ sections with unique questions and answers
        faq_questions = utils.generate_unique_faq_questions(state_name)
        faq_answers = [utils.generate_unique_faq_answer(q, state_name) for q in faq_questions[:5]]
        
        # Replace FAQ 1
        for key, value in data.items():
            if isinstance(value, str) and "How long does it take to get released using a bail bond?" in value:
                data[key] = value.replace("How long does it take to get released using a bail bond?", faq_questions[0] if len(faq_questions) > 0 else "How long does it take to get released using a bail bond?")
        
        for key, value in data.items():
            if isinstance(value, str) and "After a bail bond is posted, release times typically range from 2-8 hours depending on the facility's processing speed and how busy they are. Weekend and holiday arrests may take longer to process. The bondsman will keep you updated on the progress." in value:
                data[key] = value.replace("After a bail bond is posted, release times typically range from 2-8 hours depending on the facility's processing speed and how busy they are. Weekend and holiday arrests may take longer to process. The bondsman will keep you updated on the progress.", faq_answers[0] if len(faq_answers) > 0 else "This varies by county.")
        
        # Replace FAQ 2
        for key, value in data.items():
            if isinstance(value, str) and "What kind of collateral is accepted for bail bonds?" in value:
                data[key] = value.replace("What kind of collateral is accepted for bail bonds?", faq_questions[1] if len(faq_questions) > 1 else "What kind of collateral is accepted for bail bonds?")
        
        # Replace FAQ 3
        for key, value in data.items():
            if isinstance(value, str) and "What is the typical cost of a bail bond?" in value:
                data[key] = value.replace("What is the typical cost of a bail bond?", faq_questions[2] if len(faq_questions) > 2 else "What is the typical cost of a bail bond?")
        
        # Replace FAQ 4
        for key, value in data.items():
            if isinstance(value, str) and "What information do I need when contacting a bail bondsman?" in value:
                data[key] = value.replace("What information do I need when contacting a bail bondsman?", faq_questions[3] if len(faq_questions) > 3 else "What information do I need when contacting a bail bondsman?")
        
        # Replace FAQ 5
        for key, value in data.items():
            if isinstance(value, str) and "What types of payments do bail bondsmen accept?" in value:
                data[key] = value.replace("What types of payments do bail bondsmen accept?", faq_questions[4] if len(faq_questions) > 4 else "What types of payments do bail bondsmen accept?")
        
        # Replace the paragraphs under the map with unique content
        intro_paragraph = utils.generate_unique_intro_paragraph(state_name)
        for key, value in data.items():
            if isinstance(value, str) and "We understand that finding a reliable bail bondsman can be stressful" in value:
                data[key] = value.replace("We understand that finding a reliable bail bondsman can be stressful, especially in urgent situations. BailBondsBuddy.com simplifies the process by connecting you with trusted bail bond professionals in your local area who understand local laws and court requirements. Our network of licensed agents provides immediate assistance when you need it most, helping your loved ones return home quickly and safely.", intro_paragraph)
        
        # Replace the "Every hour spent in jail" paragraph with unique content
        arrest_paragraph = utils.generate_unique_arrest_paragraph(state_name)
        for key, value in data.items():
            if isinstance(value, str) and "Every hour spent in jail can impact someone's life significantly" in value:
                data[key] = value.replace("Every hour spent in jail can impact someone's life significantly - missed work shifts that risk employment, family responsibilities left unattended, and the emotional toll of confinement. Quick release means getting back to work, caring for family, and maintaining stability during a difficult time. Our trusted bail bondsmen prioritize swift action because they understand that restoring normalcy is about more than just freedom - it's about protecting livelihoods, reputations, and peace of mind when it matters most.", arrest_paragraph)
        
        # Replace the 24/7 Availability section with unique content
        availability_content = utils.generate_unique_availability_content(state_name)
        for key, value in data.items():
            if isinstance(value, str) and "Emergency bail bond services available any time, day or night, when you need help the most. Our bail agents answer calls around the clock and can immediately begin the release process, even on weekends and holidays. Don't wait until morning - get help now." in value:
                data[key] = value.replace("Emergency bail bond services available any time, day or night, when you need help the most. Our bail agents answer calls around the clock and can immediately begin the release process, even on weekends and holidays. Don't wait until morning - get help now.", availability_content)
        
        # Replace the Verified Bondsman section with unique content
        verified_content = utils.generate_unique_verified_content(state_name)
        for key, value in data.items():
            if isinstance(value, str) and "Emergency bail bond services available from pre-screened, licensed professionals who meet our strict standards. Each verified bondsman in our network is fully licensed, insured, and has a proven track record of reliable service and ethical business practices." in value:
                data[key] = value.replace("Emergency bail bond services available from pre-screened, licensed professionals who meet our strict standards. Each verified bondsman in our network is fully licensed, insured, and has a proven track record of reliable service and ethical business practices.", verified_content)
        
        # Replace the Nationwide Coverage section with unique content
        coverage_content = utils.generate_unique_coverage_content(state_name)
        for key, value in data.items():
            if isinstance(value, str) and "From small towns to major cities, find bail bondsmen across all 50 states. Our extensive network ensures coverage throughout America, from the largest county detention centers to the smallest municipal jails, giving you immediate access to local expertise wherever you need it." in value:
                data[key] = value.replace("From small towns to major cities, find bail bondsmen across all 50 states. Our extensive network ensures coverage throughout America, from the largest county detention centers to the smallest municipal jails, giving you immediate access to local expertise wherever you need it.", coverage_content)
        
        # Replace the "When you or a loved one is arrested" paragraph with unique content
        network_paragraph = utils.generate_unique_network_paragraph(state_name)
        for key, value in data.items():
            if isinstance(value, str) and "When you or a loved one is arrested, time is of the essence. The jail system can be overwhelming and confusing, especially during such a stressful time. That's why connecting with a local bail bondsman immediately is crucial - they understand the specific procedures of your county jail, have established relationships with local law enforcement, and can navigate the release process efficiently. A local bondsman from your community knows exactly how to expedite paperwork through the local court system, potentially reducing jail time from days to just hours." in value:
                data[key] = value.replace("When you or a loved one is arrested, time is of the essence. The jail system can be overwhelming and confusing, especially during such a stressful time. That's why connecting with a local bail bondsman immediately is crucial - they understand the specific procedures of your county jail, have established relationships with local law enforcement, and can navigate the release process efficiently. A local bondsman from your community knows exactly how to expedite paperwork through the local court system, potentially reducing jail time from days to just hours.", network_paragraph)
        
        # Replace the "BailBondsBuddy.com gives you instant access" paragraph with unique content
        for key, value in data.items():
            if isinstance(value, str) and "BailBondsBuddy.com gives you instant access to trusted bondsmen throughout America, from small towns to major cities. Our network of licensed professionals offers 24/7 service, affordable payment plans, and complete confidentiality. They can explain local specific bail laws and requirements in plain language, help with paperwork, and even provide transportation from jail when needed. Don't waste precious time behind bars - use our simple search tool to find a local bondsman in your area who can get you or your loved one home quickly, allowing you to prepare for your case while maintaining your job and family responsibilities." in value:
                data[key] = value.replace("BailBondsBuddy.com gives you instant access to trusted bondsmen throughout America, from small towns to major cities. Our network of licensed professionals offers 24/7 service, affordable payment plans, and complete confidentiality. They can explain local specific bail laws and requirements in plain language, help with paperwork, and even provide transportation from jail when needed. Don't waste precious time behind bars - use our simple search tool to find a local bondsman in your area who can get you or your loved one home quickly, allowing you to prepare for your case while maintaining your job and family responsibilities.", utils.generate_unique_bailbondsbuddy_paragraph(state_name))
        
        return data
    except Exception as e:
        print(f"Error replacing state content: {e}")
        return None

# Function to generate a page for a specific state
def generate_page_for_state(state_name, template_json):
    """Generate a page for a specific state"""
    try:
        # Load state data
        state_data_path = f"/home/ubuntu/bailbonds/state_data/{state_name.lower().replace(' ', '_')}.json"
        with open(state_data_path, 'r') as f:
            state_data = json.load(f)
        
        # Replace state content in the template
        modified_json = replace_state_content(template_json, state_data)
        if not modified_json:
            print(f"Failed to generate page for {state_name}: Content replacement error")
            return False
        
        # Save to JSON file
        os.makedirs("/home/ubuntu/bailbonds/generated_pages", exist_ok=True)
        json_filename = f"/home/ubuntu/bailbonds/generated_pages/{state_name.lower().replace(' ', '_')}.json"
        with open(json_filename, 'w') as f:
            json.dump(modified_json, f, indent=2)
        
        # Also save as HTML for easy viewing
        html_content = generate_html_preview(state_name, state_data, modified_json)
        html_filename = f"/home/ubuntu/bailbonds/generated_pages/{state_name.lower().replace(' ', '_')}.html"
        with open(html_filename, 'w') as f:
            f.write(html_content)
        
        print(f"Page for {state_name} generated successfully and saved to:")
        print(f"  - JSON: {json_filename}")
        print(f"  - HTML: {html_filename}")
        
        return True
    except Exception as e:
        print(f"Error generating page for {state_name}: {e}")
        return False

# Function to generate sample state data for testing
def generate_sample_state_data():
    """Generate sample state data for Texas"""
    state_name = "Texas"
    print(f"Generating sample data for {state_name}...")
    
    state_data = {
        "name": "Texas",
        "nickname": "Lone Star State",
        "abbreviation": "TX",
        "population": "29 million",
        "num_counties": "254",
        "largest_counties": ["Harris County", "Dallas County", "Tarrant County"],
        "major_cities": ["Houston", "Dallas", "San Antonio", "Austin", "Fort Worth"],
        "economic_info": "Texas's economy has traditionally centered around energy production and technology, with oil and natural gas remaining significant industries. However, recent economic diversification has expanded into aerospace, biotechnology, telecommunications, and healthcare. This economic evolution has affected crime patterns and bail requirements throughout the state, with growing urban centers experiencing different needs than rural communities.",
        "bail_system_info": "The state maintains a robust bail system governed by the Texas Occupations Code Chapter 1704 (Bail Bond Sureties), which requires all bondsmen to be licensed through the Texas Department of Insurance. Texas law establishes standard premium rates (typically 10% of the bail amount) and regulates bondsman practices to protect consumers during vulnerable times.",
        "criminal_justice_info": "Recent criminal justice reform initiatives in Texas have aimed to reduce the state's historically high incarceration rate, which has long ranked among the nation's highest. These reforms have modified certain bail procedures, especially for non-violent offenses, making professional guidance from experienced bondsmen even more valuable for navigating the changing legal landscape.",
        "geographical_info": "Texas's geographical positioning along major interstate highways (I-35, I-10, and I-45) has unfortunately made it a corridor for drug trafficking, resulting in significant numbers of drug-related arrests requiring bail services. Meanwhile, the state's diverse population - including substantial Hispanic and African American communities - introduces jurisdictional complexities that knowledgeable bail bondsmen must understand.",
        "weather_info": "Weather emergencies, from hurricanes along the Gulf Coast to flooding in central regions, can occasionally impact court schedules and bail processing timelines. Local bondsmen familiar with Texas's systems know how to manage these disruptions while ensuring clients meet all legal obligations."
    }
    
    # Save to file
    os.makedirs("/home/ubuntu/bailbonds/state_data", exist_ok=True)
    state_data_path = f"/home/ubuntu/bailbonds/state_data/{state_name.lower().replace(' ', '_')}.json"
    with open(state_data_path, 'w') as f:
        json.dump(state_data, f, indent=2)
    
    print(f"Sample data for {state_name} saved to {state_data_path}")

# Function to generate HTML preview of the page
def generate_html_preview(state_name, state_data, json_data):
    """Generate an HTML preview of the page for easy viewing"""
    html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{state_name} Bail Bondsman Emergency 24/7 Service | BailBondsBuddy.com</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 0;
            color: #333;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        header {{
            background-color: #f8f8f8;
            padding: 20px;
            text-align: center;
        }}
        .hero {{
            background-color: #2980b9;
            color: white;
            padding: 40px 20px;
            display: flex;
            justify-content: space-between;
        }}
        .hero-content {{
            flex: 1;
            padding-right: 20px;
        }}
        .hero-image {{
            flex: 1;
            background-color: #f8f8f8;
            border-radius: 5px;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .search-box {{
            background-color: white;
            padding: 20px;
            border-radius: 5px;
            margin-top: 20px;
        }}
        .search-input {{
            width: 100%;
            padding: 10px;
            margin-bottom: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
        }}
        .search-button {{
            width: 100%;
            padding: 10px;
            background-color: #2980b9;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }}
        .map {{
            height: 300px;
            background-color: #f8f8f8;
            margin: 20px 0;
            border-radius: 5px;
        }}
        .content {{
            padding: 20px;
        }}
        .features {{
            display: flex;
            justify-content: space-between;
            margin: 40px 0;
        }}
        .feature {{
            flex: 1;
            text-align: center;
            padding: 20px;
        }}
        .feature-icon {{
            font-size: 48px;
            color: #2980b9;
        }}
        .counties {{
            display: flex;
            justify-content: space-between;
            margin: 40px 0;
        }}
        .county {{
            flex: 1;
            padding: 20px;
            text-align: center;
        }}
        .faq {{
            margin: 40px 0;
        }}
        .faq-item {{
            margin-bottom: 20px;
            padding: 20px;
            background-color: #f8f8f8;
            border-radius: 5px;
        }}
        .faq-question {{
            font-weight: bold;
            margin-bottom: 10px;
        }}
        footer {{
            background-color: #333;
            color: white;
            padding: 20px;
            text-align: center;
        }}
    </style>
</head>
<body>
    <header>
        <h1>{state_name} Bail Bondsman Emergency 24/7 Service | BailBondsBuddy.com</h1>
    </header>
    
    <div class="hero">
        <div class="hero-content">
            <h2>Find Local {state_name} Bail Bondsmen Near You</h2>
            <h3>24/7 Jail Release Services</h3>
            <p>Find Licensed {state_name} Bail Bond Agents Available Now</p>
        </div>
        <div class="hero-image">
            <div class="map">
                [Map of {state_name} would be displayed here]
            </div>
        </div>
    </div>
    
    <div class="container">
        <div class="search-box">
            <input type="text" class="search-input" placeholder="Search any City State Here... Dallas TX   Chicago IL   San Diego CA   Enter Your Location Here">
            <button class="search-button">Find Bail Bondsmen</button>
        </div>
        
        <div class="content">
            <h2>Your Guide to Finding Local {state_name} Bail Bondsmen</h2>
            <p>Find trusted bail bondsmen in your area, available 24/7.</p>
            
            <p>{intro_paragraph}</p>
            
            <div class="features">
                <div class="feature">
                    <div class="feature-icon">⏰</div>
                    <h3>24/7 Availability</h3>
                    <p>{availability_content}</p>
                </div>
                <div class="feature">
                    <div class="feature-icon">✓</div>
                    <h3>Verified Bondsman</h3>
                    <p>{verified_content}</p>
                </div>
                <div class="feature">
                    <div class="feature-icon">🗺️</div>
                    <h3>Nationwide Coverage</h3>
                    <p>{coverage_content}</p>
                </div>
            </div>
            
            <h2>{state_name}: The {state_nickname}</h2>
            <p>{state_description}</p>
            <p>{metro_description}</p>
            <p>{economic_info}</p>
            <p>{bail_system_info}</p>
            <p>{criminal_justice_info}</p>
            <p>{geographical_info}</p>
            
            <h2>Major Counties in {state_name}</h2>
            <div class="counties">
                <div class="county">
                    <h3>{county_1}</h3>
                </div>
                <div class="county">
                    <h3>{county_2}</h3>
                </div>
                <div class="county">
                    <h3>{county_3}</h3>
                </div>
            </div>
            
            <p>{arrest_paragraph}</p>
            <p>{network_paragraph}</p>
            
            <div class="search-box">
                <input type="text" class="search-input" placeholder="Search any City State Here... Dallas TX   Chicago IL   San Diego CA   Enter Your Location Here">
                <button class="search-button">Find Bail Bondsmen</button>
            </div>
            
            <div class="faq">
                <div class="faq-item">
                    <div class="faq-question">{faq_1_question}</div>
                    <div class="faq-answer">{faq_1_answer}</div>
                </div>
                <div class="faq-item">
                    <div class="faq-question">{faq_2_question}</div>
                    <div class="faq-answer">{faq_2_answer}</div>
                </div>
                <div class="faq-item">
                    <div class="faq-question">{faq_3_question}</div>
                    <div class="faq-answer">{faq_3_answer}</div>
                </div>
                <div class="faq-item">
                    <div class="faq-question">{faq_4_question}</div>
                    <div class="faq-answer">{faq_4_answer}</div>
                </div>
                <div class="faq-item">
                    <div class="faq-question">{faq_5_question}</div>
                    <div class="faq-answer">{faq_5_answer}</div>
                </div>
            </div>
        </div>
    </div>
    
    <footer>
        <p>&copy; 2025 BailBondsBuddy.com - Your Trusted Guide to Finding Local Bail Bondsmen</p>
    </footer>
</body>
</html>
"""
    
    # Extract content for HTML preview
    intro_paragraph = utils.generate_unique_intro_paragraph(state_name)
    availability_content = utils.generate_unique_availability_content(state_name)
    verified_content = utils.generate_unique_verified_content(state_name)
    coverage_content = utils.generate_unique_coverage_content(state_name)
    arrest_paragraph = utils.generate_unique_arrest_paragraph(state_name)
    network_paragraph = utils.generate_unique_network_paragraph(state_name)
    
    # Extract FAQ questions and answers
    faq_questions = utils.generate_unique_faq_questions(state_name)
    faq_answers = [utils.generate_unique_faq_answer(q, state_name) for q in faq_questions[:5]]
    
    # Fill in the HTML template
    html_content = html_template.format(
        state_name=state_name,
        state_nickname=state_data['nickname'],
        intro_paragraph=intro_paragraph,
        availability_content=availability_content,
        verified_content=verified_content,
        coverage_content=coverage_content,
        state_description=f"{state_name}, known as the {state_data['nickname']}, combines rich Native American heritage, pioneering spirit, and modern economic growth across its diverse landscape. With a population of approximately {state_data['population']} residents spread throughout {state_data['num_counties']} counties, {state_name} presents unique challenges and opportunities within its criminal justice system.",
        metro_description=f"The state's largest metropolitan areas – {state_data['major_cities'][0] if len(state_data['major_cities']) > 0 else state_name + ' City'} and {state_data['major_cities'][1] if len(state_data['major_cities']) > 1 else 'other urban centers'} – account for the highest concentration of arrests and bail needs, but {state_name}'s extensive rural communities also require specialized bail bond services. {state_name}'s county jail system operates under state supervision while maintaining individual county administration, creating a patchwork of procedures that experienced bail bondsmen must navigate daily.",
        economic_info=state_data['economic_info'],
        bail_system_info=state_data['bail_system_info'],
        criminal_justice_info=state_data['criminal_justice_info'],
        geographical_info=state_data['geographical_info'],
        weather_info=state_data.get('weather_info', ''),
        county_1=state_data['largest_counties'][0] if len(state_data['largest_counties']) > 0 else f"{state_name} County",
        county_2=state_data['largest_counties'][1] if len(state_data['largest_counties']) > 1 else f"Central {state_name} County",
        county_3=state_data['largest_counties'][2] if len(state_data['largest_counties']) > 2 else f"Eastern {state_name} County",
        arrest_paragraph=arrest_paragraph,
        network_paragraph=network_paragraph,
        faq_1_question=faq_questions[0] if len(faq_questions) > 0 else "How long does it take to get released using a bail bond?",
        faq_1_answer=faq_answers[0] if len(faq_answers) > 0 else "This varies by county.",
        faq_2_question=faq_questions[1] if len(faq_questions) > 1 else "What kind of collateral is accepted for bail bonds?",
        faq_2_answer=faq_answers[1] if len(faq_answers) > 1 else "This varies by bondsman.",
        faq_3_question=faq_questions[2] if len(faq_questions) > 2 else "What is the typical cost of a bail bond?",
        faq_3_answer=faq_answers[2] if len(faq_answers) > 2 else "This varies by state.",
        faq_4_question=faq_questions[3] if len(faq_questions) > 3 else "What information do I need when contacting a bail bondsman?",
        faq_4_answer=faq_answers[3] if len(faq_answers) > 3 else "This varies by situation.",
        faq_5_question=faq_questions[4] if len(faq_questions) > 4 else "What types of payments do bail bondsmen accept?",
        faq_5_answer=faq_answers[4] if len(faq_answers) > 4 else "This varies by bondsman."
    )
    
    return html_content

# Function to generate a sample state for testing
def generate_sample_state():
    """Generate a sample state for testing"""
    return {
        "name": "Texas",
        "nickname": "Lone Star State",
        "abbreviation": "TX",
        "population": "29 million",
        "num_counties": "254",
        "largest_counties": ["Harris County", "Dallas County", "Tarrant County"],
        "major_cities": ["Houston", "Dallas", "San Antonio", "Austin", "Fort Worth"],
        "economic_info": "Texas's economy has traditionally centered around energy production and technology, with oil and natural gas remaining significant industries. However, recent economic diversification has expanded into aerospace, biotechnology, telecommunications, and healthcare. This economic evolution has affected crime patterns and bail requirements throughout the state, with growing urban centers experiencing different needs than rural communities.",
        "bail_system_info": "The state maintains a robust bail system governed by the Texas Occupations Code Chapter 1704 (Bail Bond Sureties), which requires all bondsmen to be licensed through the Texas Department of Insurance. Texas law establishes standard premium rates (typically 10% of the bail amount) and regulates bondsman practices to protect consumers during vulnerable times.",
        "criminal_justice_info": "Recent criminal justice reform initiatives in Texas have aimed to reduce the state's historically high incarceration rate, which has long ranked among the nation's highest. These reforms have modified certain bail procedures, especially for non-violent offenses, making professional guidance from experienced bondsmen even more valuable for navigating the changing legal landscape.",
        "geographical_info": "Texas's geographical positioning along major interstate highways (I-35, I-10, and I-45) has unfortunately made it a corridor for drug trafficking, resulting in significant numbers of drug-related arrests requiring bail services. Meanwhile, the state's diverse population - including substantial Hispanic and African American communities - introduces jurisdictional complexities that knowledgeable bail bondsmen must understand.",
        "weather_info": "Weather emergencies, from hurricanes along the Gulf Coast to flooding in central regions, can occasionally impact court schedules and bail processing timelines. Local bondsmen familiar with Texas's systems know how to manage these disruptions while ensuring clients meet all legal obligations."
    }

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
    state_files = [f for f in os.listdir(state_data_dir) if f.endswith('.json')]
    
    # Generate pages for each state
    success_count = 0
    for state_file in state_files:
        state_name = state_file.replace('.json', '').replace('_', ' ').title()
        print(f"Generating page for {state_name}...")
        if generate_page_for_state(state_name, template_json):
            success_count += 1
    
    print(f"Page generation complete! Successfully generated {success_count} out of {len(state_files)} state pages.")
    return success_count == len(state_files)

# Main function
if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Generate bail bondsman pages for all 50 states')
    parser.add_argument('--test', action='store_true', help='Test the script with a sample state (Texas)')
    parser.add_argument('--all', action='store_true', help='Generate pages for all 50 states')
    args = parser.parse_args()
    
    # Create output directories
    os.makedirs("/home/ubuntu/bailbonds/generated_pages", exist_ok=True)
    os.makedirs("/home/ubuntu/bailbonds/state_data", exist_ok=True)
    
    if args.test:
        test_with_sample_state()
    elif args.all:
        generate_all_state_pages()
    else:
        print("Please specify either --test or --all")
        print("  --test: Test the script with a sample state (Texas)")
        print("  --all: Generate pages for all 50 states")
