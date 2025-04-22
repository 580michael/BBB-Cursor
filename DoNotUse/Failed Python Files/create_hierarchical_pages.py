import requests
import random
import time
from urllib.parse import quote

# Constants
BASE_URL = "https://bailbondsbuddy.com"
TEMPLATE_PAGE_ID = 501  # Main template page ID
AUTH = ('bbbuddy', 'DpSm eiz8 yHjx Sqqk G3lG fqU6')

# State data with counties and cities
STATE_DATA = {
    "Oklahoma": {
        "abbreviation": "OK",
        "capital": {
            "name": "Oklahoma City",
            "address": "Oklahoma City, OK, USA",
            "lat": "35.4688692",
            "lng": "-97.519539"
        },
        "counties": {
            "Oklahoma County": {
                "county_seat": "Oklahoma City",
                "address": "Oklahoma City, OK, USA",
                "lat": "35.4688692",
                "lng": "-97.519539",
                "cities": ["Oklahoma City", "Edmond", "Midwest City"]
            },
            "Tulsa County": {
                "county_seat": "Tulsa",
                "address": "Tulsa, OK, USA",
                "lat": "36.1540",
                "lng": "-95.9928",
                "cities": ["Tulsa", "Broken Arrow", "Bixby"]
            },
            "Cleveland County": {
                "county_seat": "Norman",
                "address": "Norman, OK, USA",
                "lat": "35.2226",
                "lng": "-97.4395",
                "cities": ["Norman", "Moore", "Noble"]
            }
        }
    },
    "Texas": {
        "abbreviation": "TX",
        "capital": {
            "name": "Austin",
            "address": "Austin, TX, USA",
            "lat": "30.2672",
            "lng": "-97.7431"
        },
        "counties": {
            "Harris County": {
                "county_seat": "Houston",
                "address": "Houston, TX, USA",
                "lat": "29.7604",
                "lng": "-95.3698",
                "cities": ["Houston", "Pasadena", "Katy"]
            },
            "Dallas County": {
                "county_seat": "Dallas",
                "address": "Dallas, TX, USA",
                "lat": "32.7767",
                "lng": "-96.7970",
                "cities": ["Dallas", "Irving", "Garland"]
            },
            "Bexar County": {
                "county_seat": "San Antonio",
                "address": "San Antonio, TX, USA",
                "lat": "29.4252",
                "lng": "-98.4946",
                "cities": ["San Antonio", "Converse", "Helotes"]
            }
        }
    },
    "Florida": {
        "abbreviation": "FL",
        "capital": {
            "name": "Tallahassee",
            "address": "Tallahassee, FL, USA",
            "lat": "30.4383",
            "lng": "-84.2807"
        },
        "counties": {
            "Miami-Dade County": {
                "county_seat": "Miami",
                "address": "Miami, FL, USA",
                "lat": "25.7617",
                "lng": "-80.1918",
                "cities": ["Miami", "Miami Beach", "Coral Gables"]
            },
            "Broward County": {
                "county_seat": "Fort Lauderdale",
                "address": "Fort Lauderdale, FL, USA",
                "lat": "26.1224",
                "lng": "-80.1373",
                "cities": ["Fort Lauderdale", "Hollywood", "Pompano Beach"]
            },
            "Orange County": {
                "county_seat": "Orlando",
                "address": "Orlando, FL, USA",
                "lat": "28.5383",
                "lng": "-81.3792",
                "cities": ["Orlando", "Winter Park", "Maitland"]
            }
        }
    }
}

# Keyword data
KEYWORDS = [
    "Bail-Bonds", "Bondsman", "Bail-Bondsman", "Bail-Bond-Agent", 
    "Bail-Services", "Bail-Bond-Companies"
]

MODIFIERS = [
    "24-Hour", "Licensed", "Professional", "Local", "Reliable", 
    "Fast", "Affordable"
]

