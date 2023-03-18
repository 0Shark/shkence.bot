'''
    autobot.py
    ~~~~~~~~~~
    This file runs the shkence.bot in autonomous mode.
    It will scrape, generate images and post them to Instagram.

    The bot will run based on the settings in the settings.json file.
    The settings file contains the following information:
    - Number of posts to post per day
    - Hours to wait between posts
    
    The bot will run in a loop looking for new posts to post until the limit is reached.
    The bot will run as a background process and will not interfere with the user's computer.

    It will also generate a report at the end of the process.
    The report will be saved in the reports folder.
    The report will contain the following information in JSON format:
    - Number of posts scraped
    - Number of posts posted
    - Number of stories posted  
    - Potential errors
'''

import time
import json
import os
import shutil
from config import DOMAIN
from scraper import scraper
from insta_gen import create_post_image, create_story_image, create_carousel_images
from insta_post import post_post, post_story, post_carousel, login
from main import clear_workspace


def start_autobot():
    login()
    # load settings
    with open('assets/json/settings.json') as settings_file:
        settings = json.load(settings_file)
        num_posts = settings['posts_per_day']
        hours_to_wait = settings['hours_between_posts']

    # clear workspace
    clear_workspace()

    # scrape posts
    scraper(DOMAIN, num_posts)

    # load posts
    with open('assets/json/posts.json') as posts_file:
        posts = json.load(posts_file)
        post = posts['posts']

    # generate images
    print("[INFO] Generating post images...")
    for p in post:
        if p['carousel']:
            create_carousel_images(p['id'])
        else:
            create_post_image(p['id'])
        create_story_image(p['id'])

    # post images
    print("[INFO] Posting post images...")
    for p in post:
        if p['carousel']:
            post_carousel(p['id'])
        else:
            post_post(p['id'])
        time.sleep(2)

    # post stories
    print("[INFO] Posting story images...")
    for p in post:
        post_story(p['id'], p['link'])
        time.sleep(2)

    # generate report
    report = {
        "posts_scraped": len(post),
        "posts_posted": len(post),
        "stories_posted": len(post)
    }
    with open('reports/report.json', 'w') as report_file:
        json.dump(report, report_file, indent=4)

    # wait
    time.sleep(hours_to_wait * 60 * 60)

    # run again
    start_autobot()

if __name__ == "__main__":
    start_autobot()