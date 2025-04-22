import requests
from create_hierarchical_pages import create_state_page, STATE_DATA

def test_divi_template():
    """
    Test creating a single state page using the Divi Theme Builder template.
    This will create a page for Texas that uses the 'All States Pages' template.
    """
    print("Testing creation of state page with Divi Theme Builder template...")
    state_name = "Texas"
    
    # Try creating with more debugging
    try:
        # Get state info
        state_info = STATE_DATA[state_name]
        capital_info = state_info["capital"]
        state_abbr = state_info['abbreviation']
        
        # Get the top 3 counties for this state
        top_counties = list(state_info['counties'].keys())[:3]
        
        # Create a minimal content structure with the necessary shortcode replacements
        content = f"""<!-- This page uses the Divi Theme Builder "All States Pages" template -->
        <!-- Map coordinates replacement -->
        [et_pb_map address="{capital_info['address']}" zoom_level="7" 
                address_lat="{capital_info['lat']}" address_lng="{capital_info['lng']}"]
        [/et_pb_map]
        
        <!-- State and county name replacements -->
        <p class="state-name-replacement">{state_name}</p>
        <p class="county-name-replacement">{top_counties[0]}</p>
        <p class="county-name-replacement">{top_counties[1]}</p>
        <p class="county-name-replacement">{top_counties[2]}</p>
        """
        
        # Create basic data with just the essentials
        data = {
            'title': f"Test Divi Template - {state_name}",
            'content': content,
            'status': 'publish',
            'meta': {
                '_et_pb_use_builder': 'on'
            }
        }
        
        print("Sending request with data:", data)
        
        # Constants from create_hierarchical_pages.py
        BASE_URL = "https://bailbondsbuddy.com"
        AUTH = ('bbbuddy', 'DpSm eiz8 yHjx Sqqk G3lG fqU6')
        
        # Send the request
        response = requests.post(
            f"{BASE_URL}/wp-json/wp/v2/pages",
            auth=AUTH,
            json=data
        )
        
        # Check response
        response.raise_for_status()
        page_data = response.json()
        print(f"Success! Created page with ID: {page_data['id']}")
        print(f"URL: {page_data['link']}")
        print(f"This page should be using the 'All States Pages' template from Divi Theme Builder")
    
    except Exception as e:
        print(f"Error: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response content: {e.response.content}")
        print("Failed to create test page.")

if __name__ == "__main__":
    test_divi_template() 