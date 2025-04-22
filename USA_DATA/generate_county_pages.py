import os
import json
from datetime import datetime
import math

def load_county_data(county_data_file):
    """Load the comprehensive county dataset"""
    with open(county_data_file, 'r') as f:
        return json.load(f)

def load_county_seats(state_abbr):
    """Load county seats data for a state"""
    filename = f"USA_DATA/{state_abbr}/{state_abbr.lower()}-{'parish' if state_abbr == 'LA' else 'county'}-seats.json"
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def format_number(num):
    """Format numbers with commas"""
    if isinstance(num, (int, float)):
        return "{:,}".format(round(num))
    return num

def get_latest_population(population_data):
    """Get the most recent population figure"""
    if not population_data:
        return None
    latest_year = max(population_data.keys())
    return population_data[latest_year]

def calculate_percentages(male, female):
    """Calculate gender ratio percentages"""
    total = male + female
    return round(male/total * 100, 1), round(female/total * 100, 1)

def generate_county_page(county_data, county_seats_data, template_path, output_dir):
    """Generate a county profile page using the template"""
    with open(template_path, 'r') as f:
        template = f.read()

    # Extract county name and state
    county_name = county_data['name'].title()
    state_abbr = county_data['state']
    
    # Get county seat from our existing data
    county_key = county_name.replace(" County", "")
    county_seat = "Unknown"
    if county_seats_data and 'counties' in county_seats_data:
        if county_key in county_seats_data['counties']:
            county_seat = county_seats_data['counties'][county_key]['county_seat']

    # Calculate latest population and gender ratios
    current_population = get_latest_population(county_data['population'])
    male_ratio, female_ratio = calculate_percentages(county_data['male'], county_data['female'])

    # Prepare replacement dictionary
    replacements = {
        '{{county_name}}': county_name,
        '{{state_name}}': county_seats_data['metadata']['state'],
        '{{county_seat}}': county_seat,
        '{{land_area}}': format_number(county_data['land_area']),
        '{{latitude}}': round(county_data['latitude'], 4),
        '{{longitude}}': abs(round(county_data['longitude'], 4)),
        '{{zip_codes}}': ', '.join(county_data['zip-codes'][:5]) + ('...' if len(county_data['zip-codes']) > 5 else ''),
        '{{current_population}}': format_number(current_population),
        '{{male_ratio}}': male_ratio,
        '{{female_ratio}}': female_ratio,
        '{{avg_income}}': format_number(county_data['avg_income']),
        '{{living_wage}}': format_number(county_data['cost-of-living']['living_wage']),
        '{{poverty_rate}}': county_data['poverty-rate'],
        '{{avg_temp}}': round(county_data['noaa']['temp'], 1),
        '{{precipitation}}': round(county_data['noaa']['prcp'], 1),
        '{{snowfall}}': round(county_data['noaa']['snow'], 1),
        '{{housing_costs}}': format_number(county_data['cost-of-living']['housing_costs']),
        '{{food_costs}}': format_number(county_data['cost-of-living']['food_costs']),
        '{{medical_costs}}': format_number(county_data['cost-of-living']['medical_costs'])
    }

    # Replace all placeholders in template
    page_content = template
    for key, value in replacements.items():
        page_content = page_content.replace(key, str(value))

    # Create output directory if it doesn't exist
    state_dir = os.path.join(output_dir, state_abbr)
    os.makedirs(state_dir, exist_ok=True)

    # Write the generated page
    output_file = os.path.join(state_dir, f"{county_name.lower().replace(' ', '-')}.html")
    with open(output_file, 'w') as f:
        f.write(page_content)

    print(f"Generated profile page for {county_name}, {state_abbr}")

def main():
    # Load the comprehensive county dataset
    county_data = load_county_data('USA_DATA/county_data.json')

    # Process each county
    for county in county_data:
        state_abbr = county['state']
        county_seats_data = load_county_seats(state_abbr)
        
        if county_seats_data:
            generate_county_page(
                county,
                county_seats_data,
                'USA_DATA/county_profile_template.html',
                'USA_DATA/county_profiles'
            )

if __name__ == "__main__":
    main() 