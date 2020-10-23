# Instagram Bot

### Description
<div style="text-align: right"> 
The purpose of this project is to create a Python script that will read an Instagram feed and collect information based on user-inputted criteria. This script is intended to solve the challenge of collecting customer-related information through Instagram at a large scale. With this script, the user should be able to simply run the program; the program will log in to a specified account and collect information, in this case: location data of users that fit a specific set of criteria. In this proposal we shall lay out the specific functions of the script as well as the criteria that will drive data collection. With this script, the user will have their stresses alleviated in regards to the marketing aspect of their company.
</div>

### Component Description

- [Runner](runner.py): configures webdriver, calls bots functions and applys screens posts based on filter criteria
- [Bot](bot.py): the core code that will interact with pages through webdriver
- [Parser](post_parser.py): code for parsing individual post content. Transforms data into Python primitives using ig_post dataclass.
- [Filter](post_filter.py): Filters parsed data based on keywords, date of post, number of likes, and number of hashtags.
- [Tracker](post_tracker.py): Tracks how many posts bot has liked and saved, and breaks loop if posts are old or already liked.
- [Hashtags](hashtags.py): List of hashtags for bot to sort through if not sorting though feed.
- [Keywords](key_words.py): List of keywords to search captions for.
- [Config](config.py): Contains all variables to limit number of likes performed, age of posts, etc.
- [Utilities](utilites.py): Extra code that does not interact with the webdriver directly

### How to Use
1. Download chrome driver from https://chromedriver.chromium.org/ for your OS. Make sure it matches your Chrome version
2. Put username and password in config file
3. Edit keywords and hashtag files 
4. Run runner.py