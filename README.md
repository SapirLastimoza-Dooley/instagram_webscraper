# Instagram Bot

### Component description

- [Runner](runner.py): configures webdriver, calls bots functions and applys screens posts based on filter criteria
- [Bot](bot.py): the core code that will interact with pages through webdriver
- [Parser](post_parser.py): code for parsing individual post content. Transforms data into Python primitives using ig_post dataclass.
- [Filter](post_filter.py): Filters parsed data based on keywords, date of post, number of likes, and number of hashtags.
- [Tracker](post_tracker.py): Tracks how many posts bot has liked and saved, and breaks loop if posts are old or already liked.
- [Hashtags](hashtags.py): List of hashtags for bot to sort through if not sorting though feed.
- [Keywords](key_words.py): List of keywords to search captions for.
- [Config](config.py): Contains all variables to limit number of likes performed, age of posts, etc.
- [Utilities](utilites.py): Extra code that does not interact with the webdriver directly