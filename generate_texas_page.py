#!/usr/bin/env python3
"""
Texas Page Generator for Bail Bonds Buddy
This script generates a unique Texas bail bondsman page.
"""

import os
import json
import random
import sys
from Manus.improved_page_generator_part1 import load_template, load_state_data, generate_texas_data
from Manus.improved_page_generator_part2 import generate_page_for_state
from Manus.content_generator_utils_part1 import generate_unique_intro_paragraph, generate_unique_guide_paragraph
from Manus.improved_page_generator_part3 import generate_wordpress_page

# Constants
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "generated_pages")
STATE_DATA_DIR = os.path.join(BASE_DIR, "state_data")

def generate_texas_page():
    """Generate a unique page for Texas"""
    print("Generating unique Texas page...")
    
    # Create output directory if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Load template
    template_json = load_template()
    if not template_json:
        print("Failed to load template")
        return False
    
    # Generate page for Texas
    success = generate_page_for_state("Texas", template_json)
    if not success:
        print("Failed to generate Texas page")
        return False
    
    # Save the generated page
    output_file = f"{OUTPUT_DIR}/texas_unique.json"
    html_preview = f"{OUTPUT_DIR}/texas_unique.html"
    
    try:
        # Save JSON
        with open(output_file, 'w') as f:
            json.dump(template_json, f, indent=2)
        print(f"Generated page saved to {output_file}")
        
        # Save HTML preview
        title = template_json.get("title", "Texas Bail Bondsman")
        content = template_json.get("content", "")
        
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>{title}</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; margin: 0; padding: 20px; }}
        h1, h2, h3 {{ color: #0066cc; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{title}</h1>
        {content}
    </div>
</body>
</html>"""
        
        with open(html_preview, 'w') as f:
            f.write(html)
        print(f"HTML preview saved to {html_preview}")
        
        return True
    except Exception as e:
        print(f"Error saving generated page: {e}")
        return False

if __name__ == "__main__":
    generate_texas_page() 