# State Page Creation and Upload Guide for BailBondsBuddy.com

IMPORTANT DISCLAIMER:
BailBondsBuddy.com is an informational directory website only. We are NOT:
- Bail bondsmen
- Lawyers
- Legal advisors
- Law enforcement
- Court officials
- Government representatives

The information provided is for general informational purposes only and should NOT be considered:
- Legal advice
- Professional recommendations
- Official regulations
- State requirements
- Legal interpretations

For specific legal advice, always consult with a qualified attorney.
For bail bond services, contact a licensed bail bondsman directly.

DATA ACCURACY POLICY:
1. NO PLACEHOLDER DATA: This script must never use placeholder or made-up data.
2. ACCURATE DATA ONLY: All data must be sourced from official or verified sources:
   - State information from official state websites and government sources
   - Population data from US Census Bureau
   - County data from official county records
   - City data from official municipal sources
   - Geographic data from US Geological Survey
   - Weather data from National Weather Service
3. MISSING DATA HANDLING: If accurate data cannot be obtained:
   - Log an error explaining what data is missing
   - Halt generation for that state
   - Never substitute with placeholder or approximate data
4. DATA VERIFICATION: All data sources must be documented and verifiable
5. REGULAR UPDATES: Data must be updated when new official statistics are released

CONTENT UNIQUENESS REQUIREMENTS:
1. NO DUPLICATE CONTENT: Each state page must have completely unique content:
   - Never copy and paste content from other state pages
   - Never use the same descriptions or explanations
   - Never reuse the same examples or scenarios
   - Never duplicate FAQ answers or explanations
   - Each section must be completely rewritten with unique content:
     * Introduction paragraphs
     * Three icon sections (24/7 Availability, Verified Bondsman, Nationwide Coverage)
     * State description section
     * FAQ section
     * State overview section

2. UNIQUE STATE-SPECIFIC CONTENT:
   - Each state's description must be written from scratch
   - Use state-specific statistics and demographics
   - Include unique state laws and regulations
   - Reference state-specific landmarks and geography
   - Mention state-specific industries and economy
   - Include state-specific bail bond requirements
   - Each section must maintain the same logical structure but with completely different content:
     * Introduction: Focus on state-specific legal landscape and challenges
     * 24/7 Availability: Highlight state-specific locations and conditions
     * Verified Bondsman: Emphasize state-specific licensing and requirements
     * Nationwide Coverage: Detail state-specific coverage areas and facilities
     * FAQ: Address state-specific questions and concerns
     * State Overview: Provide unique state-specific information and context

3. CONTENT VERIFICATION:
   - Verify uniqueness against existing pages
   - Ensure no duplicate paragraphs or sections
   - Check for unique state-specific terminology
   - Compare each section with other state pages to ensure complete uniqueness
   - Verify that only the logical structure remains the same, not the content

4. WRITING GUIDELINES:
   - Write in a unique voice for each state
   - Use different sentence structures
   - Vary paragraph organization
   - Include state-specific examples
   - Reference local landmarks and cities
   - Use state-specific terminology
   - Maintain the same section structure but with completely different content
   - Each section should tell a unique story about the state's bail bond system

5. SECTION-SPECIFIC REQUIREMENTS:
   - Introduction: Must be completely unique while maintaining the same focus on urgency and state-specific challenges
   - Three Icon Sections: Each must have unique content while keeping the same logical structure
   - State Description: Must be entirely unique while maintaining the same comprehensive coverage
   - FAQ Section: Each question must have a unique answer specific to the state
   - State Overview: Must provide unique information while maintaining the same depth of coverage

6. CONTENT CREATION PROCESS:
   - Research state-specific information thoroughly
   - Create unique content for each section
   - Verify no content is duplicated from other state pages
   - Ensure each section maintains the same logical structure
   - Review the entire page for uniqueness
   - Compare with other state pages to confirm complete uniqueness

EXCLUDED STATES (No Commercial Bail Bonds):
The following states do not allow commercial bail bondsmen and should NOT have pages generated:
- Illinois (abolished cash bail in September 2023)
- Kentucky (banned since 1976)
- Maine
- Massachusetts (effectively ended as of 2014)
- Nebraska
- Oregon (banned since 1974)
- Wisconsin
Additionally, Washington D.C. prohibits commercial bail bonds.


