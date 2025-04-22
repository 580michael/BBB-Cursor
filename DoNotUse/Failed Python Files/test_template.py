import csv
import json
import os
import requests
from urllib.parse import urljoin
from typing import Dict, Any

# Constants
BASE_URL = "https://bailbondsbuddy.com"
TEMPLATE_PAGE_ID = 501  # Updated to use the working template page
AUTH = ('bbbuddy', 'DpSm eiz8 yHjx Sqqk G3lG fqU6')

class WordPressPageCreator:
    def __init__(self, wp_url, username, app_password):
        self.wp_url = wp_url
        self.api_url = urljoin(wp_url, 'wp-json/wp/v2/')
        self.auth = (username, app_password)
    
    def create_page(self, title, content="", status="draft", template=""):
        endpoint = urljoin(self.api_url, 'pages')
        
        # Convert template content to WordPress format if provided
        if template and isinstance(template, dict):
            content = self.convert_template_to_content(template)
        
        data = {
            'title': title,
            'content': content,
            'status': status
        }
        
        response = requests.post(endpoint, json=data, auth=self.auth)
        if response.status_code == 201:
            return response.json()
        else:
            raise Exception(f"Failed to create page: {response.text}")
    
    def update_page(self, page_id, title=None, content=None, status=None):
        endpoint = urljoin(self.api_url, f'pages/{page_id}')
        data = {}
        
        if title:
            data['title'] = title
        if content:
            data['content'] = content
        if status:
            data['status'] = status
            
        response = requests.post(endpoint, json=data, auth=self.auth)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to update page: {response.text}")
    
    def convert_template_to_content(self, template):
        content = ""
        if 'layout_content' in template:
            for section in template['layout_content']:
                content += self.convert_section(section)
        return content
    
    def convert_section(self, section):
        content = '<div class="section"'
        
        # Add background color if specified
        if 'css' in section and 'background_color' in section['css']:
            content += f' style="background-color: {section["css"]["background_color"]};"'
        
        content += '>\n'
        
        # Convert modules
        if 'modules' in section:
            for module in section['modules']:
                if isinstance(module, dict):
                    if module['type'] == 'row':
                        content += self.convert_row(module)
                    # Add other module types as needed
        
        content += '</div>\n'
        return content
    
    def convert_row(self, row):
        content = '<div class="row">\n'
        if 'columns' in row:
            for column in row['columns']:
                content += self.convert_column(column)
        content += '</div>\n'
        return content
    
    def convert_column(self, column):
        content = '<div class="column"'
        
        # Add width if specified
        if 'css' in column and 'width' in column['css']:
            content += f' style="width: {column["css"]["width"]};"'
        
        content += '>\n'
        
        # Convert modules
        if 'modules' in column:
            for module in column['modules']:
                if isinstance(module, dict):
                    if module['type'] == 'text':
                        content += module['content'] + '\n'
                    elif module['type'] == 'blurb':
                        content += f'<div class="blurb"><h3>{module["title"]}</h3><p>{module["content"]}</p></div>\n'
                    elif module['type'] == 'button':
                        content += f'<a href="{module["button_url"]}" class="button">{module["button_text"]}</a>\n'
                    # Add other module types as needed
        
        content += '</div>\n'
        return content

def create_state_page(state_name):
    """Create a new WordPress page for a state using the template."""
    try:
        # Get template content
        template_response = requests.get(
            f"{BASE_URL}/wp-json/wp/v2/pages/{TEMPLATE_PAGE_ID}",
            auth=AUTH,
            params={'context': 'edit'}  # This will give us the raw content
        )
        template_response.raise_for_status()  # Raise an exception for bad status codes
        template_data = template_response.json()
        
        # Get content from template - first try raw, then rendered if raw not available
        content = template_data.get('content', {})
        if isinstance(content, dict):
            content = content.get('raw', content.get('rendered', ''))
        elif isinstance(content, str):
            content = content
        else:
            raise ValueError("Unexpected content format in template")
            
        if not content:
            raise ValueError("Could not get content from template")
            
        # Replace placeholders with state name
        content = content.replace('[state_name]', state_name)
        
        # Prepare data for the new page
        data = {
            'title': f'Bail Bonds in {state_name}',
            'content': content,
            'status': 'publish',
            'meta': {
                '_et_pb_use_builder': 'on',
                '_et_pb_old_content': '',
                '_et_pb_post_type_layout': 'custom_body'
            }
        }
        
        # Create the page
        response = requests.post(
            f"{BASE_URL}/wp-json/wp/v2/pages",
            auth=AUTH,
            json=data
        )
        response.raise_for_status()  # Raise an exception for bad status codes
        
        page_data = response.json()
        print(f"Successfully created page for {state_name}")
        print(f"View at: {BASE_URL}/?page_id={page_data['id']}")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"HTTP Error: {str(e)}")
        return False
    except (ValueError, KeyError) as e:
        print(f"Data Error: {str(e)}")
        return False
    except Exception as e:
        print(f"Unexpected Error: {str(e)}")
        return False

