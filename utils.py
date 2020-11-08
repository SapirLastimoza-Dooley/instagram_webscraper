import random
import time
from dataclasses import dataclass, asdict
import datetime
import json
from config import post_tracker

def random_sleep():
    t = random.randint(5, 8)
    time.sleep(random.randint(3, 8))
    return t 

def convert_timestamp(item_date_object):
    if isinstance(item_date_object, (datetime.date, datetime.datetime)):
        return item_date_object.timestamp()

def convert_to_json(post):
    post = asdict(post)
    json_object = json.dumps(post, default = convert_timestamp)  
    return json_object