## Directory Structure
```
Combined Json State Files/
├── Generated_State_Pages/          # Contains all state HTML and JSON files
│   ├── alabama.html
│   ├── alabama.json
│   ├── alaska.html
│   ├── alaska.json
│   └── ... (all other state files)
├── alabama.json                    # Example completed state page
├── upload_state_page.py           # Upload script
├── Template-Only----Oklahoma Bail Bondsman Emergency 24_7 Service _ BailBondsBuddy.com.json  # Base template
└── Edit-Rewrite-Template-LoadWP-StatePages.md  # This guide
```

## Step 1: Creating a New State Page

### Template Components
The state page JSON consists of these main sections:
- Context (et_builder)
- Data (contains the Divi builder content)
- Global colors
- Images

### Required Edits for Each State
1. **State Name References**
   - Page title: "Find Local [STATE] Bail Bondsmen Near You | 24/7 Emergency Service"
   - H1 heading: "Find Local [STATE] Bail Bondsmen Near You 24/7 Jail Release Services"
   - H2 subheading: "Find Licensed [STATE] Bail Bond Agents Available Now"

2. **Map Component**
   - Update address to state capital: `address="[CAPITAL CITY], [STATE], USA"`
   - Update coordinates: `address_lat="[LAT]" address_lng="[LONG]"`

3. **State Description Section**
   - Write completely unique content for each state
   - Include state-specific:
     - Nickname and history
     - Population data and demographics
     - Number of counties and major cities
     - Economic information and industries
     - Geographic features and climate
     - Bail bond regulations and requirements
     - Local court systems and procedures
     - State-specific challenges and solutions
     - Recent legal changes and reforms
     - Local resources and support systems

4. **File Naming**
   - Save as lowercase: `[state].json`
   - Example: `alabama.json`

### JSON Formatting Requirements
When creating or editing the JSON file:
1. Ensure proper JSON structure with:
   - Opening and closing curly braces `{}`
   - Proper nesting of objects and arrays
   - Correct comma placement between elements
2. Validate JSON before saving using a JSON validator
3. Avoid extra data or characters at the end of the file
4. Maintain consistent indentation for readability

## Step 2: Uploading to WordPress

### Using the Upload Script
1. Navigate to the Combined Json State Files directory:
```bash
cd "Combined Json State Files"
```

2. Run the upload script:
```bash
python3 upload_state_page.py StateName
```
Example:
```bash
python3 upload_state_page.py Alabama
```

### What the Script Does
1. Locates the JSON file in the current directory
2. Extracts the page content
3. Creates a WordPress page with:
   - Title: "Find Local [State] Bail Bondsmen Near You | 24/7 Emergency Service"
   - Slug: "[state]-bail-bondsman-24-hour-emergency-service-nearby"
   - Status: Draft
   - Divi Builder enabled
   - No sidebar layout

### After Upload
1. WordPress creates a new page and returns:
   - Page ID
   - Preview Link
   - Edit Link
2. Review the page in WordPress admin
3. Make any final adjustments
4. Publish when ready

## Example Output
```
Looking for JSON file at: /path/to/Combined Json State Files/alabama.json
Uploading Alabama page to WordPress...

Success! Alabama page uploaded to WordPress
Page ID: 1160
Preview Link: https://bailbondsbuddy.com/?page_id=1160&preview=true
Edit Link: https://bailbondsbuddy.com/wp-admin/post.php?post=1160&action=edit
```

## Common Issues and Solutions
1. **File Not Found Error**
   - Ensure JSON file is in the Combined Json State Files directory
   - Check file name is lowercase
   - Verify file extension is .json

2. **Invalid JSON Structure**
   - Verify JSON has required sections:
     - context
     - data
     - presets
     - global_colors
   - Check for proper JSON formatting:
     - No extra data at the end of the file
     - Proper nesting of objects and arrays
     - Correct comma placement
   - Use a JSON validator to check syntax

3. **Upload Timeout**
   - Script has 30-second timeout
   - Check internet connection
   - Retry upload

4. **Duplicate Content Detection** 
   - Compare with existing state pages
   - Ensure unique state-specific information
   - Verify different writing style and structure

## Next Steps
1. Create JSON files for remaining states using template
2. Write unique content for each state
3. Update state-specific information
4. Upload each state page
5. Review and publish in WordPress

## Generated State Pages
The `