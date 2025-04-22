# WordPress Import Instructions for Bail Bonds Buddy State Pages

This guide will help you import the generated state pages into your WordPress site using the Divi theme.

## Option 1: Using JSON Import (Recommended)

### Prerequisites
1. Make sure you have the Divi theme activated on your WordPress site
2. Install the "Divi Import/Export" plugin if you don't already have it

### Import Steps
1. Log in to your WordPress dashboard
2. Navigate to Divi → Divi Library
3. Click on "Import & Export" in the top right
4. Select "Import" tab
5. Choose the JSON file for the state you want to import (e.g., `texas.json`)
6. Click "Import Divi Builder Layout"
7. Once imported, create a new page for the state
8. Edit the page with Divi Builder
9. Click "Load From Library" and select the imported layout
10. Save and publish the page

## Option 2: Manual Content Creation

If you prefer to create pages manually or encounter any issues with JSON import:

1. Open the HTML file for the state you want to create (e.g., `texas.html`)
2. Use it as a reference to create a new page in WordPress with Divi Builder
3. Copy the content sections from the HTML file into your Divi modules
4. Save and publish the page

## Important Notes

- Each state has unique content to avoid duplicate content penalties
- All headings include the state name for better SEO
- FAQ sections have unique questions and answers for each state
- The state-specific information (population, counties, etc.) is accurate for each state
- You may need to adjust the map module to show the correct state location

## Next Steps

After importing all state pages, you can proceed to Phase 2 of your project:
- Creating county pages for each state
- Adding maps to county courthouses
- Adding phone numbers for county jails and courthouses

## Technical Support

If you encounter any issues with the import process, you can modify the scripts in your Cursor IDE:
- `improved_page_generator_v2.py` - Main script for generating pages
- `content_generator_utils.py` - Utilities for generating unique content
- `state_data_generator.py` - Script for generating state-specific data
