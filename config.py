from dataclasses import dataclass, field
from key_words import crossing_keywords
from typing import List

 
@dataclass
class config:
    username: str = 'sapirdooley'           # username
    password: str = 'T313v1510n!'           # password
    num_posts: int = 30                     # number of posts to gather
    max_post_likes: int = 1000              # max likes of post
    max_hashtags: int = 15                  # max hashtags of post
    max_likes: int = 500                    # max likes to perform
    max_already_liked: int = 15             # stops after number of posts already liked
    max_old_posts: int = 15                 # stops after number of old posts
    max_post_age: int = 30                  # number of days qualifying old post
