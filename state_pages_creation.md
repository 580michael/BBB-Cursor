# State Pages Creation Guide for BailBondsBuddy.com

## Overview
This guide documents the working process for creating state-specific pages on BailBondsBuddy.com using the DIVI template and WordPress API.

## Working Configuration

### Main Script
We are using `create_state_page.py` as our primary script. This script successfully:
- Creates pages with exact DIVI template formatting
- Sets up full-width pages without sidebars
- Maintains all styling and layout from the template

### WordPress API Configuration
```python
BASE_URL = "https://bailbondsbuddy.com"
API_URL = f"{BASE_URL}/wp-json/v2"
AUTH = ("bbbuddy", "DpSm eiz8 yHjx Sqqk G3lG fqU6")
```

### Template File
The template is stored in: `BailBondsBuddy.com _ Find Local Trusted Bail Bondsman in [state].json`

### Critical WordPress Page Settings
```python
page_data = {
    "title": format_title(state_name),
    "slug": create_slug(state_name),
    "content": content,
    "status": "draft",
    "meta": {
        "description": generate_meta_description(state_name),
        "_et_pb_page_layout": "et_no_sidebar",  # Full width
        "_et_pb_side_nav": "off",  # No side nav
        "_et_pb_use_builder": "on",  # Enable DIVI
        "_wp_page_template": "page-template-blank.php"  # Blank template
    }
}
```

## State Data Structure
```python
STATE_DATA = {
    "Oklahoma": {
        "abbreviation": "OK",
        "capital": {
            "name": "Oklahoma City",
            "address": "Oklahoma City, OK",
            "lat": "35.4676",
            "lng": "-97.5164"
        },
        "counties": ["Oklahoma County", "Tulsa County", "Cleveland County"],
        "sample_cities": ["Oklahoma City", "Tulsa", "Norman", "Edmond", "Lawton"]
    }
    # Additional states follow same format
}
```

## Placeholder System
The template uses standard bracket format for all replacements:
- State Name: `[state_name]`
- State Abbreviation: `[state_abbr]`
- Counties: `[county_name_1]`, `[county_name_2]`, `[county_name_3]`
- FAQs: `[FAQ_QUESTION_1]`, `[FAQ_ANSWER_1]` etc.

## Current Status
- ✅ Template formatting is perfect
- ✅ Page layout and styling match exactly
- ✅ Full-width layout working
- ✅ DIVI builder integration working
- ❌ Placeholder replacements need fixing (still showing brackets)

## How to Create a State Page

1. Ensure you have the required files:
   - `create_state_page.py`
   - `FAQ.md`
   - Template JSON file
   
2. Run the script:
```bash
python3 create_state_page.py
```

3. Check the created page at the provided URL:
```
https://bailbondsbuddy.com/?page_id=<PAGE_ID>
```

## Next Steps
1. Fix placeholder replacements in the content
2. Test with multiple states
3. Implement batch creation for all states

## File Structure
```
├── create_state_page.py    # Main script
├── FAQ.md                  # FAQ content
├── BailBondsBuddy.com _ Find Local Trusted Bail Bondsman in [state].json  # Template
└── state_pages_creation.md # This documentation
```

## Troubleshooting
If you encounter issues:
1. Check WordPress API response codes
2. Verify template JSON format
3. Ensure all placeholders use standard bracket format `[placeholder]`
4. Verify DIVI builder is enabled for the page

## Notes
- The script creates pages in DRAFT status for review
- Each page gets a unique ID from WordPress
- The template maintains all DIVI modules and styling
- Full width layout is enforced through meta settings

## API Endpoints
- Page Creation: `POST /wp-json/wp/v2/pages`
- Page Update: `POST /wp-json/wp/v2/pages/<page_id>`
- Page Status: `GET /wp-json/wp/v2/pages/<page_id>`

## Required Python Packages
```python
import requests
import random
import os
import json
import time
import traceback
import re
``` 