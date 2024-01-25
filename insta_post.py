help = '''
    insta_post.py - Post a picture to instagram

    InstaPost can be used to post to instagram.
    - It can post a normal post, a story, or carousel.
    - It can post videos and reels.

    Usage:
        python insta_post.py <post_id> <post_type> <post_link> (post_link is optional)
    
    Parameters:
        post_id: The post id to post.
        post_type: The type of post to post.
        post_link: The link of the post. (optional)

    Example:
        python insta_post.py 123456789 story https://www.google.com

    Output:
        1) None if post id is not found.
        2) Link to the post if it was posted successfully.

    Note:
        - The post_type can be "post", "story", "carousel", or "reel".
        - The post_link is the link of the post.
'''
import html
import json
import os
import sys
from config import INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD

from instagrapi import Client
from instagrapi.story import StoryBuilder
from instagrapi.types import StoryHashtag, StoryLink, StoryMedia, StoryMention, StorySticker

default_caption = ''
with open('insta/caption.txt', encoding='utf8') as caption_file:
    default_caption = caption_file.read()

cl = ''


def login(username=INSTAGRAM_USERNAME, password=INSTAGRAM_PASSWORD):
    global cl
    print(f'[INFO] Logging in as {username}')
    cl = Client()
    cl.login(username, password)

    return cl


def get_caption(post_id):
    post_data = []
    with open('assets/json/posts.json') as posts_file:
        posts_json = json.load(posts_file)
        posts = posts_json['posts']
        for p in posts:
            if p['id'] == post_id:
                # convert tags into a string of hashtags
                tags = p['tags']
                tags_str = ''
                for tag in tags:
                    tags_str += f' #{tag}'

                post_data = [p['title'], p['content'], tags_str]
    return html.unescape(f'{post_data[0]}\n\n{post_data[1]}\n\n{default_caption}\n{post_data[2]}')


def post_post(post_id):
    post_id = int(post_id)
    print(f'[INFO] Posting post {post_id}')
    cl.photo_upload(
        f'insta/posts/{post_id}.jpg', caption=get_caption(post_id))
    print(f"[INFO] Posted post {post_id}")


def post_carousel(post_id):
    post_id = int(post_id)
    print(f'[INFO] Posting carousel {post_id}')
    post_paths = []
    if os.path.exists(f'insta/posts/{post_id}.jpg'):
        post_paths.append(f'insta/posts/{post_id}.jpg')

    for file in os.listdir(f'insta/carousels/{post_id}'):
        if file.endswith(".jpg") or file.endswith(".png"):
            post_paths.append(f'insta/carousels/{post_id}/{file}')
    cl.album_upload(post_paths, caption=get_caption(post_id))
    print(f"[INFO] Posted carousel {post_id}")


def post_story(post_id, link_url):
    post_id = int(post_id)
    print(f'[INFO] Posting story {post_id}')
    
    try:
        buildout = StoryBuilder(
            f'insta/stories/{post_id}.jpg',
        ).photo(5)  
    except Exception as e:
        print(e)
        print(f"[ERROR] Error generating story for post {post_id}")
        return

    cl.video_upload_to_story(
        buildout.path, 
        "Kliko këtu",
        links=[StoryLink(webUri=link_url, x=0.77, y=0.24)]
    )

    print(f"[INFO] Posted story {post_id}")


if __name__ == "__main__":
    if len(sys.argv) <= 4:
        if sys.argv[1] == '-h' or sys.argv[1] == '--help':
            print(help)
            exit()

        post_id = sys.argv[1]
        post_type = sys.argv[2]
        login()
        if post_type == "post":
            post_post(post_id)
        elif post_type == "story":
            post_link = sys.argv[3]
            post_story(post_id, post_link)
        elif post_type == "carousel":
            post_carousel(post_id)

    else:
        print("[ERROR] Missing parameters")
        exit()
