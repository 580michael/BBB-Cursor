import os
import json

def normalize_name(name):
    """Normalize county/city names by removing 'County' and extra spaces"""
    return name.strip().replace(" County", "").strip()

def format_directory_name(county):
    """Format county name for directory (e.g., 'Dallas County' -> 'Dallas-County')"""
    return f"{normalize_name(county)}-County"

def should_skip_entry(city):
    """Check if the entry should be skipped based on certain keywords"""
    skip_terms = ['Bank', 'Insurance', 'Trust', 'Company', 'Corporation', 'Corp', 'Inc']
    return any(term in city for term in skip_terms)

def format_county_name(name):
    """Format county name from uppercase to title case and add 'County'"""
    return f"{name.title()} County"

# Set up paths
script_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(os.path.dirname(script_dir))
texas_txt_path = os.path.join(root_dir, 'Texas.txt')

print(f"Reading cities from: {texas_txt_path}")

# Read the cities data
cities_by_county = {}
try:
    with open(texas_txt_path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) >= 5:  # Ensure we have all required fields
                city = parts[0].strip()
                county = format_county_name(parts[3].strip())  # Get county from fourth column
                
                # Skip entries that match skip terms
                if should_skip_entry(city):
                    continue
                
                # Add city to the county's list
                if county not in cities_by_county:
                    cities_by_county[county] = set()
                cities_by_county[county].add(city)

except FileNotFoundError:
    print(f"Error: Texas.txt file not found at {texas_txt_path}")
    exit(1)

print(f"Found {len(cities_by_county)} counties with cities")

# Create county files
base_dir = os.path.join(script_dir, "counties")
if not os.path.exists(base_dir):
    os.makedirs(base_dir)

print(f"Writing city files to: {base_dir}")

# Process each county
for county, cities in cities_by_county.items():
    # Format directory name
    dir_name = format_directory_name(county)
    county_dir = os.path.join(base_dir, dir_name)
    
    # Create county directory if it doesn't exist
    if not os.path.exists(county_dir):
        os.makedirs(county_dir)
    
    # Create cities subdirectory
    cities_dir = os.path.join(county_dir, "cities")
    if not os.path.exists(cities_dir):
        os.makedirs(cities_dir)
    
    # Create the cities file
    file_name = f"{dir_name.lower()}-cities.txt"
    file_path = os.path.join(county_dir, file_name)
    
    # Write sorted cities to file
    with open(file_path, 'w', encoding='utf-8') as f:
        for city in sorted(cities):
            f.write(f"{city}\n")
    
    print(f"Created {file_path} with {len(cities)} cities")

print("Completed organizing Texas cities into county files") 