def load_template(template_path):
    with open(template_path, 'r') as f:
        return json.load(f)

def load_state_data(csv_path):
    states = {}
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            states[row['state_name']] = row
    return states

def replace_variables(content, state_data):
    if isinstance(content, dict):
        for key, value in content.items():
            content[key] = replace_variables(value, state_data)
    elif isinstance(content, list):
        return [replace_variables(item, state_data) for item in content]
    elif isinstance(content, str):
        for key, value in state_data.items():
            if f"[{key}]" in content:
                content = content.replace(f"[{key}]", str(value))
    return content

def generate_state_template():
    return {
        "version": "4.20.0",
        "title": "State Template",
        "layout_type": "template",
        "layout_content": [
            {
                "type": "section",
                "css": {
                    "background_color": "#2b87da",
                    "padding": "80px|0px|80px|0px"
                },
                "modules": [
                    {
                        "type": "row",
                        "columns": [
                            {
                                "type": "column",
                                "css": {
                                    "padding": "20px|20px|20px|20px",
                                    "width": "50%"
                                },
                                "modules": [
                                    {
                                        "type": "text",
                                        "content": "<h1 style='color: #ffffff; font-size: 48px; line-height: 1.2em;'>Find Bail Bonds in [state_name]</h1>",
                                        "css": {
                                            "text_align": "left"
                                        }
                                    },
                                    {
                                        "type": "text",
                                        "content": "<p style='color: #ffffff; font-size: 18px;'>Find trusted bail bondsmen available 24/7 across [state_name]. Connect with licensed professionals in your area instantly.</p>",
                                        "css": {
                                            "text_align": "left"
                                        }
                                    },
                                    {
                                        "type": "search",
                                        "placeholder": "Search for bail bondsmen in [state_name]...",
                                        "button_text": "Find Bail Bondsmen",
                                        "css": {
                                            "width": "100%",
                                            "margin_top": "20px"
                                        }
                                    }
                                ]
                            },
                            {
                                "type": "column",
                                "css": {
                                    "padding": "20px|20px|20px|20px",
                                    "width": "50%"
                                },
                                "modules": [
                                    {
                                        "type": "map",
                                        "address": "[state_name]",
                                        "zoom_level": "6",
                                        "height": "400px",
                                        "css": {
                                            "border_radius": "8px",
                                            "box_shadow": "0px 4px 12px rgba(0,0,0,0.1)"
                                        }
                                    }
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                "type": "section",
                "css": {
                    "background_color": "#ffffff",
                    "padding": "60px|0px|60px|0px"
                },
                "modules": [
                    {
                        "type": "row",
                        "columns": [
                            {
                                "type": "column",
                                "css": {
                                    "padding": "20px|20px|20px|20px"
                                },
                                "modules": [
                                    {
                                        "type": "text",
                                        "content": "<h2 style='text-align: center; color: #333333;'>Your Trusted Guide to Finding Bail Bondsmen in [state_name]</h2>",
                                        "css": {
                                            "font_size": "36px",
                                            "margin_bottom": "20px"
                                        }
                                    },
                                    {
                                        "type": "text",
                                        "content": "<p style='text-align: center; color: #666666;'>We understand that finding a reliable bail bondsman can be stressful, especially in urgent situations. BailBondsBuddy.com simplifies the process by connecting you with trusted bail bond professionals in [state_name], any time of day or night.</p>",
                                        "css": {
                                            "font_size": "18px",
                                            "line_height": "1.6em"
                                        }
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "type": "row",
                        "columns": [
                            {
                                "type": "column",
                                "css": {
                                    "padding": "20px|20px|20px|20px",
                                    "width": "33.33%"
                                },
                                "modules": [
                                    {
                                        "type": "blurb",
                                        "title": "24/7 Availability",
                                        "content": "Emergency bail bond services available anytime, day or night, when you need help the most.",
                                        "use_icon": True,
                                        "font_icon": "⏰",
                                        "css": {
                                            "text_align": "center"
                                        }
                                    }
                                ]
                            },
                            {
                                "type": "column",
                                "css": {
                                    "padding": "20px|20px|20px|20px",
                                    "width": "33.33%"
                                },
                                "modules": [
                                    {
                                        "type": "blurb",
                                        "title": "Verified Bondsmen",
                                        "content": "All bail bondsmen are licensed and verified in [state_name].",
                                        "use_icon": True,
                                        "font_icon": "✓",
                                        "css": {
                                            "text_align": "center"
                                        }
                                    }
                                ]
                            },
                            {
                                "type": "column",
                                "css": {
                                    "padding": "20px|20px|20px|20px",
                                    "width": "33.33%"
                                },
                                "modules": [
                                    {
                                        "type": "blurb",
                                        "title": "Local Coverage",
                                        "content": "From small towns to major cities, find bondsmen across all [state_name] counties.",
                                        "use_icon": True,
                                        "font_icon": "📍",
                                        "css": {
                                            "text_align": "center"
                                        }
                                    }
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                "type": "section",
                "css": {
                    "background_color": "#f5f5f5",
                    "padding": "60px|0px|60px|0px"
                },
                "modules": [
                    {
                        "type": "row",
                        "columns": [
                            {
                                "type": "column",
                                "css": {
                                    "padding": "20px|20px|20px|20px"
                                },
                                "modules": [
                                    {
                                        "type": "text",
                                        "content": "<h2 style='text-align: center; color: #333333;'>Counties in [state_name]</h2>",
                                        "css": {
                                            "font_size": "32px",
                                            "margin_bottom": "40px"
                                        }
                                    },
                                    {
                                        "type": "blog",
                                        "fullwidth": "off",
                                        "posts_number": "12",
                                        "include_categories": "[state_counties_category]",
                                        "show_thumbnail": True,
                                        "show_content": False,
                                        "show_author": False,
                                        "show_date": False,
                                        "show_categories": False,
                                        "show_pagination": True
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    }

def generate_state_page(template_path, csv_path, state_name, output_dir, wp_creator=None):
    # Load template and state data
    template = load_template(template_path)
    states = load_state_data(csv_path)
    
    if state_name not in states:
        raise ValueError(f"State {state_name} not found in CSV data")
    
    # Replace variables in template
    state_data = states[state_name]
    populated_template = replace_variables(template, state_data)
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Save populated template
    output_path = os.path.join(output_dir, f"{state_name.lower()}-template.json")
    with open(output_path, 'w') as f:
        json.dump(populated_template, f, indent=4)
    
    # Create WordPress page if wp_creator is provided
    if wp_creator:
        page_title = f"Bail Bonds in {state_name}"
        # Create page with template content
        page = wp_creator.create_page(
            title=page_title,
            template=populated_template,
            status="draft"
        )
        print(f"Created WordPress page: {page['link']}")
    
    return output_path

def get_template_content():
    """Get the content from the template page."""
    template_response = requests.get(
        f"{BASE_URL}/wp-json/wp/v2/pages/{TEMPLATE_PAGE_ID}",
        auth=AUTH,
        params={'context': 'edit'}  # This will give us the raw content
    )
    
    if template_response.status_code != 200:
        print(f"Error getting template: {template_response.status_code}")
        print(template_response.text)
        return None
        
    template_data = template_response.json()
    content = template_data.get('content', {}).get('raw', '')
    
    if not content:
        print("Error: Could not get raw content from template")
        return None
        
    return content

def main():
    template_content = get_template_content()
    if template_content is None:
        print("Failed to get template content")
        return False
    
    response = create_state_page(template_content)
    if response and isinstance(response, dict) and 'id' in response:
        print(f"New page created at: {BASE_URL}/?page_id={response['id']}")
        return True
    else:
        print("Failed to create page")
        return False

def get_state_counties(state_name):
    """Return a list of major counties for a given state."""
    state_counties = {
        "Oklahoma": ["Oklahoma County", "Tulsa County", "Cleveland County"],
        "Texas": ["Harris County", "Dallas County", "Bexar County"]
    }
    return state_counties.get(state_name, ["County 1", "County 2", "County 3"])

def get_state_capital(state_name):
    """Return the capital city for map centering."""
    state_capitals = {
        "Oklahoma": "Oklahoma City, Oklahoma",
        "Texas": "Austin, Texas"
    }
    return state_capitals.get(state_name, f"{state_name}, USA")

def get_state_coordinates(state_name):
    """Return the center coordinates for each state."""
    state_coords = {
        "Oklahoma": {"lat": "35.4676", "lng": "-97.5164"},  # Oklahoma City coordinates
        "Texas": {"lat": "30.2672", "lng": "-97.7431"}      # Austin coordinates
    }
    return state_coords.get(state_name, {"lat": "39.8283", "lng": "-98.5795"})  # Default to center of US

def get_state_capital_address(state_name):
    """Return the full address for the state capital."""
    capitals = {
        "Texas": "Austin, TX, USA",
        "Oklahoma": "Oklahoma City, OK, USA"
    }
    return capitals.get(state_name, f"{state_name}, USA")

def get_state_capital_info(state_name):
    """Return the capital city info including address and coordinates."""
    capitals = {
        "Texas": {
            "address": "Austin, TX, USA",
            "lat": "30.2672",
            "lng": "-97.7431"
        },
        "Oklahoma": {
            "address": "Oklahoma City, OK, USA",
            "lat": "35.4688692",
            "lng": "-97.519539"
        }
    }
    return capitals.get(state_name, {
        "address": f"{state_name}, USA",
        "lat": "39.8283",
        "lng": "-98.5795"
    })

def create_page(state_name):
    """Create a new WordPress page for a state using the template."""
    try:
        # Get template content
        template_response = requests.get(
            f"{BASE_URL}/wp-json/wp/v2/pages/{TEMPLATE_PAGE_ID}",
            auth=AUTH,
            params={'context': 'edit'}
        )
        template_response.raise_for_status()
        template_data = template_response.json()
        
        # Get content from template
        content = template_data.get('content', {}).get('raw', '')
        if not content:
            raise ValueError("Could not get raw content from template")
        
        # Get capital city info
        capital_info = get_state_capital_info(state_name)
        
        # Replace map address and coordinates
        content = content.replace('Oklahoma City, OK, USA', capital_info['address'])
        content = content.replace('35.4688692', capital_info['lat'])
        content = content.replace('-97.519539', capital_info['lng'])
        
        # Replace Oklahoma with the new state name
        content = content.replace('Oklahoma', state_name)
        
        # Replace county names
        if state_name == "Texas":
            content = content.replace('Tulsa County', 'Dallas County')
            content = content.replace('Cleveland County', 'Bexar County')
        
        # Create the page
        data = {
            'title': f'Bail Bonds in {state_name}',
            'content': content,
            'status': 'publish',
            'slug': f'bail-bonds-in-{state_name.lower()}',
            'meta': {
                '_et_pb_use_builder': 'on',
                '_et_pb_old_content': '',
                '_et_pb_post_type_layout': 'custom_body'
            }
        }
        
        response = requests.post(
            f"{BASE_URL}/wp-json/wp/v2/pages",
            auth=AUTH,
            json=data
        )
        response.raise_for_status()
        
        page_data = response.json()
        print(f"Successfully created page with ID: {page_data['id']}")
        print(f"View the page at: {page_data['link']}")
        return page_data['id']
        
    except requests.exceptions.RequestException as e:
        print(f"HTTP Error: {str(e)}")
        if hasattr(e, 'response') and hasattr(e.response, 'text'):
            print(f"Response: {e.response.text}")
        return None
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

def create_pages_for_states(states):
    """Create pages for multiple states."""
    for state in states:
        page_id = create_page(state)
        if page_id:
            print(f"✓ Successfully created page for {state}")
        else:
            print(f"✗ Failed to create page for {state}")

# Update the main section to create pages for both states
if __name__ == "__main__":
    states_to_create = ["Texas"]  # Let's just try Texas first
    for state in states_to_create:
        page_id = create_page(state)
        if page_id:
            print(f"✓ Successfully created page for {state}")
        else:
            print(f"✗ Failed to create page for {state}") 