def select_keywords():
    """Randomly select a keyword and modifier combination"""
    keyword = random.choice(KEYWORDS)
    modifier = random.choice(MODIFIERS)
    return {
        "modifier": modifier,
        "keyword": keyword
    }

def format_title(keyword_data, location):
    """Format page title with proper connecting words"""
    modifier = keyword_data["modifier"]
    keyword = keyword_data["keyword"]
    
    if keyword.startswith("Bail"):
        return f"{modifier} {keyword} in {location}"
    else:
        return f"{modifier} Bail {keyword} in {location}"

def create_slug(keyword_data, location, location_type, state_abbr=None, county_name=None):
    """Create properly formatted slug based on location type"""
    modifier = keyword_data["modifier"].lower().replace(" ", "-")
    keyword = keyword_data["keyword"].lower().replace(" ", "-")
    location_slug = location.lower().replace(" ", "-")
    
    if location_type == "state":
        return f"{modifier}-{keyword}-in-{location_slug}"
    elif location_type == "county":
        county_slug = county_name.lower().replace(" ", "-")
        return f"{state_abbr}/{county_slug}/{modifier}-{keyword}-in-{county_slug}"
    else:  # city
        county_slug = county_name.lower().replace(" ", "-")
        return f"{state_abbr}/{county_slug}/{modifier}-{keyword}-in-{location_slug}"

def create_meta_description(keyword_data, location_type, location, state=None):
    """Create a meta description for the page"""
    modifier = keyword_data["modifier"].lower()
    
    if location_type == "state":
        return f"Find {modifier} bail bond services throughout {location}. Available 24/7 to help with bail in any county."
    elif location_type == "county":
        return f"Need a bail bondsman in {location}, {state}? Connect with {modifier} bail bond agents serving the entire county."
    else:  # city
        return f"Looking for {modifier} bail bondsmen in {location}, {state}? Get immediate assistance from local agents."

def get_template_content():
    """Get the content from the template page."""
    try:
        template_response = requests.get(
            f"{BASE_URL}/wp-json/wp/v2/pages/{TEMPLATE_PAGE_ID}",
            auth=AUTH,
            params={'context': 'edit'}
        )
        template_response.raise_for_status()
        
        template_data = template_response.json()
        content = template_data.get('content', {}).get('raw', '')
        
        if not content:
            raise ValueError("Could not get raw content from template")
            
        return content
    except Exception as e:
        print(f"Error getting template: {str(e)}")
        return None

