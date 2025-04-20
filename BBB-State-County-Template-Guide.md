# Bail Bonds Buddy Template Guide

This guide outlines the structure and components used in the BBB template system for creating state, county, and city pages.

## Modular Template Structure

The template system uses Divi Builder to create consistent, modular pages with the following components:

### State Page Components
1. **Header Section** - Title and introduction to state bail bond services
2. **Blue CTA Section** - "Need a Bail Bondsman" with call button
3. **Information Section** - "How Bail Bonds Work in [state]"
4. **County Listing** - Displays the top counties with links to county pages
5. **Services Section** - Features grid showing available bail bond services
6. **Map Section** - Shows the state capital location with Google Maps
7. **FAQ Section** - Displays dynamic, state-specific bail bond questions

### County Page Components
1. **Header Section** - County-specific title and introduction
2. **Blue CTA Section** - Same as state page but county-specific
3. **Information Section** - County-specific bail bond information
4. **City Listing** - Lists cities in the county with links to city pages
5. **Jail Information** - Details about the county jail facilities
6. **Map Section** - Shows the county seat location
7. **FAQ Section** - County-specific questions

### City Page Components
1. **Header Section** - City-specific title and introduction
2. **Blue CTA Section** - City-specific call to action
3. **Local Services** - Information about local bail bondsmen
4. **Navigation Section** - Links back to county and state pages
5. **Map Section** - Shows the city location
6. **FAQ Section** - City-specific questions

## Dynamic Content Replacement

The template system dynamically replaces placeholders with location-specific content:

- `{state_name}` - Name of the state (e.g., "Oklahoma")
- `{counties[0]}`, `{counties[1]}`, etc. - County names
- `{capital['name']}` - State capital name
- `{capital['address']}` - State capital address
- `{capital['lat']}` and `{capital['lng']}` - Map coordinates

## FAQ Integration

FAQs are loaded from a central FAQ.md file and customized for each location:

- `[state_name]` - Replaced with the current state name
- `[premium_rate]` - Dynamic bail bond premium rate (typically "10" or "15")
- `[recent_state_change]` - Recent bail legislation or practice changes
- `[state_specific_factor]` - Location-specific bail considerations

## SEO Optimization

Each page includes optimized elements:

- **Title** - Format: "Bail Bonds in [Location] | Local [Keyword] Services"
- **Slug** - Format: "bail-bonds-in-[location]-[abbreviation]"
- **Meta Description** - Dynamic description with location and keyword variations

## Scripts and Tools

### state_page_creator.py
- Creates state pages with modular components
- Uses STATE_DATA dictionary for location information
- Dynamically selects and customizes FAQs
- Handles SEO elements and slug creation

### create_hierarchical_pages.py
- Creates complete hierarchy of state, county, and city pages
- Maintains proper navigation between related pages
- Uses same modular component approach

## Best Practices

1. Test new pages before mass creation
2. Verify links between pages work correctly
3. Check that maps are centered properly
4. Ensure county and city lists are accurate
5. Validate that all placeholders are replaced

## Original Guide Content

## Overview
This guide explains how to use the template system to create state and county pages using Python automation. The system uses template page ID 501 as the master template for state pages and automatically replaces placeholders with state-specific information.

## State Pages

### Template Information
- **Master Template Source**: Divi Theme Builder → All States Pages → Custom Body
- **Python Script**: `create_hierarchical_pages.py`
- **Base URL**: bailbondsbuddy.com

### Available Variables
The script automatically replaces these variables in the template:
- `[state_name]` - Name of the state (e.g., "Texas", "Oklahoma")
- `[state_capital_address]` - Full address of state capital (e.g., "Austin, TX, USA")
- `[state_capital_lat]` - Latitude of state capital (e.g., "30.2672")
- `[state_capital_lng]` - Longitude of state capital (e.g., "-97.7431")
- `[county_name]` - County names (repeats for each county displayed)

### State-Specific Data
The script includes functions to handle:
1. State capitals and coordinates
2. Major counties for each state
3. State-specific map centering

