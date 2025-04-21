"""
State Data Structure for Bail Bonds Buddy Website

This file defines the structure for state-specific data needed to generate
unique content for each state page on the BailBondsBuddy.com website.
"""

# Example structure based on Oklahoma page
STATE_TEMPLATE = {
    "name": "",                    # Full state name
    "abbreviation": "",            # Two-letter state abbreviation
    "nickname": "",                # State nickname (e.g., "The Sooner State")
    "capital": "",                 # State capital city
    "population": 0,               # Approximate state population
    "num_counties": 0,             # Number of counties in the state
    "largest_counties": [          # List of 3 largest counties
        {"name": "", "description": ""},
        {"name": "", "description": ""},
        {"name": "", "description": ""}
    ],
    "major_cities": [],            # List of major metropolitan areas
    "economy": "",                 # Description of state economy
    "bail_system": "",             # Description of state bail bond system
    "criminal_justice": "",        # Criminal justice context and reforms
    "geography": "",               # Geographical considerations affecting bail
    "weather": "",                 # Weather factors affecting court schedules
    "faqs": [                      # 5 unique FAQs for each state
        {"question": "", "answer": ""},
        {"question": "", "answer": ""},
        {"question": "", "answer": ""},
        {"question": "", "answer": ""},
        {"question": "", "answer": ""}
    ]
}

# Example of Oklahoma data (based on existing page)
OKLAHOMA_DATA = {
    "name": "Oklahoma",
    "abbreviation": "OK",
    "nickname": "The Sooner State",
    "capital": "Oklahoma City",
    "population": 4000000,
    "num_counties": 77,
    "largest_counties": [
        {"name": "Oklahoma County", "description": ""},
        {"name": "Tulsa County", "description": ""},
        {"name": "Cleveland County", "description": ""}
    ],
    "major_cities": ["Oklahoma City", "Tulsa"],
    "economy": "Oklahoma's economy has traditionally centered around energy production, with oil and natural gas remaining significant industries. However, recent economic diversification has expanded into aerospace, biotechnology, telecommunications, and healthcare.",
    "bail_system": "The state maintains a robust bail system governed by the Oklahoma Bail Bondsmen Act, which requires all bondsmen to be licensed through the Oklahoma Insurance Department. Oklahoma law establishes standard premium rates (typically 10% of the bail amount) and regulates bondsman practices to protect consumers during vulnerable times.",
    "criminal_justice": "Recent criminal justice reform initiatives in Oklahoma have aimed to reduce the state's historically high incarceration rate, which has long ranked among the nation's highest. These reforms have modified certain bail procedures, especially for non-violent offenses, making professional guidance from experienced bondsmen even more valuable for navigating the changing legal landscape.",
    "geography": "Oklahoma's geographical positioning along major interstate highways (I-35, I-40, and I-44) has unfortunately made it a corridor for drug trafficking, resulting in significant numbers of drug-related arrests requiring bail services. Meanwhile, the state's diverse population – including substantial Native American communities – introduces jurisdictional complexities that knowledgeable bail bondsmen must understand.",
    "weather": "Weather emergencies, from tornadoes to ice storms, can occasionally impact court schedules and bail processing timelines. Local bondsmen familiar with Oklahoma's systems know how to manage these disruptions while ensuring clients meet all legal obligations.",
    "faqs": [
        {
            "question": "How long does it take to get released using a bail bond?",
            "answer": "After a bail bond is posted, release times typically range from 2-8 hours depending on the facility's processing speed and how busy they are. Weekend and holiday arrests may take longer to process. The bondsman will keep you updated on the progress."
        },
        {
            "question": "What kind of collateral is accepted for bail bonds?",
            "answer": ""
        },
        {
            "question": "What is the typical cost of a bail bond?",
            "answer": ""
        },
        {
            "question": "What information do I need when contacting a bail bondsman?",
            "answer": ""
        },
        {
            "question": "What types of payments do bail bondsmen accept?",
            "answer": ""
        }
    ]
}
