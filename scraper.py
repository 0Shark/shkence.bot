'''
    Scraper.py

    Scraper is a python script that scrapes data from a website.
    It can be used to get posts from a website, download thumbnails,
    and save the data to a json file.

    Usage:
        python scraper.py <url> <posts_num>

    Parameters:
        url: The url of the website you want to scrape.
        posts_num: The number of posts you want to scrape.

    Example:
        python scraper.py https://www.example.com/ 10

    Output:
        Scraper will download the posts from the website and save them to a json file.
        It will also download the thumbnails of the posts.
'''

import json
import os
import ssl
import sys
import time
import urllib

import requests
import urllib3

from console import progress_bar

urllib3.disable_warnings()
ssl._create_default_https_context = ssl._create_unverified_context

ssl_verify = False

asset_dir = "assets/thumbnails/"

def get_post_data(url, posts_num):

    # clear assets/thumbnails folder
    if os.path.exists('assets/thumbnails'):
        for f in os.listdir('assets/thumbnails'):
            os.remove(os.path.join('assets/thumbnails', f))
    else:
        os.makedirs('assets/thumbnails')

    if url[:8] != "https://":
        url = "https://" + url

    endpoint = url + '/wp-json/wp/v2/posts?per_page=' + str(posts_num)

    try:
        response = requests.get(endpoint, verify=ssl_verify)
        if response.status_code == 200:
            data = response.json()
        else:
            print("[ERROR] Scraper can't access domain! \n" +
                  str(response.status_code))
            return None
    except Exception as e:
        print("[ERROR] Scraper can't access domain! \n" + str(e))
        return None

    print("[INFO] Scraping posts...")
    posts = []
    for post in progress_bar(data, prefix='Progress:', suffix='Complete', length=50):
        # checking if post posted within 24 hours ago
        time_now = time.time()
        time_post = time.mktime(time.strptime(
            post['date'], "%Y-%m-%dT%H:%M:%S"))
        if time_now - time_post < 86400:
            # get first paragraph of the post
            post_paragraph = post['content']['rendered']
            post_paragraph = post_paragraph.split('<p>')
            post_paragraph = post_paragraph[1].split('</p>')
            post_paragraph = post_paragraph[0]

            # get the category
            category = post['categories'][0]
            if category == "Breaking News":
                category = post['categories'][1]
            endpoint = url + '/wp-json/wp/v2/categories/' + str(category)
            response = requests.get(endpoint, verify=ssl_verify)
            post_category = response.json()['name']

            # get tags
            post_tags = []
            for tag in post['tags']:
                endpoint = url + '/wp-json/wp/v2/tags/{}'.format(tag)
                response = requests.get(endpoint, verify=ssl_verify)
                post_tags.append(response.json()['name'].replace(' ', ''))

            posts.append({
                'id': post['id'],
                'title': post['title']['rendered'],
                'image': requests.get(post['_links']['wp:featuredmedia'][0]['href'], verify=ssl_verify).json()['source_url'],
                'content': post_paragraph,
                'category': post_category,
                'tags': post_tags,
                'link': post['link']
            })

    posts_json = {
        'date': time.strftime("%Y-%m-%d %H:%M:%S"),
        'posts': posts
    }

    # Save to file inside /assets/json
    with open('assets/json/posts.json', 'w') as outfile:
        json.dump(posts_json, outfile)

    return posts_json


def download_thumbnails(posts):
    if not os.path.exists(asset_dir):
        os.makedirs(asset_dir)

    print("[INFO] Downloading thumbnails...")
    # Delete old thumbnails
    for filename in os.listdir(asset_dir):
        os.remove(asset_dir + filename)

    # if posts is empty, return
    if not posts:
        return False

    # Download new thumbnails
    for post in progress_bar(posts, prefix='Progress:', suffix='Complete', length=50):
        try:
            urllib.request.urlretrieve(
                post['image'], asset_dir + str(post['id']) + '.jpg')
        except Exception:
            continue
    
    return True


def scraper(url, post_num):
    posts_num = int(post_num)
    posts_json = get_post_data(url, posts_num)
    status = download_thumbnails(posts_json['posts'])
    if status:
        print("[INFO] Scraper finished!")
    else:
        print("[ERROR] Scraper failed!")


if __name__ == "__main__":
    url = sys.argv[1]
    if sys.argv[1] == '-h' or sys.argv[1] == '--help':
        exit()

    posts_num = int(sys.argv[2])
    posts_json = get_post_data(url, posts_num)
    download_thumbnails(posts_json['posts'])
    print("[INFO] Scraping complete!")