### Creating State Pages
The current implementation:
1. Uses the `create_state_page` function in `create_hierarchical_pages.py`
2. Creates Divi Builder content with proper shortcodes
3. Dynamically replaces state and county names
4. Sets map coordinates based on the state capital

## Technical Implementation

### Implementation Issues Discovered
When comparing the Theme Builder template to generated pages:

1. **Template Changes**: Changes made to the Divi Theme Builder template don't automatically propagate to pages created previously
   - This suggests we need to use Divi's Global Modules or Saved Layouts

2. **Content Differences**: Some content in the template isn't appearing in generated pages
   - We need to ensure all sections from the template are included in our generated content

3. **Button Functionality**: The "View Bondsman" buttons need proper URLs to county pages
   - We should modify our script to include proper URLs

### Script Updates
We've modified `create_state_page` to:
1. Create full Divi Builder shortcode content
2. Include dynamic state and county replacements
3. Set proper meta fields to enable Divi Builder

### Example Code
```python
def create_state_page(state_name, template_content=None):
    """Create a state page that uses the Divi Theme Builder template"""
    try:
        # Get state info
        state_info = STATE_DATA[state_name]
        capital_info = state_info["capital"]
        
        # Create Divi Builder content with state-specific data
        content = f"""[et_pb_section fb_built="1" _builder_version="4.27.4" ...]
            <h1>Find Local Bail Bondsmen in {state_name}</h1>
            ...
            [et_pb_heading title="{top_counties[0]}" ...]
            ...
        """
        
        # Create the page with Divi Builder meta fields
        data = {
            'title': page_title,
            'content': content,
            'status': 'publish',
            'meta': {
                '_et_pb_use_builder': 'on',
                '_et_pb_old_content': '',
                '_et_pb_post_type_layout': 'et_body_layout',
                ...
            }
        }
        
        # API request to create the page
        response = requests.post(...)
```

## Required Divi Configuration
For optimal template usage, we need to ensure:

1. **Global Elements**: Convert key design elements to Divi Global modules
2. **Proper Theme Builder Setup**: Ensure the "All States Pages" template is correctly configured
3. **Layout Library Usage**: Save sections as Divi Library items for consistent reuse

## Next Steps

### Technical Improvements
1. **Read Divi Documentation**: Understand proper template inheritance
2. **Test Template Changes**: Make a change to the template and see if it propagates
3. **Setup Global Modules**: For elements that should update everywhere
4. **Fix Button Links**: Ensure county buttons link to the right places
5. **Restore Missing Content**: Identify and restore any missing paragraphs

### Future Development
1. Apply same approach to county and city pages
2. Create test harness to verify template changes propagate
3. Document the final solution for future reference

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

## Content Variation Strategy for 50 State Pages

### Available Data in USA_DATA Structure
The project includes extensive state and county data in the `USA_DATA` directory:
- All 50 state directories (e.g., `/TX`, `/OK`, `/CA`)
- County-level data for each state, including:
  - County directories (e.g., `TX/counties/Travis-County`)
  - County seats (e.g., `tx-county-seats.json`)
  - City lists for each county (e.g., `travis-county-cities.txt`)

### Core State Variables
```json
{
  "state_name": "Texas",
  "state_nickname": "The Lone Star State",
  "top_counties": ["Harris County", "Dallas County", "Bexar County"],
  "major_cities": ["Houston", "Dallas", "San Antonio", "Austin"],
  "state_population": "29 million"
}
```

### General Process Variables (Non-Legal)
```json
{
  "typical_processing_time": "several hours to days",
  "common_payment_methods": ["cash", "credit cards", "payment plans"],
  "bond_fee_percentage": "typically 10-15%"
}
```

### Recommended Variation Count
For 50 unique state pages that avoid duplication penalties while maintaining efficiency:
- **Introduction variations**: 5-6 different templates
- **Process information**: 4-5 variations
- **Financial considerations**: 4-5 variations  
- **Local knowledge sections**: 4-5 variations
- **Support/guidance paragraphs**: 3-4 variations
- **Call-to-action closings**: 3-4 variations