def create_state_page(state_name, template_content=None):
    """Create a state page that uses the Divi Theme Builder template"""
    try:
        # Get state info
        state_info = STATE_DATA[state_name]
        capital_info = state_info["capital"]
        state_abbr = state_info['abbreviation']
        
        # Get the top 3 counties for this state
        top_counties = list(state_info['counties'].keys())[:3]
        
        # Include full Divi Builder content 
        content = f"""[et_pb_section fb_built="1" _builder_version="4.27.4" _module_preset="default" background_color="rgba(43,135,218,0.78)" use_background_color_gradient="on" background_color_gradient_direction="120deg" background_color_gradient_stops="#2b87da 33%|#002c6b 99%" width="100%" max_width="100%" module_alignment="center" custom_padding="80px|80px|80px|80px|false|false"]
[et_pb_row column_structure="1_2,1_2" _builder_version="4.27.4" _module_preset="default" width="100%" max_width="100%" module_alignment="center" custom_padding="0px|0px|0px|0px"]
[et_pb_column type="1_2" _builder_version="4.27.4" _module_preset="default"]
[et_pb_text _builder_version="4.27.4" _module_preset="default"]

<h1 style="color: white; font-size: 48px; line-height: 1.2em; margin-bottom: 20px;">Find Local Bail Bondsmen in {state_name}</h1>
<p style="color: rgba(255,255,255,0.9); font-size: 18px; margin-bottom: 30px;">Need someone to help? You'll find them here!</p>

[/et_pb_text]
[et_pb_code _builder_version="4.27.4" _module_preset="default"]
<div class="search-container" style="background: white; padding: 20px; border-radius: 8px; box-shadow: 0 4px 20px rgba(0,0,0,0.15);">
  <form action="/search" method="get" class="search-form">
    <input type="text" placeholder="Search for bail bondsmen..." style="width: 100%; padding: 12px; border: 1px solid #eee; border-radius: 4px; margin-bottom: 10px;">
    <input type="text" placeholder="Location" style="width: 100%; padding: 12px; border: 1px solid #eee; border-radius: 4px; margin-bottom: 10px;">
    <button type="submit" style="width: 100%; padding: 12px; background: #2b87da; color: white; border: none; border-radius: 4px; cursor: pointer; font-weight: bold; transition: all 0.3s ease;">Find Bail Bondsmen</button>
  </form>
</div>
[/et_pb_code]
[/et_pb_column]
[et_pb_column type="1_2" _builder_version="4.27.4" _module_preset="default"]
[et_pb_map address="{capital_info['address']}" zoom_level="7" _builder_version="4.27.4" _module_preset="default" hover_enabled="0" border_radii="on|15px|15px|15px|15px" box_shadow_style="preset3" address_lat="{capital_info['lat']}" address_lng="{capital_info['lng']}" sticky_enabled="0"]
[/et_pb_map]
[/et_pb_column]
[/et_pb_row]
[/et_pb_section]

[et_pb_section _builder_version="4.27.4" _module_preset="default" min_height="145.8px" custom_padding="||0px||false|false"]
[et_pb_row _builder_version="4.27.4" _module_preset="default"]
[et_pb_column type="4_4" _builder_version="4.27.4" _module_preset="default"]
[et_pb_text _builder_version="4.27.4" _module_preset="default" header_text_align="center"]

<h2 style="font-size: 32px; margin-bottom: 10px; color: #002c6b; text-align: center;">Your Guide to Finding Local Bail Bondsmen in {state_name}</h2>
<p style="font-size: 20px; color: #666666; margin-bottom: 10px; text-align: center;">Find trusted bail bondsmen in your area, available 24/7.</p>

[/et_pb_text]
[/et_pb_column]
[/et_pb_row]
[/et_pb_section]

[et_pb_section _builder_version="4.27.4" _module_preset="default"]
[et_pb_row column_structure="1_3,1_3,1_3" _builder_version="4.27.4" _module_preset="default"]
[et_pb_column type="1_3" _builder_version="4.27.4" _module_preset="default"]
[et_pb_heading title="Major Counties in {state_name}" _builder_version="4.27.4" _module_preset="default" title_text_align="center"]
[/et_pb_heading]
[/et_pb_column]
[/et_pb_row]

[et_pb_row column_structure="1_3,1_3,1_3" _builder_version="4.27.4" _module_preset="default"]
[et_pb_column type="1_3" _builder_version="4.27.4" _module_preset="default"]
[et_pb_heading title="{top_counties[0]}" _builder_version="4.27.4" _module_preset="default" title_text_align="center"]
[/et_pb_heading]
[et_pb_button button_text="View Bondsman" button_alignment="center" _builder_version="4.27.4" _module_preset="default"]
[/et_pb_button]
[/et_pb_column]
[et_pb_column type="1_3" _builder_version="4.27.4" _module_preset="default"]
[et_pb_heading title="{top_counties[1]}" _builder_version="4.27.4" _module_preset="default" title_text_align="center"]
[/et_pb_heading]
[et_pb_button button_text="View Bondsman" button_alignment="center" _builder_version="4.27.4" _module_preset="default"]
[/et_pb_button]
[/et_pb_column]
[et_pb_column type="1_3" _builder_version="4.27.4" _module_preset="default"]
[et_pb_heading title="{top_counties[2]}" _builder_version="4.27.4" _module_preset="default" title_text_align="center"]
[/et_pb_heading]
[et_pb_button button_text="View Bondsman" button_alignment="center" _builder_version="4.27.4" _module_preset="default"]
[/et_pb_button]
[/et_pb_column]
[/et_pb_row]
[/et_pb_section]
"""
        
        # Select keyword combination
        keyword_data = select_keywords()
        page_title = format_title(keyword_data, state_name)
        page_slug = create_slug(keyword_data, state_name, "state")
        
        # Create the page with full Divi Builder content
        data = {
            'title': page_title,
            'content': content,
            'status': 'publish',
            'slug': page_slug,
            'meta': {
                '_et_pb_use_builder': 'on',
                '_et_pb_old_content': '',
                '_et_gb_content_width': '',
                '_et_pb_post_type_layout': 'et_body_layout',
                '_yoast_wpseo_metadesc': create_meta_description(keyword_data, "state", state_name)
            }
        }
        
        # Send the request
        response = requests.post(
            f"{BASE_URL}/wp-json/wp/v2/pages",
            auth=AUTH,
            json=data
        )
        response.raise_for_status()
        
        page_data = response.json()
        print(f"✓ Created state page: {state_name} (ID: {page_data['id']})")
        print(f"  URL: {page_data['link']}")
        return page_data['id']
        
    except Exception as e:
        print(f"✗ Error creating state page for {state_name}: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"  Response content: {e.response.content}")
        return None

def create_county_page(state_name, county_name, template_content):
    """Create a county page with city links"""
    try:
        # Use our template content
        content = template_content
        
        # Get state and county info
        state_info = STATE_DATA[state_name]
        county_info = state_info['counties'][county_name]
        state_abbr = state_info['abbreviation']
        
        # Replace map address and coordinates
        content = content.replace('[state_capital_address]', county_info['address'])
        content = content.replace('[state_capital_lat]', county_info['lat'])
        content = content.replace('[state_capital_lng]', county_info['lng'])
        
        # Replace county-specific content
        content = content.replace('[state_name]', f"{county_name}, {state_name}")
        content = content.replace('Major Counties', 'Major Cities')
        
        # Select keyword combination
        keyword_data = select_keywords()
        page_title = format_title(keyword_data, f"{county_name}, {state_name}")
        page_slug = create_slug(keyword_data, county_name, "county", state_abbr, county_name)
        
        # Add city list section
        cities_section = f"<h3>Major Cities in {county_name}</h3><ul>"
        for city_name in county_info['cities']:
            cities_section += f"<li>{city_name}</li>"
        cities_section += "</ul>"
        
        # Add the cities section to the content
        content = content.replace('</ul></div></div>', '</ul></div></div>' + cities_section)
        
        # Add link back to state page
        content += f'<p><a href="{BASE_URL}/bail-bonds-in-{state_name.lower()}" target="_blank">View All {state_name} Bail Bond Services</a></p>'
        
        # Create the page
        data = {
            'title': page_title,
            'content': content,
            'status': 'publish',
            'slug': page_slug,
            'meta': {
                '_et_pb_use_builder': 'on',
                '_et_pb_old_content': '',
                '_et_pb_post_type_layout': 'custom_body',
                '_yoast_wpseo_metadesc': create_meta_description(keyword_data, "county", county_name, state_name)
            }
        }
        
        response = requests.post(
            f"{BASE_URL}/wp-json/wp/v2/pages",
            auth=AUTH,
            json=data
        )
        response.raise_for_status()
        
        page_data = response.json()
        print(f"  ✓ Created county page: {county_name} (ID: {page_data['id']})")
        print(f"    URL: {page_data['link']}")
        return page_data['id']
        
    except Exception as e:
        print(f"  ✗ Error creating county page for {county_name}: {str(e)}")
        return None

def create_city_page(state_name, county_name, city_name, template_content):
    """Create a city page"""
    try:
        # Use our template content
        content = template_content
        
        # Get state, county and city info
        state_info = STATE_DATA[state_name]
        county_info = state_info['counties'][county_name]
        state_abbr = state_info['abbreviation']
        
        # For city, we'll use the same coordinates as the county seat
        content = content.replace('[state_capital_address]', county_info['address'])
        content = content.replace('[state_capital_lat]', county_info['lat'])
        content = content.replace('[state_capital_lng]', county_info['lng'])
        
        # Replace city-specific content
        content = content.replace('[state_name]', f"{city_name}, {state_name}")
        content = content.replace('Major Counties', 'Bail Bond Services in ' + city_name)
        
        # Replace counties section with local bail bond services
        bail_services = """
        <h3>Local Bail Bond Services in {city}</h3>
        <p>Looking for bail bond services in {city}? Our network includes trusted bail bondsmen who provide:</p>
        <ul>
            <li>24/7 emergency assistance</li>
            <li>Fast jail release</li>
            <li>Affordable payment options</li>
            <li>Confidential service</li>
            <li>Free consultations</li>
        </ul>
        """.format(city=city_name)
        
        # Add city-specific content
        content = content.replace('</ul></div></div>', '</ul></div></div>' + bail_services)
        
        # Select keyword combination
        keyword_data = select_keywords()
        page_title = format_title(keyword_data, f"{city_name}, {state_name}")
        page_slug = create_slug(keyword_data, city_name, "city", state_abbr, county_name)
        
        # Add links back to county and state pages
        content += f"""
        <p>
        <a href="{BASE_URL}/{state_abbr}/{county_name.lower().replace(' ', '-')}/bail-bonds-in-{county_name.lower().replace(' ', '-')}" target="_blank">View All {county_name} Bail Bond Services</a><br>
        <a href="{BASE_URL}/bail-bonds-in-{state_name.lower()}" target="_blank">View All {state_name} Bail Bond Services</a>
        </p>
        """
        
        # Create the page
        data = {
            'title': page_title,
            'content': content,
            'status': 'publish',
            'slug': page_slug,
            'meta': {
                '_et_pb_use_builder': 'on',
                '_et_pb_old_content': '',
                '_et_pb_post_type_layout': 'custom_body',
                '_yoast_wpseo_metadesc': create_meta_description(keyword_data, "city", city_name, state_name)
            }
        }
        
        response = requests.post(
            f"{BASE_URL}/wp-json/wp/v2/pages",
            auth=AUTH,
            json=data
        )
        response.raise_for_status()
        
        page_data = response.json()
        print(f"    ✓ Created city page: {city_name} (ID: {page_data['id']})")
        print(f"      URL: {page_data['link']}")
        return page_data['id']
        
    except Exception as e:
        print(f"    ✗ Error creating city page for {city_name}: {str(e)}")
        return None

def create_hierarchical_pages():
    """Create a hierarchical structure of pages for states, counties, and cities"""
    # Process each state
    for state_name in STATE_DATA.keys():
        print(f"\nProcessing state: {state_name}")
        
        # Create state page with Divi Theme Builder template
        state_page_id = create_state_page(state_name)
        if not state_page_id:
            print(f"Skipping {state_name} counties due to state page creation failure")
            continue
            
        time.sleep(2)  # Pause to avoid overwhelming the API
        
        # For county pages, we still need the template content
        template_content = get_template_content()
        if template_content is None:
            print("Failed to get template content for county pages. Exiting.")
            return
        
        # Process counties in this state
        state_info = STATE_DATA[state_name]
        for county_name in state_info['counties'].keys():
            print(f"  Processing county: {county_name}")
            
            # Create county page
            county_page_id = create_county_page(state_name, county_name, template_content)
            if not county_page_id:
                print(f"  Skipping {county_name} cities due to county page creation failure")
                continue
                
            time.sleep(2)  # Pause to avoid overwhelming the API
            
            # Process cities in this county
            county_info = state_info['counties'][county_name]
            for city_name in county_info['cities']:
                print(f"    Processing city: {city_name}")
                
                # Create city page
                city_page_id = create_city_page(state_name, county_name, city_name, template_content)
                
                time.sleep(2)  # Pause to avoid overwhelming the API

if __name__ == "__main__":
    create_hierarchical_pages() 