from dataclasses import dataclass, field
from dataclass_csv import DataclassReader, dateformat
from datetime import datetime

@dataclass
class config:
    # basic user info
<<<<<<< HEAD

    insta_username = input('Enter your Instagram username: ')
    insta_password = input('Enter your Instagram password: ')
    arcgis_username = input('Enter your ArcGIS Online username: ')
    arcgis_password = input('Enter your ArcGIS Online password: ')
=======
>>>>>>> 9ae55ef55ed86ad5684b00a720fbd39b653f32c8
    
    user_profile: str = 'https://www.instagram.com/' + insta_username + '/'  # link to user profile

    # parameters for bot functions
    num_posts = int(input('How many posts would you like to scrape?: '))
    like_post = input('Would you like to like all posts? (y/n): ')
    if like_post == 'y':
        like_post = True
        num_likes = int(input('How many likes would you like to perform?: '))  
    else:
        like_post = False
    save_post = input('Would you like to save matched posts? (y/n): ')
    if save_post == 'y':
        save_post = True
    else:
        save_post = False

    # parameters for bot filter
    max_post_likes: int = 1000  # skips posts with more likes
    max_hashtags: int = 15      # skips posts with more hashtags
    max_already_liked: int = 15 # stops when all posts have been liked
    max_old_posts: int = 30     # stops when posts are all old
    max_post_age: int = 30      # number of days qualifying post as old      

# tracks progress of bot
class post_tracker: 
    like_counter: int = 0               # tracks number of posts liked
    save_counter: int = 0               # tracks number of posts saved
    follow_counter: int = 0             # tracks number of follows performed
    unfollow_counter: int = 0           # tracks number of unfollows performed
    already_liked_counter: int = 0      # tracks number of reccuring posts already liked
    old_post_counter: int = 0           # tracks number of reccuring old posts 
    matched_post_counter: int = 0       # tracks number of matched posts found
    posts_with_location: list = []      # posts saved with location tag
    all_posts: list = []                # all posts matching keywords

@dataclass
class xpaths:
    # login xpaths
    username_input: str = '//input[@name=\'username\']'
    password_input: str = '//input[@name=\'password\']'
    login_button: str = '//div[contains(text(), "Log In")]'
    logout_button: str = '//div[contains(text(), "Log Out")]'
    popup_button: str = '//button[contains(text(), "Not Now")]'

    # main page xpaths
    dropdown_menu: str = '/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div[5]/span/img'
    post_link: str = '//a[@class=\'c-Yi7\']'

    # post xpaths
    like_button: str = '//*[@aria-label="Like"][@width="24"]'
    save_button: str = '//*[@aria-label="Save"]'
    author: str = '//a[@class=\'sqdOP yWX7d     _8A5w5   ZIAjV \']'
    caption: str = '//div[@class =\'C4VMK\']'
    likes: str = '/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[2]/div/div[2]/button/span'
    hashtags: str = '//a[@class=\' xil3i\']'
    date: str = '//time[@class=\'_1o9PC Nzb55\']'
    location: str = '//a[@class=\'O4GlU\']'

    # profile xpaths
    follow_button: str = '//button[contains(text(), "Follow")]'
    unfollow_button: str = '//button[contains(text(), "Unfollow")]'
    followers_button: str = f'//a[@href=\'/{config.insta_username}/followers/\']'
    followers_count: str = '/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span'
    following_button: str = f'//a[@href=\'/{config.insta_username}/following/\']'
    following_count: str = '/html/body/div[1]/section/main/div/header/section/ul/li[3]/a/span'
    follow_back_button: str = '//button[contains(text(), "Follow Back")]'
    bio: str = '/html/body/div[1]/section/main/div/header/section/div[2]/span'

    # following/follower dialog xpaths
    follower_window: str = '//div[@role =\'dialog\']//a'
    following_window: str = '//div[@role =\'dialog\']//a'
    friend_follow_button: str = '/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div[2]/div/span/span[1]/button' 
    profile_link: str = '//a[@class =\'FPmhX notranslate  _0imsa \']'

# post filter keywords
#post_keywords = ['crossing', 'crossed', 'installation', 'probate', 'introduce']
post_keywords_str = input('What keywords are we looking for? (seperate with comma): ')
post_keywords = list(post_keywords_str.split(",")) 
print('-------------------------------------------------------------------------------')

# profile location keywords
location_keywords = ['Texas']

# hashtags for scraping
tamu_hashtags = ['tamu24', 'tamu23', 'tamu22', 'tamu21', 'tamu', 'aggieland', 'gigem', 'AggieLand', 'GigEm', 'AggieFootball', 'Aggies', 'AggieRing', 'aggiebound', 'sec', 'gigs']
greek_hashtags =['whygorho', 'whygospo', 'whyichoseldy', 'rushrho', 'rushldy','rushldpsi', 'rushsigmas', 'rushakdphi', 'rushadk', 'rushlambdas', 'lambdaphiepsilon', 'rushsyz', 'sigmapsizeta',
                    'rushkpl', 'kappaphilambda', 'pialphaphi' , 'rushsopi', 'sigmaomicronpi', 'chideltatheta', 'rushchidelts', 'alphaxi', 'bidday', 'gogreek', 'bidweek' ] 
