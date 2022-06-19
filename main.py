import time
import json
import os
from config import DOMAIN
from console import start_message
from scraper import scraper
from insta_gen import create_post_image, create_story_image
from insta_post import login, post_post, post_story, post_carousel


def full_run():
    num_posts = int(input("Enter number of posts: "))
    scraper(DOMAIN, num_posts)
    with open('assets/json/posts.json') as posts_file:
        posts = json.load(posts_file)
        post = posts['posts']
        for p in post:
            create_post_image(p['id'])
            create_story_image(p['id'])
        login()
        print("[INFO] Posting post images...")
        for p in post:
            post_post(p['id'])
            time.sleep(2)
        print("[INFO] Posting story images...")
        for p in post:
            post_story(p['id'], p['link'])
            time.sleep(2)


def main(choice):
    if choice == 1:
        print("shkence.bot: Running full run...")
        full_run()

    elif choice == 2:
        print("shkence.bot: Running scraper...")
        num_posts = int(input("Enter number of posts: "))
        scraper(DOMAIN, num_posts)

    elif choice == 3:
        print("shkence.bot: Generating posts and story images...")
        with open('assets/json/posts.json') as posts_file:
            posts = json.load(posts_file)
            post = posts['posts']
            for p in post:
                create_post_image(p['id'])
                create_story_image(p['id'])

    elif choice == 4:
        print("shkence.bot: Generating only post images...")
        with open('assets/json/posts.json') as posts_file:
            posts = json.load(posts_file)
            post = posts['posts']
            for p in post:
                create_post_image(p['id'])

    elif choice == 5:
        print("shkence.bot: Generating only story images...")
        with open('assets/json/posts.json') as posts_file:
            posts = json.load(posts_file)
            post = posts['posts']
            for p in post:
                create_story_image(p['id'])

    elif choice == 6:
        print("shkence.bot: Posting post and stories...")
        login()
        with open('assets/json/posts.json') as posts_file:
            posts = json.load(posts_file)
            post = posts['posts']
            for p in post:
                post_post(p['id'])
                time.sleep(2)
            for p in post:
                post_story(p['id'], p['link'])
                time.sleep(2)

    elif choice == 7:
        print("shkence.bot: Posting only posts...")
        login()
        with open('assets/json/posts.json') as posts_file:
            posts = json.load(posts_file)
            post = posts['posts']
            for p in post:
                post_post(p['id'])
                time.sleep(2)

    elif choice == 8:
        print("shkence.bot: Posting only stories...")
        login()
        with open('assets/json/posts.json') as posts_file:
            posts = json.load(posts_file)
            post = posts['posts']
            for p in post:
                post_story(p['id'], p['link'])
                time.sleep(2)
    
    elif choice == 9:
        print("shkence.bot: Posting all carousels...")
        login()
        with open('assets/json/posts.json') as posts_file:
            posts = json.load(posts_file)
            post = posts['posts']
            for p in post:
                post_paths = []
                for file in os.listdir(f'insta/carousels/{p["id"]}'):
                    if file.endswith(".jpg") or file.endswith(".png"):
                        post_paths.append(f'insta/carousels/{p["id"]}/{file}')
                post_carousel(p["id"], post_paths)
    elif choice == 10:
        # clear insta/stories folder
        if os.path.exists('insta/stories'):
            for f in os.listdir('insta/stories'):
                os.remove(os.path.join('insta/stories', f))
        else:
            os.makedirs('insta/stories')

        # clear insta/posts folder
        if os.path.exists('insta/posts'):
            for f in os.listdir('insta/posts'):
                os.remove(os.path.join('insta/posts', f))
        else:
            os.makedirs('insta/posts')

    elif choice == 11:
        exit()


if __name__ == '__main__':
    main(start_message())
    while True:
        print("shkence.bot: What would you like to do next?")
        main(int(input()))