### Content Placement Strategy
For natural content that isn't over-optimized:
- **H1 title**: Include `[state_name]` (e.g., "Find Bail Bonds in [state_name]")
- **First paragraph**: 1 mention of `[state_name]`
- **H2 subheading**: 1 mention where appropriate
- **Body**: Occasional natural mentions (1-2 total) + references to local counties/cities
- **Conclusion**: 1 final mention of `[state_name]`

### Example Paragraph Variations

#### Introduction Variations
```
When someone you care about is detained in [state_name], every hour matters. Connecting with a local bail bondsman can help navigate this challenging situation and potentially speed up the release process. Families across the region have found that professional assistance makes a significant difference during these difficult times.
```

```
The moments following a loved one's detention are crucial. Throughout [state_name], bail bondsmen serve as essential resources for families facing this unexpected situation. Their familiarity with local facilities in places like [major_cities[0]] and [major_cities[1]] can help reunite families more quickly.
```

#### Local Knowledge Variations
```
Local knowledge matters when navigating detention procedures. Bondsmen who regularly work with facilities in [top_counties[0]], [top_counties[1]], and neighboring counties understand important differences that can save families considerable time and confusion during the process.
```

```
Counties like [top_counties[0]] and [top_counties[2]] each operate their facilities differently. Bondsmen familiar with these local systems can help families navigate the process more efficiently than those attempting to figure it out on their own for the first time.
```

### Implementation Strategy
1. Create a JSON file with all state data (using existing data from USA_DATA)
2. Develop a template library with all paragraph variations (stored as a second JSON file)
3. For each state page:
   - Randomly select one variation from each content section
   - Ensure no two neighboring states use identical pattern combinations
   - Insert state-specific data into the selected templates

### Technical Implementation
This can be managed through the existing Python script by:
1. Loading both the state data and paragraph template libraries
2. Creating a function to build unique combinations for each state
3. Tracking which combinations have been used to avoid duplication

### Extra Uniqueness for Competitive States
For high-competition states (CA, TX, FL, NY), consider:
- 1-2 completely unique paragraphs written specifically for that state
- Additional local references beyond the standard variables
- Slightly longer content with more regional details

## Keyword and URL Strategy

### Keyword Structure
The site uses two CSV files to generate consistent yet varied keyword combinations:

1. **z-Keyword.csv**: Principal keywords for bail bond services such as:
   - Bail-Bonds
   - Bondsman
   - Bail-Bondsman
   - Bail-Bond-Agent
   - Bail-Services
   - Bail-Agencies
   - Bail-Bond-Companies

2. **z-ModifierKeyword.csv**: Modifier keywords that describe the services:
   - 24-Hour
   - Affordable
   - Local
   - Fast
   - Emergency
   - Express
   - Licensed
   - Professional

### URL Structure
The site follows a hierarchical URL pattern that incorporates location and keywords:

1. **State Pages**:
   ```
   bailbondsbuddy.com/[ModifierKeyword]-[Keyword]-[FullState]
   ```
   Example: `bailbondsbuddy.com/24Hour-Bail-Bondsman-in-Oklahoma`

2. **County Pages**:
   ```
   bailbondsbuddy.com/[2LetterState]/[County]/[ModifierKeyword]-[Keyword]-[FullState]
   ```
   Example: `bailbondsbuddy.com/OK/Pontoc-County/24Hour-Bail-Bondsman-in-Oklahoma`

3. **City Pages**:
   ```
   bailbondsbuddy.com/[2LetterState]/[County]/[ModifierKeyword]-[Keyword]-[City]-[FullState]
   ```
   Example: `bailbondsbuddy.com/OK/Pontoc-County/24Hour-Bail-Bondsman-in-Ada-Oklahoma`

### WordPress Implementation
To implement this URL structure in WordPress:
1. Set permalink structure to custom: `/%postname%/`
2. Use the `post_name` parameter in API requests when creating pages
3. Ensure the Python script generates appropriate slugs based on the URL pattern

## SEO Strategy

