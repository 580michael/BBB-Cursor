import json
import random
import os

# Create directory for state data if it doesn't exist
os.makedirs('/home/ubuntu/bailbonds/state_data', exist_ok=True)

# List of all 50 states with their data
states = [
    {
        "name": "Alabama",
        "abbreviation": "AL",
        "nickname": "Yellowhammer State",
        "capital": "Montgomery",
        "population": "5.1 million",
        "num_counties": "67",
        "largest_counties": [
            "Jefferson County",
            "Mobile County",
            "Madison County"
        ],
        "major_cities": [
            "Birmingham",
            "Montgomery",
            "Mobile"
        ]
    },
    {
        "name": "Alaska",
        "abbreviation": "AK",
        "nickname": "Last Frontier",
        "capital": "Juneau",
        "population": "731,000",
        "num_counties": "30",
        "largest_counties": [
            "Anchorage Borough",
            "Fairbanks North Star Borough",
            "Matanuska-Susitna Borough"
        ],
        "major_cities": [
            "Anchorage",
            "Fairbanks",
            "Juneau"
        ]
    },
    {
        "name": "Arizona",
        "abbreviation": "AZ",
        "nickname": "Grand Canyon State",
        "capital": "Phoenix",
        "population": "7.4 million",
        "num_counties": "15",
        "largest_counties": [
            "Maricopa County",
            "Pima County",
            "Pinal County"
        ],
        "major_cities": [
            "Phoenix",
            "Tucson",
            "Mesa"
        ]
    },
    {
        "name": "Arkansas",
        "abbreviation": "AR",
        "nickname": "Natural State",
        "capital": "Little Rock",
        "population": "3 million",
        "num_counties": "75",
        "largest_counties": [
            "Pulaski County",
            "Benton County",
            "Washington County"
        ],
        "major_cities": [
            "Little Rock",
            "Fayetteville",
            "Fort Smith"
        ]
    },
    {
        "name": "California",
        "abbreviation": "CA",
        "nickname": "Golden State",
        "capital": "Sacramento",
        "population": "39.5 million",
        "num_counties": "58",
        "largest_counties": [
            "Los Angeles County",
            "San Diego County",
            "Orange County"
        ],
        "major_cities": [
            "Los Angeles",
            "San Diego",
            "San Francisco"
        ]
    },
    {
        "name": "Colorado",
        "abbreviation": "CO",
        "nickname": "Centennial State",
        "capital": "Denver",
        "population": "5.8 million",
        "num_counties": "64",
        "largest_counties": [
            "Denver County",
            "El Paso County",
            "Arapahoe County"
        ],
        "major_cities": [
            "Denver",
            "Colorado Springs",
            "Aurora"
        ]
    },
    {
        "name": "Connecticut",
        "abbreviation": "CT",
        "nickname": "Constitution State",
        "capital": "Hartford",
        "population": "3.6 million",
        "num_counties": "8",
        "largest_counties": [
            "Fairfield County",
            "Hartford County",
            "New Haven County"
        ],
        "major_cities": [
            "Bridgeport",
            "New Haven",
            "Hartford"
        ]
    },
    {
        "name": "Delaware",
        "abbreviation": "DE",
        "nickname": "First State",
        "capital": "Dover",
        "population": "990,000",
        "num_counties": "3",
        "largest_counties": [
            "New Castle County",
            "Sussex County",
            "Kent County"
        ],
        "major_cities": [
            "Wilmington",
            "Dover",
            "Newark"
        ]
    },
    {
        "name": "Florida",
        "abbreviation": "FL",
        "nickname": "Sunshine State",
        "capital": "Tallahassee",
        "population": "21.7 million",
        "num_counties": "67",
        "largest_counties": [
            "Miami-Dade County",
            "Broward County",
            "Palm Beach County"
        ],
        "major_cities": [
            "Miami",
            "Orlando",
            "Tampa"
        ]
    },
    {
        "name": "Georgia",
        "abbreviation": "GA",
        "nickname": "Peach State",
        "capital": "Atlanta",
        "population": "10.7 million",
        "num_counties": "159",
        "largest_counties": [
            "Fulton County",
            "Gwinnett County",
            "Cobb County"
        ],
        "major_cities": [
            "Atlanta",
            "Augusta",
            "Columbus"
        ]
    },
    {
        "name": "Hawaii",
        "abbreviation": "HI",
        "nickname": "Aloha State",
        "capital": "Honolulu",
        "population": "1.4 million",
        "num_counties": "5",
        "largest_counties": [
            "Honolulu County",
            "Hawaii County",
            "Maui County"
        ],
        "major_cities": [
            "Honolulu",
            "Hilo",
            "Kailua"
        ]
    },
    {
        "name": "Idaho",
        "abbreviation": "ID",
        "nickname": "Gem State",
        "capital": "Boise",
        "population": "1.8 million",
        "num_counties": "44",
        "largest_counties": [
            "Ada County",
            "Canyon County",
            "Kootenai County"
        ],
        "major_cities": [
            "Boise",
            "Meridian",
            "Nampa"
        ]
    },
    {
        "name": "Illinois",
        "abbreviation": "IL",
        "nickname": "Prairie State",
        "capital": "Springfield",
        "population": "12.7 million",
        "num_counties": "102",
        "largest_counties": [
            "Cook County",
            "DuPage County",
            "Lake County"
        ],
        "major_cities": [
            "Chicago",
            "Aurora",
            "Naperville"
        ]
    },
    {
        "name": "Indiana",
        "abbreviation": "IN",
        "nickname": "Hoosier State",
        "capital": "Indianapolis",
        "population": "6.7 million",
        "num_counties": "92",
        "largest_counties": [
            "Marion County",
            "Lake County",
            "Allen County"
        ],
        "major_cities": [
            "Indianapolis",
            "Fort Wayne",
            "Evansville"
        ]
    },
    {
        "name": "Iowa",
        "abbreviation": "IA",
        "nickname": "Hawkeye State",
        "capital": "Des Moines",
        "population": "3.2 million",
        "num_counties": "99",
        "largest_counties": [
            "Polk County",
            "Linn County",
            "Scott County"
        ],
        "major_cities": [
            "Des Moines",
            "Cedar Rapids",
            "Davenport"
        ]
    },
    {
        "name": "Kansas",
        "abbreviation": "KS",
        "nickname": "Sunflower State",
        "capital": "Topeka",
        "population": "2.9 million",
        "num_counties": "105",
        "largest_counties": [
            "Johnson County",
            "Sedgwick County",
            "Shawnee County"
        ],
        "major_cities": [
            "Wichita",
            "Overland Park",
            "Kansas City"
        ]
    },
    {
        "name": "Kentucky",
        "abbreviation": "KY",
        "nickname": "Bluegrass State",
        "capital": "Frankfort",
        "population": "4.5 million",
        "num_counties": "120",
        "largest_counties": [
            "Jefferson County",
            "Fayette County",
            "Kenton County"
        ],
        "major_cities": [
            "Louisville",
            "Lexington",
            "Bowling Green"
        ]
    },
    {
        "name": "Louisiana",
        "abbreviation": "LA",
        "nickname": "Pelican State",
        "capital": "Baton Rouge",
        "population": "4.6 million",
        "num_counties": "64",
        "largest_counties": [
            "East Baton Rouge Parish",
            "Jefferson Parish",
            "Orleans Parish"
        ],
        "major_cities": [
            "New Orleans",
            "Baton Rouge",
            "Shreveport"
        ]
    },
    {
        "name": "Maine",
        "abbreviation": "ME",
        "nickname": "Pine Tree State",
        "capital": "Augusta",
        "population": "1.3 million",
        "num_counties": "16",
        "largest_counties": [
            "Cumberland County",
            "York County",
            "Penobscot County"
        ],
        "major_cities": [
            "Portland",
            "Lewiston",
            "Bangor"
        ]
    },
    {
        "name": "Maryland",
        "abbreviation": "MD",
        "nickname": "Old Line State",
        "capital": "Annapolis",
        "population": "6.1 million",
        "num_counties": "24",
        "largest_counties": [
            "Montgomery County",
            "Prince George's County",
            "Baltimore County"
        ],
        "major_cities": [
            "Baltimore",
            "Columbia",
            "Germantown"
        ]
    },
    {
        "name": "Massachusetts",
        "abbreviation": "MA",
        "nickname": "Bay State",
        "capital": "Boston",
        "population": "6.9 million",
        "num_counties": "14",
        "largest_counties": [
            "Middlesex County",
            "Worcester County",
            "Suffolk County"
        ],
        "major_cities": [
            "Boston",
            "Worcester",
            "Springfield"
        ]
    },
    {
        "name": "Michigan",
        "abbreviation": "MI",
        "nickname": "Great Lakes State",
        "capital": "Lansing",
        "population": "10 million",
        "num_counties": "83",
        "largest_counties": [
            "Wayne County",
            "Oakland County",
            "Macomb County"
        ],
        "major_cities": [
            "Detroit",
            "Grand Rapids",
            "Warren"
        ]
    },
    {
        "name": "Minnesota",
        "abbreviation": "MN",
        "nickname": "North Star State",
        "capital": "Saint Paul",
        "population": "5.7 million",
        "num_counties": "87",
        "largest_counties": [
            "Hennepin County",
            "Ramsey County",
            "Dakota County"
        ],
        "major_cities": [
            "Minneapolis",
            "Saint Paul",
            "Rochester"
        ]
    },
    {
        "name": "Mississippi",
        "abbreviation": "MS",
        "nickname": "Magnolia State",
        "capital": "Jackson",
        "population": "3 million",
        "num_counties": "82",
        "largest_counties": [
            "Hinds County",
            "Harrison County",
            "DeSoto County"
        ],
        "major_cities": [
            "Jackson",
            "Gulfport",
            "Southaven"
        ]
    },
    {
        "name": "Missouri",
        "abbreviation": "MO",
        "nickname": "Show Me State",
        "capital": "Jefferson City",
        "population": "6.1 million",
        "num_counties": "114",
        "largest_counties": [
            "St. Louis County",
            "Jackson County",
            "St. Charles County"
        ],
        "major_cities": [
            "Kansas City",
            "St. Louis",
            "Springfield"
        ]
    },
    {
        "name": "Montana",
        "abbreviation": "MT",
        "nickname": "Treasure State",
        "capital": "Helena",
        "population": "1.1 million",
        "num_counties": "56",
        "largest_counties": [
            "Yellowstone County",
            "Missoula County",
            "Gallatin County"
        ],
        "major_cities": [
            "Billings",
            "Missoula",
            "Great Falls"
        ]
    },
    {
        "name": "Nebraska",
        "abbreviation": "NE",
        "nickname": "Cornhusker State",
        "capital": "Lincoln",
        "population": "1.9 million",
        "num_counties": "93",
        "largest_counties": [
            "Douglas County",
            "Lancaster County",
            "Sarpy County"
        ],
        "major_cities": [
            "Omaha",
            "Lincoln",
            "Bellevue"
        ]
    },
    {
        "name": "Nevada",
        "abbreviation": "NV",
        "nickname": "Silver State",
        "capital": "Carson City",
        "population": "3.1 million",
        "num_counties": "17",
        "largest_counties": [
            "Clark County",
            "Washoe County",
            "Lyon County"
        ],
        "major_cities": [
            "Las Vegas",
            "Henderson",
            "Reno"
        ]
    },
    {
        "name": "New Hampshire",
        "abbreviation": "NH",
        "nickname": "Granite State",
        "capital": "Concord",
        "population": "1.4 million",
        "num_counties": "10",
        "largest_counties": [
            "Hillsborough County",
            "Rockingham County",
            "Merrimack County"
        ],
        "major_cities": [
            "Manchester",
            "Nashua",
            "Concord"
        ]
    },
    {
        "name": "New Jersey",
        "abbreviation": "NJ",
        "nickname": "Garden State",
        "capital": "Trenton",
        "population": "9 million",
        "num_counties": "21",
        "largest_counties": [
            "Bergen County",
            "Middlesex County",
            "Essex County"
        ],
        "major_cities": [
            "Newark",
            "Jersey City",
            "Paterson"
        ]
    },
    {
        "name": "New Mexico",
        "abbreviation": "NM",
        "nickname": "Land of Enchantment",
        "capital": "Santa Fe",
        "population": "2.1 million",
        "num_counties": "33",
        "largest_counties": [
            "Bernalillo County",
            "Doña Ana County",
            "Santa Fe County"
        ],
        "major_cities": [
            "Albuquerque",
            "Las Cruces",
            "Rio Rancho"
        ]
    },
    {
        "name": "New York",
        "abbreviation": "NY",
        "nickname": "Empire State",
        "capital": "Albany",
        "population": "19.5 million",
        "num_counties": "62",
        "largest_counties": [
            "Kings County",
            "Queens County",
            "New York County"
        ],
        "major_cities": [
            "New York City",
            "Buffalo",
            "Rochester"
        ]
    },
    {
        "name": "North Carolina",
        "abbreviation": "NC",
        "nickname": "Tar Heel State",
        "capital": "Raleigh",
        "population": "10.5 million",
        "num_counties": "100",
        "largest_counties": [
            "Mecklenburg County",
            "Wake County",
            "Guilford County"
        ],
        "major_cities": [
            "Charlotte",
            "Raleigh",
            "Greensboro"
        ]
    },
    {
        "name": "North Dakota",
        "abbreviation": "ND",
        "nickname": "Peace Garden State",
        "capital": "Bismarck",
        "population": "760,000",
        "num_counties": "53",
        "largest_counties": [
            "Cass County",
            "Burleigh County",
            "Grand Forks County"
        ],
        "major_cities": [
            "Fargo",
            "Bismarck",
            "Grand Forks"
        ]
    },
    {
        "name": "Ohio",
        "abbreviation": "OH",
        "nickname": "Buckeye State",
        "capital": "Columbus",
        "population": "11.7 million",
        "num_counties": "88",
        "largest_counties": [
            "Franklin County",
            "Cuyahoga County",
            "Hamilton County"
        ],
        "major_cities": [
            "Columbus",
            "Cleveland",
            "Cincinnati"
        ]
    },
    {
        "name": "Oklahoma",
        "abbreviation": "OK",
        "nickname": "Sooner State",
        "capital": "Oklah
(Content truncated due to size limit. Use line ranges to read in chunks)