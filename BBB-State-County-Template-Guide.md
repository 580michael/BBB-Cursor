# Bail Bonds Buddy - State & County Template Guide

## Overview
This guide explains how to use the template system to create state and county pages using Python automation. The system uses template page ID 501 as the master template for state pages and automatically replaces placeholders with state-specific information.

## State Pages

### Template Information
- **Master Template Page ID**: 501
- **Python Script**: `test_template.py`
- **Base URL**: bailbondsbuddy.com

### Available Variables
The script automatically replaces these variables in the template:
- `[state_name]` - Name of the state (e.g., "Texas", "Oklahoma")
- `[state_capital_address]` - Full address of state capital (e.g., "Austin, TX, USA")
- `[state_capital_lat]` - Latitude of state capital (e.g., "30.2672")
- `[state_capital_lng]` - Longitude of state capital (e.g., "-97.7431")

### State-Specific Data
The script includes functions to handle:
1. State capitals and coordinates (`get_state_capital_info`)
2. Major counties for each state (`get_state_counties`)
3. State-specific map centering

### Creating State Pages
1. Edit template page (ID: 501) in WordPress to adjust:
   - Layout
   - Styling
   - Content structure
   - Global elements

2. Run the Python script:
   ```bash
   python3 test_template.py
   ```

3. The script will:
   - Pull content from template page 501
   - Replace all placeholders with state data
   - Create a new published page
   - Return the new page ID and URL

### Template Sections
1. **Blue Header Section**
   - Title: "Find Bail Bonds in [state_name]"
   - Search form
   - Interactive map centered on state capital

2. **Features Section**
   - 24/7 Availability
   - Verified Bondsmen
   - Local Coverage

3. **Counties Section**
   - Lists major counties in the state
   - Blog module for county posts

## County Pages (Template Structure)

### Recommended Template Setup
Create a new template page for counties with these modifications:

1. **Header Section**
   ```html
   <h1>Find Bail Bonds in [county_name], [state_name]</h1>
   ```

2. **Map Section**
   - Use `[county_coordinates_lat]` and `[county_coordinates_lng]`
   - Default zoom level should be higher than state pages
   - Center on county seat

3. **Search Section**
   ```html
   <input placeholder="Search for bail bondsmen in [county_name], [state_name]...">
   ```

### Suggested County Variables
- `[county_name]` - Full county name (e.g., "Harris County")
- `[county_short_name]` - County without "County" (e.g., "Harris")
- `[county_seat]` - County seat name
- `[county_seat_address]` - Full address of county seat
- `[county_coordinates_lat]` - County seat latitude
- `[county_coordinates_lng]` - County seat longitude
- `[state_name]` - Parent state name
- `[county_population]` - County population (if available)
- `[county_courts_address]` - County courts address
- `[county_jail_address]` - County jail address

### County-Specific Sections
1. **Local Information**
   - County courthouse details
   - Local jail information
   - Bond process specific to county

2. **Bondsmen Section**
   - Local licensed bondsmen
   - Service areas within county
   - 24/7 availability status

3. **Cities/Towns Section**
   - Major cities in county
   - Coverage areas
   - Local office locations

## Python Script Details

### Key Functions
1. `create_page(state_name)`
   - Creates new state page
   - Handles all replacements
   - Returns page ID

2. `get_state_capital_info(state_name)`
   - Returns capital city info
   - Includes address and coordinates

3. `get_state_counties(state_name)`
   - Returns list of major counties

### Batch Creation
To create multiple state pages:
```python
states_to_create = ["Texas", "Oklahoma", "Florida"]  # Add all states
create_pages_for_states(states_to_create)
```

### Error Handling
The script includes:
- API error handling
- Content validation
- Response verification
- Detailed error messages

## Best Practices

1. **Template Editing**
   - Always edit template 501 for global changes
   - Test with one state before batch creation
   - Verify all variables are properly replaced

2. **Content Management**
   - Keep consistent formatting
   - Use proper HTML structure
   - Maintain mobile responsiveness

3. **Map Configuration**
   - Verify coordinates for each state/county
   - Adjust zoom levels appropriately
   - Enable all necessary map controls

4. **SEO Considerations**
   - Use proper heading hierarchy
   - Include state/county in meta titles
   - Maintain unique content for each page

## Troubleshooting

### Common Issues
1. **Map Not Centering**
   - Verify coordinates in `get_state_capital_info`
   - Check map module settings
   - Ensure proper variable replacement

2. **Content Not Replacing**
   - Check variable syntax `[variable_name]`
   - Verify template ID is correct
   - Check API response for errors

3. **Page Creation Fails**
   - Verify WordPress credentials
   - Check API endpoint accessibility
   - Review error messages in script output

## Future Enhancements
1. Add more state-specific data
2. Implement county page automation
3. Add city-level page creation
4. Enhance error reporting
5. Add content validation tools

## Required WordPress Setup
1. Divi Builder enabled
2. REST API accessible
3. Proper user permissions
4. Required plugins activated

## Security Notes
- API credentials stored securely
- Rate limiting considered
- Error logging implemented
- Access controls maintained 