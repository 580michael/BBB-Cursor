import os
import json
from collections import defaultdict

def normalize_name(name):
    """Normalize county/city names by removing 'County' and extra spaces"""
    return name.strip().replace(" County", "").strip()

def format_directory_name(county, state_abbr=None):
    """Format county/parish name for directory"""
    if state_abbr == 'LA':
        return f"{normalize_name(county)}-Parish"
    return f"{normalize_name(county)}-County"

def format_file_name(county, state_abbr=None):
    """Format the name for the cities file"""
    if state_abbr == 'LA':
        return f"{normalize_name(county).lower()}-parish-cities.txt"
    return f"{normalize_name(county).lower()}-county-cities.txt"

def should_skip_entry(city):
    """Check if the entry should be skipped based on certain keywords"""
    skip_terms = ['Bank', 'Insurance', 'Trust', 'Company', 'Corporation', 'Corp', 'Inc']
    return any(term in city for term in skip_terms)

def format_county_name(name, state_abbr=None):
    """Format county/parish name from uppercase to title case and add appropriate suffix"""
    if state_abbr == 'LA':
        return name.title()
    return f"{name.title()} County"

def process_state(state_abbr, cities_data):
    """Process cities data for a single state"""
    # Create state directory if it doesn't exist
    state_dir = os.path.join("USA_DATA", state_abbr)
    if not os.path.exists(state_dir):
        os.makedirs(state_dir)
    
    # Create counties directory
    counties_dir = os.path.join(state_dir, "counties")
    if not os.path.exists(counties_dir):
        os.makedirs(counties_dir)
    
    # Group cities by county
    counties = defaultdict(set)
    for city, state, county in cities_data:
        if should_skip_entry(city):
            continue
        counties[format_county_name(county, state_abbr)].add(city)
    
    print(f"\nProcessing {state_abbr} - Found {len(counties)} counties")
    
    # Create county directories and files
    for county, cities in counties.items():
        dir_name = format_directory_name(county, state_abbr)
        county_dir = os.path.join(counties_dir, dir_name)
        
        # Create county directory
        if not os.path.exists(county_dir):
            os.makedirs(county_dir)
        
        # Create cities subdirectory
        cities_dir = os.path.join(county_dir, "cities")
        if not os.path.exists(cities_dir):
            os.makedirs(cities_dir)
        
        # Create cities file with appropriate naming
        file_name = format_file_name(county, state_abbr)
        file_path = os.path.join(county_dir, file_name)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            for city in sorted(cities):
                f.write(f"{city}\n")
        
        print(f"Created {file_path} with {len(cities)} cities")

def main():
    # Set up paths
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Go up one level to root
    all_states_file = os.path.join(script_dir, "All 50 States-disorganized.txt")
    
    # States to skip (already processed)
    skip_states = {'TX', 'OK'}
    
    # Read and group data by state
    state_data = defaultdict(list)
    print(f"Reading data from: {all_states_file}")
    
    with open(all_states_file, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) >= 5:
                city = parts[0].strip()
                state = parts[1].strip()
                county = parts[3].strip()
                
                # Skip non-state territories and already processed states
                if state in skip_states or len(state) != 2:
                    continue
                
                state_data[state].append((city, state, county))
    
    # Sort states alphabetically
    sorted_states = sorted(state_data.keys())
    print(f"\nFound {len(sorted_states)} states to process")
    
    # Process states in batches of 5
    batch_size = 5
    for i in range(0, len(sorted_states), batch_size):
        batch = sorted_states[i:i + batch_size]
        print(f"\nProcessing batch {(i//batch_size)+1} of {(len(sorted_states)+batch_size-1)//batch_size}")
        print(f"States in this batch: {', '.join(batch)}")
        
        for state in batch:
            process_state(state, state_data[state])
        
        print(f"\nCompleted batch {(i//batch_size)+1}")

if __name__ == "__main__":
    main() 