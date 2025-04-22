import json
import os

def create_county_seats_json(state, state_abbr, county_seats_data):
    """
    Create a JSON file for a state's county seats
    
    Args:
        state (str): Full state name
        state_abbr (str): Two-letter state abbreviation
        county_seats_data (dict): Dictionary mapping county names to their seats
    """
    output = {
        "metadata": {
            "state": state,
            "stateAbbr": state_abbr,
            "lastUpdated": "2024-03-24",
            "totalCounties": len(county_seats_data)
        },
        "counties": {}
    }
    
    for county, seat in county_seats_data.items():
        # Format directory name consistently
        directory = county.replace(" ", "-")
        
        output["counties"][county] = {
            "countySeat": seat,
            "directory": directory
        }
    
    # Ensure state directory exists
    os.makedirs(f"USA_DATA/{state_abbr}", exist_ok=True)
    
    # Write the JSON file
    output_file = f"USA_DATA/{state_abbr}/{state_abbr.lower()}-county-seats.json"
    with open(output_file, "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"Created {output_file} with {len(county_seats_data)} counties")

# Example usage for Missouri
mo_county_seats = {
    "Adair County": "Kirksville",
    "Andrew County": "Savannah",
    "Atchison County": "Rock Port",
    "Audrain County": "Mexico",
    "Barry County": "Cassville",
    "Barton County": "Lamar",
    "Bates County": "Butler",
    "Benton County": "Warsaw",
    "Bollinger County": "Marble Hill",
    "Boone County": "Columbia",
    "Buchanan County": "St. Joseph",
    "Butler County": "Poplar Bluff",
    "Caldwell County": "Kingston",
    "Callaway County": "Fulton",
    "Camden County": "Camdenton",
    "Cape Girardeau County": "Jackson",
    "Carroll County": "Carrollton",
    "Carter County": "Van Buren",
    "Cass County": "Harrisonville",
    "Cedar County": "Stockton",
    "Chariton County": "Keytesville",
    "Christian County": "Ozark",
    "Clark County": "Kahoka",
    "Clay County": "Liberty",
    "Clinton County": "Plattsburg",
    "Cole County": "Jefferson City",
    "Cooper County": "Boonville",
    "Crawford County": "Steelville",
    "Dade County": "Greenfield",
    "Dallas County": "Buffalo",
    "Daviess County": "Gallatin",
    "DeKalb County": "Maysville",
    "Dent County": "Salem",
    "Douglas County": "Ava",
    "Dunklin County": "Kennett",
    "Franklin County": "Union",
    "Gasconade County": "Hermann",
    "Gentry County": "Albany",
    "Greene County": "Springfield",
    "Grundy County": "Trenton",
    "Harrison County": "Bethany",
    "Henry County": "Clinton",
    "Hickory County": "Hermitage",
    "Holt County": "Oregon",
    "Howard County": "Fayette",
    "Howell County": "West Plains",
    "Iron County": "Ironton",
    "Jackson County": "Independence",
    "Jasper County": "Carthage",
    "Jefferson County": "Hillsboro",
    "Johnson County": "Warrensburg",
    "Knox County": "Edina",
    "Laclede County": "Lebanon",
    "Lafayette County": "Lexington",
    "Lawrence County": "Mount Vernon",
    "Lewis County": "Monticello",
    "Lincoln County": "Troy",
    "Linn County": "Linneus",
    "Livingston County": "Chillicothe",
    "McDonald County": "Pineville",
    "Macon County": "Macon",
    "Madison County": "Fredericktown",
    "Maries County": "Vienna",
    "Marion County": "Palmyra",
    "Mercer County": "Princeton",
    "Miller County": "Tuscumbia",
    "Mississippi County": "Charleston",
    "Moniteau County": "California",
    "Monroe County": "Paris",
    "Montgomery County": "Montgomery City",
    "Morgan County": "Versailles",
    "New Madrid County": "New Madrid",
    "Newton County": "Neosho",
    "Nodaway County": "Maryville",
    "Oregon County": "Alton",
    "Osage County": "Linn",
    "Ozark County": "Gainesville",
    "Pemiscot County": "Caruthersville",
    "Perry County": "Perryville",
    "Pettis County": "Sedalia",
    "Phelps County": "Rolla",
    "Pike County": "Bowling Green",
    "Platte County": "Platte City",
    "Polk County": "Bolivar",
    "Pulaski County": "Waynesville",
    "Putnam County": "Unionville",
    "Ralls County": "New London",
    "Randolph County": "Huntsville",
    "Ray County": "Richmond",
    "Reynolds County": "Centerville",
    "Ripley County": "Doniphan",
    "St. Charles County": "St. Charles",
    "St. Clair County": "Osceola",
    "St. Francois County": "Farmington",
    "St. Louis County": "Clayton",
    "Ste. Genevieve County": "Ste. Genevieve",
    "Saline County": "Marshall",
    "Schuyler County": "Lancaster",
    "Scotland County": "Memphis",
    "Scott County": "Benton",
    "Shannon County": "Eminence",
    "Shelby County": "Shelbyville",
    "Stoddard County": "Bloomfield",
    "Stone County": "Galena",
    "Sullivan County": "Milan",
    "Taney County": "Forsyth",
    "Texas County": "Houston",
    "Vernon County": "Nevada",
    "Warren County": "Warrenton",
    "Washington County": "Potosi",
    "Wayne County": "Greenville",
    "Webster County": "Marshfield",
    "Worth County": "Grant City",
    "Wright County": "Hartville"
}

# Create Missouri county seats JSON
create_county_seats_json("Missouri", "MO", mo_county_seats)

# Example usage for Nevada
nv_county_seats = {
    "Carson City": "Carson City",
    "Churchill County": "Fallon",
    "Clark County": "Las Vegas",
    "Douglas County": "Minden",
    "Elko County": "Elko",
    "Esmeralda County": "Goldfield",
    "Eureka County": "Eureka",
    "Humboldt County": "Winnemucca",
    "Lander County": "Battle Mountain",
    "Lincoln County": "Pioche",
    "Lyon County": "Yerington",
    "Mineral County": "Hawthorne",
    "Nye County": "Tonopah",
    "Pershing County": "Lovelock",
    "Storey County": "Virginia City",
    "Washoe County": "Reno",
    "White Pine County": "Ely"
}

# Create Nevada county seats JSON
create_county_seats_json("Nevada", "NV", nv_county_seats)

# Example usage for Alabama
al_county_seats = {
    "Autauga County": "Prattville",
    "Baldwin County": "Bay Minette",
    "Barbour County": "Clayton",
    "Bibb County": "Centreville",
    "Blount County": "Oneonta",
    "Bullock County": "Union Springs",
    "Butler County": "Greenville",
    "Calhoun County": "Anniston",
    "Chambers County": "LaFayette",
    "Cherokee County": "Centre",
    "Chilton County": "Clanton",
    "Choctaw County": "Butler",
    "Clarke County": "Grove Hill",
    "Clay County": "Ashland",
    "Cleburne County": "Heflin",
    "Coffee County": "Elba",
    "Colbert County": "Tuscumbia",
    "Conecuh County": "Evergreen",
    "Coosa County": "Rockford",
    "Covington County": "Andalusia",
    "Crenshaw County": "Luverne",
    "Cullman County": "Cullman",
    "Dale County": "Ozark",
    "Dallas County": "Selma",
    "DeKalb County": "Fort Payne",
    "Elmore County": "Wetumpka",
    "Escambia County": "Brewton",
    "Etowah County": "Gadsden",
    "Fayette County": "Fayette",
    "Franklin County": "Russellville",
    "Geneva County": "Geneva",
    "Greene County": "Eutaw",
    "Hale County": "Greensboro",
    "Henry County": "Abbeville",
    "Houston County": "Dothan",
    "Jackson County": "Scottsboro",
    "Jefferson County": "Birmingham",
    "Lamar County": "Vernon",
    "Lauderdale County": "Florence",
    "Lawrence County": "Moulton",
    "Lee County": "Opelika",
    "Limestone County": "Athens",
    "Lowndes County": "Hayneville",
    "Macon County": "Tuskegee",
    "Madison County": "Huntsville",
    "Marengo County": "Linden",
    "Marion County": "Hamilton",
    "Marshall County": "Guntersville",
    "Mobile County": "Mobile",
    "Monroe County": "Monroeville",
    "Montgomery County": "Montgomery",
    "Morgan County": "Decatur",
    "Perry County": "Marion",
    "Pickens County": "Carrollton",
    "Pike County": "Troy",
    "Randolph County": "Wedowee",
    "Russell County": "Phenix City",
    "St. Clair County": "Pell City",
    "Shelby County": "Columbiana",
    "Sumter County": "Livingston",
    "Talladega County": "Talladega",
    "Tallapoosa County": "Dadeville",
    "Tuscaloosa County": "Tuscaloosa",
    "Walker County": "Jasper",
    "Washington County": "Chatom",
    "Wilcox County": "Camden",
    "Winston County": "Double Springs"
}

# Create Alabama county seats JSON
create_county_seats_json("Alabama", "AL", al_county_seats)

# Example usage for Arizona
az_county_seats = {
    "Apache County": "St. Johns",
    "Cochise County": "Bisbee",
    "Coconino County": "Flagstaff",
    "Gila County": "Globe",
    "Graham County": "Safford",
    "Greenlee County": "Clifton",
    "La Paz County": "Parker",
    "Maricopa County": "Phoenix",
    "Mohave County": "Kingman",
    "Navajo County": "Holbrook",
    "Pima County": "Tucson",
    "Pinal County": "Florence",
    "Santa Cruz County": "Nogales",
    "Yavapai County": "Prescott",
    "Yuma County": "Yuma"
}

# Create Arizona county seats JSON
create_county_seats_json("Arizona", "AZ", az_county_seats)

# Colorado county seats data
co_county_seats = {
    "Adams County": "Brighton",
    "Alamosa County": "Alamosa",
    "Arapahoe County": "Littleton",
    "Archuleta County": "Pagosa Springs",
    "Baca County": "Springfield",
    "Bent County": "Las Animas",
    "Boulder County": "Boulder",
    "Broomfield County": "Broomfield",
    "Chaffee County": "Salida",
    "Cheyenne County": "Cheyenne Wells",
    "Clear Creek County": "Georgetown",
    "Conejos County": "Conejos",
    "Costilla County": "San Luis",
    "Crowley County": "Ordway",
    "Custer County": "Westcliffe",
    "Delta County": "Delta",
    "Denver County": "Denver",
    "Dolores County": "Dove Creek",
    "Douglas County": "Castle Rock",
    "Eagle County": "Eagle",
    "El Paso County": "Colorado Springs",
    "Elbert County": "Kiowa",
    "Fremont County": "Cañon City",
    "Garfield County": "Glenwood Springs",
    "Gilpin County": "Central City",
    "Grand County": "Hot Sulphur Springs",
    "Gunnison County": "Gunnison",
    "Hinsdale County": "Lake City",
    "Huerfano County": "Walsenburg",
    "Jackson County": "Walden",
    "Jefferson County": "Golden",
    "Kiowa County": "Eads",
    "Kit Carson County": "Burlington",
    "La Plata County": "Durango",
    "Lake County": "Leadville",
    "Larimer County": "Fort Collins",
    "Las Animas County": "Trinidad",
    "Lincoln County": "Hugo",
    "Logan County": "Sterling",
    "Mesa County": "Grand Junction",
    "Mineral County": "Creede",
    "Moffat County": "Craig",
    "Montezuma County": "Cortez",
    "Montrose County": "Montrose",
    "Morgan County": "Fort Morgan",
    "Otero County": "La Junta",
    "Ouray County": "Ouray",
    "Park County": "Fairplay",
    "Phillips County": "Holyoke",
    "Pitkin County": "Aspen",
    "Prowers County": "Lamar",
    "Pueblo County": "Pueblo",
    "Rio Blanco County": "Meeker",
    "Rio Grande County": "Del Norte",
    "Routt County": "Steamboat Springs",
    "Saguache County": "Saguache",
    "San Juan County": "Silverton",
    "San Miguel County": "Telluride",
    "Sedgwick County": "Julesburg",
    "Summit County": "Breckenridge",
    "Teller County": "Cripple Creek",
    "Washington County": "Akron",
    "Weld County": "Greeley",
    "Yuma County": "Wray"
}

# Create Colorado county seats JSON
create_county_seats_json("Colorado", "CO", co_county_seats)

# Connecticut county seats data
ct_county_seats = {
    "Fairfield County": "Bridgeport",
    "Hartford County": "Hartford",
    "Litchfield County": "Litchfield",
    "Middlesex County": "Middletown",
    "New Haven County": "New Haven",
    "New London County": "New London",
    "Tolland County": "Rockville",
    "Windham County": "Willimantic"
}

# Create Connecticut county seats JSON
create_county_seats_json("Connecticut", "CT", ct_county_seats)

# Example usage for Delaware
de_county_seats = {
    "Kent County": "Dover",
    "New Castle County": "Wilmington",
    "Sussex County": "Georgetown"
}

# Create Delaware county seats JSON
create_county_seats_json("Delaware", "DE", de_county_seats)

# Example usage for Florida
fl_county_seats = {
    "Alachua County": "Gainesville",
    "Baker County": "Macclenny",
    "Bay County": "Panama City",
    "Bradford County": "Starke",
    "Brevard County": "Titusville",
    "Broward County": "Fort Lauderdale",
    "Calhoun County": "Blountstown",
    "Charlotte County": "Punta Gorda",
    "Citrus County": "Inverness",
    "Clay County": "Green Cove Springs",
    "Collier County": "East Naples",
    "Columbia County": "Lake City",
    "DeSoto County": "Arcadia",
    "Dixie County": "Cross City",
    "Duval County": "Jacksonville",
    "Escambia County": "Pensacola",
    "Flagler County": "Bunnell",
    "Franklin County": "Apalachicola",
    "Gadsden County": "Quincy",
    "Gilchrist County": "Trenton",
    "Glades County": "Moore Haven",
    "Gulf County": "Port St. Joe",
    "Hamilton County": "Jasper",
    "Hardee County": "Wauchula",
    "Hendry County": "LaBelle",
    "Hernando County": "Brooksville",
    "Highlands County": "Sebring",
    "Hillsborough County": "Tampa",
    "Holmes County": "Bonifay",
    "Indian River County": "Vero Beach",
    "Jackson County": "Marianna",
    "Jefferson County": "Monticello",
    "Lafayette County": "Mayo",
    "Lake County": "Tavares",
    "Lee County": "Fort Myers",
    "Leon County": "Tallahassee",
    "Levy County": "Bronson",
    "Liberty County": "Bristol",
    "Madison County": "Madison",
    "Manatee County": "Bradenton",
    "Marion County": "Ocala",
    "Martin County": "Stuart",
    "Miami-Dade County": "Miami",
    "Monroe County": "Key West",
    "Nassau County": "Fernandina Beach",
    "Okaloosa County": "Crestview",
    "Okeechobee County": "Okeechobee",
    "Orange County": "Orlando",
    "Osceola County": "Kissimmee",
    "Palm Beach County": "West Palm Beach",
    "Pasco County": "Dade City",
    "Pinellas County": "Clearwater",
    "Polk County": "Bartow",
    "Putnam County": "Palatka",
    "St. Johns County": "St. Augustine",
    "St. Lucie County": "Fort Pierce",
    "Santa Rosa County": "Milton",
    "Sarasota County": "Sarasota",
    "Seminole County": "Sanford",
    "Sumter County": "Bushnell",
    "Suwannee County": "Live Oak",
    "Taylor County": "Perry",
    "Union County": "Lake Butler",
    "Volusia County": "DeLand",
    "Wakulla County": "Crawfordville",
    "Walton County": "DeFuniak Springs",
    "Washington County": "Chipley"
}

# Create Florida county seats JSON
create_county_seats_json("Florida", "FL", fl_county_seats) 