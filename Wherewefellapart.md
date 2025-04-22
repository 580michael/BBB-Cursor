OK, you're getting way ahead of yourself. I'm not sure why you decided to start building out every page when you didn't even know if the first page was right, it wasn't I have looked through many of these pages. They are all the same. They look like this Pennsylvania page, which does not in anyway look like the page that I have built for the template. please look at the template closely and then look at the items that you are allowed to use from the template section all of the global items and then I named them easily for you to be able to find and use. 

Please stop going off on tangent and doing things that no one has asked for right now we are trying to build one correct Oklahoma page from the template that has all of the information in the correct order so that it looks like the pictures that I gave you that are properly built not the pictures from Pennsylvania, which is what the output of your python file is giving now do not do multiple states until we can accomplish one state

Here is what you wrote to me when we had everything working fine before all of this craziness started

I've reviewed all the screenshots and understand your Divi Theme Builder setup for state pages. You have different components saved as individual library items, which is excellent for maintainability. Here's my analysis of the page structure and how to implement it for Oklahoma:
Page Structure Analysis
Hero Section: Blue header with BBB logo, search bar, state name, and map
Title Section: "Your Guide to Finding Local Bail Bondsmen in [state_name]"
Content Section: Paragraphs about bail bond services
Features Section: 24/7 Availability, Verified Bondsman, Nationwide Coverage icons with descriptions
Counties Section: Major Counties in [state_name] with 3 county listings
Additional Text: More detailed information about bail bond services
Second Search Bar: Another opportunity for users to search
FAQ Section: 5 placeholder questions/answers
Implementation for Oklahoma State Page
Here's how to build the Oklahoma page using your saved components:
Start with your All States Pages template in Theme Builder as the base
Add these components in this order:
"Blue Search Global" (hero section with map)
"Text Header below Hero States" (the "Your Guide to Finding..." section)
"Content Below Map States" (the descriptive paragraphs)
The 24/7, Verified, Nationwide features section
"Major Counties in [state_name]"
"3 [county_name] row" (for the three Oklahoma counties)
The additional text content section
The second search form
FAQ section (with placeholders)
For the FAQ section, keep your placeholders as they are now:
[FAQ_QUESTION_1] through [FAQ_QUESTION_5]
[FAQ_ANSWER_1] through [FAQ_ANSWER_5]
Testing Process
Create a test page for Oklahoma using your Python script
Verify the placeholders are replaced correctly:
[state_name] → "Oklahoma"
[county_name] → "Oklahoma County", "Tulsa County", "Cleveland County"
Map centered on Oklahoma City
FAQ placeholders replaced with random questions/answers
The key advantage of your current setup is that you have modular components which can be maintained individually in the Divi library. If you need to update any section in the future, you can edit the saved library item, and it will update across all pages using that component.