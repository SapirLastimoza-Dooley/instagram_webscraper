import random
import time
from dataclasses import dataclass
from dataclasses_json import dataclass_json

def random_sleep():
    t = time.sleep(random.randint(3, 8))
    return t 

def to_json_dict(post):
    post.to_dict()
    