### Keyword Optimization
- Use **exact phrase match** targeting for search queries
- Select different keyword combinations for each page using the CSV files
- Include location-specific keywords in titles, headings, and content
- Use keyword variations naturally throughout the content

### On-Page SEO Elements
1. **Meta Information**:
   - Create unique meta titles: `[ModifierKeyword] [Keyword] in [Location] | Bail Bonds Buddy`
   - Write compelling meta descriptions with call-to-action
   - Implement proper canonical URLs

2. **Content Structure**:
   - Use H1 for main title with primary keyword and location
   - Include H2 and H3 headings with secondary keywords
   - Add location-specific information relevant to bail bonds
   - Maintain at least 500 words of unique content per page

3. **Technical SEO**:
   - Implement schema.org structured data for local businesses
   - Generate comprehensive XML sitemaps (split into smaller chunks)
   - Create a proper robots.txt file
   - Ensure mobile responsiveness

## Interlinking Strategy

### Hierarchical Structure
1. **City Pages** will link to:
   - Two other city pages in the same county
   - Parent county page (breadcrumb navigation)
   - Links should open in a new tab

2. **County Pages** will link to:
   - Two other county pages in the same state
   - Two city pages within the county
   - Parent state page (breadcrumb navigation)
   - Homepage (https://bailbondsbuddy.com)
   - Links should open in a new tab

3. **State Pages** will link to:
   - Three major county pages within the state
   - Homepage (https://bailbondsbuddy.com)
   - Links should open in a new tab

### Implementation in Templates
To add these links within the WordPress template:
1. Include a "Related Pages" section in each template
2. Add the following to the template content:
   ```html
   <div class="related-pages">
     <h3>Related Resources</h3>
     <ul>
       <li><a href="[link_url_1]" target="_blank">[ModifierKeyword] [Keyword] in [Location1]</a></li>
       <li><a href="[link_url_2]" target="_blank">[ModifierKeyword] [Keyword] in [Location2]</a></li>
     </ul>
   </div>
   ```
3. The Python script should replace the placeholders with appropriate links

## Content Generation Implementation

### Template Variation
For maximum content uniqueness:
1. Create 5-7 different content templates for each page type (state, county, city)
2. Combine with the paragraph variations described earlier
3. Rotate templates to avoid duplicate content across pages

### Content Template Selection
In the Python script, implement a template selection function:
```python
def select_template(location_type, location_name):
    """
    Selects an appropriate template based on location type and name.
    Ensures variety across pages.
    
    Args:
        location_type: "state", "county", or "city"
        location_name: Name of the location
    
    Returns:
        template_id: ID of the selected template
    """
    # Implementation logic here
```

### Keyword Selection
Add a function to select varied keyword combinations:
```python
def select_keywords(location_type, location_name):
    """
    Select appropriate keyword combinations based on location.
    
    Args:
        location_type: "state", "county", or "city"
        location_name: Name of the location
    
    Returns:
        keyword_dict: Dictionary with selected keywords
    """
    # Implementation logic here
```

### Integration with Existing Script
Modify the existing `create_page` function to incorporate these strategies:
```python
def create_page(location_type, location_name, state_abbr=None, county_name=None):
    """
    Creates a page for the specified location using appropriate templates and keywords.
    
    Args:
        location_type: "state", "county", or "city"
        location_name: Name of the location
        state_abbr: Two-letter state abbreviation (required for county and city)
        county_name: County name (required for city)
    
    Returns:
        page_id: ID of the created page
        page_url: URL of the created page
    """
    # Get location data
    # Select template
    # Select keywords
    # Generate content with variations
    # Create page via WordPress API
    # Return results
```

## Implementation Roadmap

1. **Phase 1: Template Setup** (Current)
   - Finalize state page template
   - Create county page template
   - Set up content variation system

2. **Phase 2: Oklahoma Pilot**
   - Implement full URL structure
   - Generate all Oklahoma state, county, and major city pages
   - Test and refine process

3. **Phase 3: National Rollout**
   - Apply template to all 50 states
   - Prioritize high-traffic states (TX, CA, FL, NY)
   - Monitor performance and adjust

4. **Phase 4: Optimization**
   - Add more local data to high-performing pages
   - Enhance interlinking based on analytics
   - Expand city coverage based on demand 

## Implementation Details

### Page Creation Order and Interlinking

For effective implementation of the interlinking strategy, a two-phase approach is recommended:

#### First Phase - Create All Page Shells
```python
def create_page_shells():
    """Create basic versions of all pages with essential metadata"""
    # For each state, county, city
    # Generate and set:
    #   - Title
    #   - Meta description
    #   - URL slug
    #   - Minimal placeholder content
    #   - Status = Published
```

1. Create all pages with basic structure first:
   - Include titles, metadata, and minimal content
   - Set proper URL slugs following the hierarchy
   - Don't include internal links yet
   - This ensures all pages are indexed with basic SEO elements

#### Second Phase - Complete Content and Links
```python
def update_pages_with_content_and_links():
    """Add complete content and internal links to all pages"""
    # For each state, county, city
    # Now that all pages exist:
    #   - Add full template content
    #   - Include proper internal links to other pages
    #   - Update with final versions of all elements
```

2. Once all pages exist, run a second script pass:
   - Add full content to each page
   - Add proper internal links to now-existing pages
   - This ensures all link targets exist
   - Complete breadcrumb navigation

### Keyword Combination Logic

To ensure logical keyword combinations that make sense to readers and search engines:

#### Preventing Illogical Combinations
```python
def is_valid_combination(modifier, keyword):
    """Check if a modifier-keyword combination makes logical sense"""
    
    # Define incompatible combinations
    invalid_combinations = {
        "Fast": ["Bail-Bond-Firm", "Bail-Bond-Company", "Bail-Bond-Organization"],
        "Cheap": ["Premier", "Expert", "Professional", "Premium"],
        "Affordable": ["High-Quality", "Premium", "Elite"],
        "24-Hour": ["Bail-Bond-Firm", "Bail-Bonds-Institution"],
        "Emergency": ["Bail-Bond-Center", "Bail-Bonds-Association"],
        "Express": ["Bail-Bond-Consultation", "Bail-Bonds-Organization"],
        "Mobile": ["Bail-Bond-Desk", "Bail-Bonds-Center"],
        # Add other incompatible pairs as needed
    }
    
    # Check if this combination should be rejected
    if modifier in invalid_combinations and keyword in invalid_combinations[modifier]:
        return False
        
    return True
```

#### Adding Connecting Words
```python
def format_title(modifier, keyword, location):
    """Format page title with proper connecting words"""
    
    # Format based on keyword type
    if keyword.startswith("Bail"):
        return f"{modifier} {keyword} in {location}"
    elif keyword.endswith("Bondsman"):
        return f"{modifier} {keyword} in {location}"
    else:
        return f"{modifier} Bail {keyword} in {location}"
        
    # Special cases can be handled individually
    special_cases = {
        "Bondsman": f"{modifier} Bail Bondsman in {location}",
        "Bondsman-Near-Me": f"{modifier} Bail Bondsman Near Me in {location}",
        # Add other special cases
    }
    
    if keyword in special_cases:
        return special_cases[keyword]
```

#### Sample Keyword Selection Function
```python
def select_keywords(location_type, location_name):
    """
    Select appropriate keyword combinations based on location.
    Ensures combinations make logical sense.
    """
    # Load keywords from CSV files
    with open('z-Keyword.csv', 'r') as f:
        keywords = [line.strip() for line in f.readlines()[1:]]  # Skip header
        
    with open('z-ModifierKeyword.csv', 'r') as f:
        modifiers = [line.strip() for line in f.readlines()[1:]]  # Skip header
    
    # For deterministic but varied selection
    # Use location name hash to seed random selection
    import hashlib
    seed = int(hashlib.md5(location_name.encode()).hexdigest(), 16) % 1000000
    import random
    rand = random.Random(seed)
    
    # Try combinations until finding valid one
    while True:
        modifier = rand.choice(modifiers)
        keyword = rand.choice(keywords)
        
        if is_valid_combination(modifier, keyword):
            break
    
    return {
        'modifier': modifier,
        'keyword': keyword,
        'title': format_title(modifier, keyword, location_name),
        'slug': create_slug(modifier, keyword, location_name)
    }
```

### URL Structure Implementation

Several approaches can be used to implement the hierarchical URL structure in WordPress:

#### 1. Custom Rewrite Rules
Add to functions.php or a custom plugin:
```php
function custom_rewrite_rules() {
    // State level: /state-name/
    add_rewrite_rule(
        '^([^/]+)/?$',
        'index.php?pagename=$matches[1]',
        'top'
    );
    
    // County level: /ST/county-name/
    add_rewrite_rule(
        '^([A-Z]{2})/([^/]+)/?$',
        'index.php?pagename=$matches[1]/$matches[2]',
        'top'
    );
    
    // City level: /ST/county-name/city-page/
    add_rewrite_rule(
        '^([A-Z]{2})/([^/]+)/([^/]+)/?$',
        'index.php?pagename=$matches[1]/$matches[2]/$matches[3]',
        'top'
    );
}
add_action('init', 'custom_rewrite_rules');
```

#### 2. Create State Directories First
Before creating county and city pages, establish the state-level structure:
```python
def create_state_url_structure():
    """Create all state-level URLs/directories"""
    
    states = {
        'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 
        # Add all states
    }
    
    for abbr, name in states.items():
        # Create state directory/page
        create_state_page(abbr, name)
```

#### URL and Slug Capitalization
```python
def create_proper_slug(modifier, keyword, location_type, location):
    """Create properly formatted slug with appropriate formatting"""
    
    # For title display: Capitalize words properly
    title_words = []
    for word in f"{modifier} {keyword} in {location}".split():
        if word.lower() not in ['in', 'of', 'the', 'and', 'for']:
            title_words.append(word.capitalize())
        else:
            title_words.append(word.lower())
    
    title = " ".join(title_words)
    
    # For URL slug based on location type
    if location_type == "state":
        slug = f"{modifier.lower()}-{keyword.lower()}-in-{location.lower().replace(' ', '-')}"
    elif location_type == "county":
        state_abbr = get_state_abbr(location)
        county_name = get_county_name(location)
        slug = f"{state_abbr}/{county_name.replace(' ', '-')}/{modifier.lower()}-{keyword.lower()}-in-{location.lower().replace(' ', '-')}"
    else:  # city
        state_abbr = get_state_abbr(location)
        county_name = get_county_for_city(location)
        slug = f"{state_abbr}/{county_name.replace(' ', '-')}/{modifier.lower()}-{keyword.lower()}-in-{location.lower().replace(' ', '-')}"
    
    return title, slug
```

### Process Flow Implementation

A detailed step-by-step process for implementation:

#### 1. Setup Phase
- Configure WordPress permalink structure to `/%postname%/`
- Test custom URL patterns work correctly
- Verify API access and permissions
- Load and validate the USA_DATA structure

#### 2. Content Template Preparation
- Create and test template variations
- Build keyword selection functions
- Implement template selection logic

#### 3. State URL Structure Creation
```python
def initialize_state_url_structure():
    """Create the basic state URL structure"""
    states = load_state_data()
    
    for state_abbr, state_info in states.items():
        state_name = state_info['name']
        
        # Create basic state page without links
        keywords = select_keywords("state", state_name)
        page_title = keywords['title']
        page_slug = keywords['slug']
        
        # Create minimal state page
        create_minimal_page(
            title=page_title,
            slug=page_slug,
            content=get_basic_state_content(state_name),
            meta_description=f"Find reliable bail bondsmen in {state_name}. 24/7 bail bond services available for all counties."
        )
        
        print(f"Created state URL structure for {state_name}")
```

#### 4. First Pass: Create All Page Shells
```python
def create_all_page_shells():
    """Create basic versions of all county and city pages"""
    states = load_state_data()
    
    for state_abbr, state_info in states.items():
        state_name = state_info['name']
        counties = load_counties(state_abbr)
        
        # For each county
        for county_name, county_info in counties.items():
            # Create county page shell
            county_keywords = select_keywords("county", county_name)
            county_page_title = county_keywords['title']
            county_page_slug = county_keywords['slug']
            
            create_minimal_page(
                title=county_page_title,
                slug=county_page_slug,
                content=get_basic_county_content(county_name, state_name),
                meta_description=f"Find {county_keywords['modifier'].lower()} bail bondsmen in {county_name}, {state_name}. Available 24/7 for your bail bond needs."
            )
            
            # For priority cities in county
            cities = load_cities(state_abbr, county_name)
            for city_name in cities[:10]:  # Top 10 cities per county
                # Create city page shell
                city_keywords = select_keywords("city", city_name)
                city_page_title = city_keywords['title']
                city_page_slug = city_keywords['slug']
                
                create_minimal_page(
                    title=city_page_title,
                    slug=city_page_slug,
                    content=get_basic_city_content(city_name, county_name, state_name),
                    meta_description=f"Looking for {city_keywords['modifier'].lower()} bail bondsmen in {city_name}, {state_name}? Connect with local bail bond agents 24/7."
                )
```

#### 5. Second Pass: Complete Content and Links
```python
def complete_all_pages():
    """Add full content and internal links to all pages"""
    # Now that all pages exist, we can correctly set up internal links
    
    # Get all created pages
    state_pages = get_all_state_pages()
    county_pages = get_all_county_pages()
    city_pages = get_all_city_pages()
    
    # Process state pages
    for state_page in state_pages:
        state_name = extract_state_from_page(state_page)
        
        # Get county pages for this state
        related_counties = get_county_pages_for_state(state_name)
        homepage_url = "https://bailbondsbuddy.com"
        
        # Select template and create full content with links
        template = select_template("state", state_name)
        content = generate_state_content(
            template=template,
            state_name=state_name,
            county_links=related_counties[:3],  # Top 3 counties
            homepage_url=homepage_url
        )
        
        # Update the page with full content
        update_page_content(state_page['id'], content)
    
    # Similarly process county and city pages with appropriate links
```

#### 6. Verification Process
```python
def verify_pages():
    """Check for issues with created pages"""
    # Check for 404s
    check_all_internal_links()
    
    # Verify indexability
    check_robots_txt_rules()
    
    # Ensure sitemap is complete
    verify_sitemap_includes_all_pages()
    
    # Report any issues found
    print_verification_report()
```

### Tracking and Monitoring

To maintain control over the page creation process:

```python
def track_page_creation():
    """Track and log all page creation activities"""
    # Create logs directory if not exists
    os.makedirs("page_creation_logs", exist_ok=True)
    
    # Log files
    state_log = "page_creation_logs/states.csv"
    county_log = "page_creation_logs/counties.csv"
    city_log = "page_creation_logs/cities.csv"
    
    # Headers if files don't exist
    for log_file in [state_log, county_log, city_log]:
        if not os.path.exists(log_file):
            with open(log_file, "w") as f:
                f.write("id,title,url,status,created_date\n")
    
    # For each created page, log its details
    with open(log_file, "a") as f:
        f.write(f"{page_id},{page_title},{page_url},{status},{datetime.now()}\n")
```

### Error Handling and Recovery

For a robust implementation that can handle interruptions:

```python
def implement_error_recovery():
    """Set up error handling and recovery processes"""
    
    # Load previously created pages to avoid duplication
    existing_pages = load_creation_logs()
    
    # Process only missing pages
    pages_to_create = get_pages_not_in_logs(all_pages, existing_pages)
    
    # For each batch of pages
    for batch in chunks(pages_to_create, 50):  # Process in batches of 50
        try:
            # Create batch
            create_page_batch(batch)
            
            # Log successful batch
            log_successful_batch(batch)
            
        except Exception as e:
            # Log error
            log_error(batch, str(e))
            
            # Wait and retry failed batch
            time.sleep(60)  # Wait 1 minute
            retry_failed_batch(batch)
``` 