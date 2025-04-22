#!/usr/bin/env python3
"""
Cline State Page Generator for Bail Bonds Buddy (Part 3)

This script provides the main execution logic for the state page generation system.
It works together with cline_state.py and cline_state_part2.py to provide a complete solution.

This file handles:
1. Command-line argument parsing
2. Coordinating the generation of state pages
3. Uploading pages to WordPress

Usage:
  python3 cline_state_part3.py --state [StateName]         # Generate a state page
  python3 cline_state_part3.py --state [StateName] --upload # Generate and upload to WordPress
  python3 cline_state_part3.py --all                       # Generate all state pages
"""

import os
import json
import argparse
import sys
import traceback
from cline_state_part2 import generate_page_for_state, upload_to_wordpress

def print_banner():
    """Print a banner for the script"""
    banner = """
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║   Cline State Page Generator for Bail Bonds Buddy Website     ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """
    print(banner)
    print("This script generates state pages for the Bail Bonds Buddy website.")
    print("It creates unique content for each state and can upload directly to WordPress.\n")

def generate_single_state(state_name, upload=False):
    """Generate a page for a single state and optionally upload it"""
    print(f"\n=== Generating page for {state_name} ===")
    success = generate_page_for_state(state_name)
    
    if success:
        print(f"✅ Successfully generated page for {state_name}")
        
        if upload:
            print(f"\n=== Uploading {state_name} page to WordPress ===")
            upload_success = upload_to_wordpress(state_name)
            
            if upload_success:
                print(f"✅ Successfully uploaded {state_name} page to WordPress")
            else:
                print(f"❌ Failed to upload {state_name} page to WordPress")
        
        return True
    else:
        print(f"❌ Failed to generate page for {state_name}")
        return False

def generate_all_states(upload=False):
    """Generate pages for all 50 states"""
    print("\n=== Generating pages for all 50 states ===")
    
    # List of all 50 states
    states = [
        "Alabama", "Alaska", "Arizona", "Arkansas", "California", 
        "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", 
        "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", 
        "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", 
        "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana",
        "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", 
        "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", 
        "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", 
        "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", 
        "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"
    ]
    
    success_count = 0
    for state in states:
        print(f"\nGenerating page for {state}...")
        if generate_page_for_state(state):
            success_count += 1
            print(f"✅ {state} page generated successfully")
            
            if upload:
                print(f"Uploading {state} page to WordPress...")
                if upload_to_wordpress(state):
                    print(f"✅ {state} page uploaded successfully")
                else:
                    print(f"❌ Failed to upload {state} page to WordPress")
        else:
            print(f"❌ Failed to generate page for {state}")
    
    print(f"\n=== Summary ===")
    print(f"Successfully generated {success_count} out of 50 state pages.")
    return success_count

def main():
    """Main function to handle command line arguments"""
    parser = argparse.ArgumentParser(description="Generate state pages for Bail Bonds Buddy")
    parser.add_argument('--state', type=str, help='Generate a page for a specific state')
    parser.add_argument('--upload', action='store_true', help='Upload the generated page to WordPress')
    parser.add_argument('--all', action='store_true', help='Generate pages for all states')
    args = parser.parse_args()

    print_banner()

    if args.state:
        generate_single_state(args.state, args.upload)
    elif args.all:
        generate_all_states(args.upload)
    else:
        print("No action specified. Use --state [StateName], --upload, or --all.")
        print("\nExamples:")
        print("  python3 cline_state_part3.py --state 'New Mexico'")
        print("  python3 cline_state_part3.py --state 'Texas' --upload")
        print("  python3 cline_state_part3.py --all")

if __name__ == "__main__":
    main()
