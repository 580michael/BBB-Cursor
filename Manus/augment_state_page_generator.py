#!/usr/bin/env python3
"""
Augment State Page Generator for Bail Bonds Buddy
Handles state data collection, page generation, and WordPress upload in one streamlined process.

Usage:
    python3 augment_state_page_generator.py --state "New Mexico"
"""

import os
import json
import sys
import requests
import argparse
from typing import Dict, Optional

# Constants
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_DATA_DIR = os.path.join(BASE_DIR, "state_data")
TEMPLATE_FILE = os.path.join(BASE_DIR, "templates", "State-Template-Page-Only-Variables.json")
WP_BASE_URL = "https://bailbondsbuddy.com/wp-json/wp/v2"
WP_AUTH = ("bbbuddy", "DpSm eiz8 yHjx Sqqk G3lG fqU6")

class StatePageGenerator:
    def __init__(self, state_name: str):
        self.state_name = state_name
        self.state_data = {}
        os.makedirs(STATE_DATA_DIR, exist_ok=True)
    
    def gather_state_data(self) -> Dict:
        """
        Gather and structure all necessary state data.
        This should be customized with actual data sources (API calls, database queries, etc.)
        """
        print(f"Gathering data for {self.state_name}...")
        
        # This is where you would implement actual data gathering
        # For now, we'll require manual input for key data
        self.state_data = {
            "name": self.state_name,
            "abbreviation": input(f"Enter {self.state_name}'s two-letter abbreviation: ").upper(),
            "nickname": input(f"Enter {self.state_name}'s nickname (e.g., Land of Enchantment): "),
            "capital": {
                "name": input(f"Enter {self.state_name}'s capital city: "),
                "address": input("Enter capital's full address: "),
                "lat": input("Enter capital's latitude: "),
                "lng": input("Enter capital's longitude: ")
            },
            "population": input(f"Enter {self.state_name}'s population: "),
            "num_counties": int(input(f"Enter number of counties in {self.state_name}: ")),
            "largest_counties": [
                input(f"Enter name of largest county in {self.state_name}: "),
                input("Enter name of second largest county: "),
                input("Enter name of third largest county: ")
            ],
            "major_cities": [
                input(f"Enter largest city in {self.state_name}: "),
                input("Enter second largest city: "),
                input("Enter third largest city: ")
            ],
            "economic_info": input("Enter brief economic overview: "),
            "bail_system": input("Enter bail system information: "),
            "criminal_justice": input("Enter criminal justice system overview: "),
            "geography": input("Enter geographical information: "),
            "weather": input("Enter typical weather patterns: ")
        }
        
        # Save state data
        self._save_state_data()
        return self.state_data
    
    def _save_state_data(self):
        """Save state data to JSON file"""
        filename = os.path.join(STATE_DATA_DIR, f"{self.state_name.lower().replace(' ', '_')}.json")
        with open(filename, 'w') as f:
            json.dump(self.state_data, f, indent=2)
        print(f"State data saved to {filename}")
    
    def generate_page(self) -> Dict:
        """Generate WordPress page data using template and state data"""
        print("Generating page content...")
        
        # Load template
        with open(TEMPLATE_FILE, 'r') as f:
            template = json.load(f)
        
        # Replace placeholders in template
        content = template["content"]
        replacements = {
            "[state_name]": self.state_data["name"],
            "[state_abbr]": self.state_data["abbreviation"],
            "[state_nickname]": self.state_data["nickname"],
            "[state_population]": self.state_data["population"],
            "[state_counties]": str(self.state_data["num_counties"]),
            "[state_capital]": self.state_data["capital"]["name"],
            "[state_capital_address]": self.state_data["capital"]["address"],
            "[state_capital_lat]": self.state_data["capital"]["lat"],
            "[state_capital_lng]": self.state_data["capital"]["lng"],
            "[county_1]": self.state_data["largest_counties"][0],
            "[county_2]": self.state_data["largest_counties"][1],
            "[county_3]": self.state_data["largest_counties"][2],
            "[major_city_1]": self.state_data["major_cities"][0],
            "[major_city_2]": self.state_data["major_cities"][1],
            "[major_city_3]": self.state_data["major_cities"][2],
            "[economic_info]": self.state_data["economic_info"],
            "[bail_system_info]": self.state_data["bail_system"],
            "[criminal_justice_info]": self.state_data["criminal_justice"],
            "[geographical_info]": self.state_data["geography"],
            "[weather_info]": self.state_data["weather"]
        }
        
        for placeholder, value in replacements.items():
            content = content.replace(placeholder, str(value))
        
        # Create page data
        page_data = {
            "title": f"Bail Bonds in {self.state_name} | Licensed Bail Bonds Company",
            "slug": f"bail-bonds-in-{self.state_name.lower().replace(' ', '-')}-{self.state_data['abbreviation'].lower()}",
            "content": content,
            "status": "draft",
            "meta": {
                "description": f"Find trusted bail bond agents in {self.state_name}. 24/7 service, fast release, and affordable payment options. Licensed bail bondsmen ready to help.",
                "_et_pb_use_builder": "on",
                "_et_pb_page_layout": "et_no_sidebar",
                "_et_pb_side_nav": "off",
                "_wp_page_template": "page-template-blank.php",
                "_et_pb_post_type_layout": "custom_body",
                "_et_gb_content_width": "1080px"
            }
        }
        
        return page_data
    
    def upload_to_wordpress(self, page_data: Dict) -> Optional[int]:
        """Upload the generated page to WordPress"""
        print("Uploading to WordPress...")
        
        try:
            response = requests.post(
                f"{WP_BASE_URL}/pages",
                auth=WP_AUTH,
                json=page_data
            )
            
            if response.status_code in range(200, 300):
                page_id = response.json().get("id")
                print(f"Successfully created page with ID {page_id}")
                print(f"Draft page URL: https://bailbondsbuddy.com/?page_id={page_id}")
                return page_id
            else:
                print(f"Error creating page: {response.status_code}")
                print(response.text)
                return None
                
        except Exception as e:
            print(f"Error uploading to WordPress: {str(e)}")
            return None

def main():
    parser = argparse.ArgumentParser(description="Generate and upload state pages for Bail Bonds Buddy")
    parser.add_argument("--state", required=True, help="State name (e.g., 'New Mexico')")
    args = parser.parse_args()
    
    generator = StatePageGenerator(args.state)
    
    # Step 1: Gather state data
    state_data = generator.gather_state_data()
    if not state_data:
        print("Failed to gather state data")
        sys.exit(1)
    
    # Step 2: Generate page
    page_data = generator.generate_page()
    if not page_data:
        print("Failed to generate page")
        sys.exit(1)
    
    # Step 3: Upload to WordPress
    page_id = generator.upload_to_wordpress(page_data)
    if not page_id:
        print("Failed to upload page")
        sys.exit(1)
    
    print("Process completed successfully!")

if __name__ == "__main__":
    main()