import random
import time
from dataclasses import dataclass, asdict
import datetime
from post_tracker import post_tracker
import json

def random_sleep():
    t = time.sleep(random.randint(3, 8))
    return t 

def convert_timestamp(item_date_object):
    if isinstance(item_date_object, (datetime.date, datetime.datetime)):
        return item_date_object.timestamp()

def convert_to_json(post):
    post = asdict(post)
    json_object = json.dumps(post, default = convert_timestamp)  
    entry = {post_tracker.matched_post_counter: json_object}
    return entry

