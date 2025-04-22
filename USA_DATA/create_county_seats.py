import os
import json
from datetime import datetime

def get_state_name(abbr):
    """Return full state name from abbreviation"""
    state_names = {
        'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas',
        'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware',
        'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii', 'ID': 'Idaho',
        'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas',
        'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland',
        'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi',
        'MO': 'Missouri', 'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada',
        'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NY': 'New York',
        'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio', 'OK': 'Oklahoma',
        'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina',
        'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah',
        'VT': 'Vermont', 'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia',
        'WI': 'Wisconsin', 'WY': 'Wyoming'
    }
    return state_names.get(abbr, '')

def format_directory_name(county):
    """Format county name for directory"""
    return f"{county.replace(' County', '').strip()}-County"

def create_county_seats_json(state_abbr):
    """Create county-seats.json file for a state"""
    state_name = get_state_name(state_abbr)
    if not state_name:
        print(f"Skipping {state_abbr} - not a US state")
        return

    # Skip if already exists
    output_file = f"USA_DATA/{state_abbr}/{state_abbr.lower()}-{'parish' if state_abbr == 'LA' else 'county'}-seats.json"
    if os.path.exists(output_file):
        print(f"Skipping {state_abbr} - file already exists")
        return

    # Read the cities file to extract county information
    counties = {}
    state_dir = f"USA_DATA/{state_abbr}/{'parishes' if state_abbr == 'LA' else 'counties'}"
    
    if not os.path.exists(state_dir):
        print(f"Skipping {state_abbr} - no {'parishes' if state_abbr == 'LA' else 'counties'} directory found")
        return

    # Get all county directories
    county_dirs = [d for d in os.listdir(state_dir) if os.path.isdir(os.path.join(state_dir, d))]
    
    # For each county directory, read the cities file to find the county seat
    for county_dir in county_dirs:
        county_name = county_dir.replace('-County', '').replace('-Parish', '')
        cities_file = os.path.join(state_dir, county_dir, 
                                 f"{county_name.lower()}-{'parish' if state_abbr == 'LA' else 'county'}-cities.txt")
        
        if os.path.exists(cities_file):
            with open(cities_file, 'r', encoding='utf-8') as f:
                # Assume first city in the file is the county seat
                county_seat = f.readline().strip()
                counties[county_name] = {
                    f"{'parish' if state_abbr == 'LA' else 'county'}_seat": county_seat,
                    "directory": county_dir
                }

    # Create the JSON structure
    data = {
        "metadata": {
            "state": state_name,
            "stateAbbr": state_abbr,
            "lastUpdated": datetime.now().strftime("%Y-%m-%d"),
            f"total_{'parishes' if state_abbr == 'LA' else 'counties'}": len(counties)
        },
        f"{'parishes' if state_abbr == 'LA' else 'counties'}": counties
    }

    # Ensure state directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Write the JSON file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

    print(f"Created {output_file} with {len(counties)} {'parishes' if state_abbr == 'LA' else 'counties'}")

def main():
    # Process all state directories (excluding OK and TX)
    state_abbrs = [
        'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
        'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
        'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
        'NM', 'NY', 'NC', 'ND', 'OH', 'OR', 'PA', 'RI', 'SC', 'SD',
        'TN', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
    ]

    for state_abbr in state_abbrs:
        create_county_seats_json(state_abbr)

if __name__ == "__main__":
    main() 