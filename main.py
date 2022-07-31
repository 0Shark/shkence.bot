import time
import json
import os
import git
import shutil
from config import DOMAIN, promt_login
from console import start_message
from scraper import scraper
from insta_gen import create_post_image, create_story_image, create_carousel_images
from insta_post import login, post_post, post_story, post_carousel


def repo_update():
    repo = git.Repo('./')
    repo.git.reset('--hard')
    repo.remotes.origin.pull()
    print("shkence.bot: Repository updated.")


def full_run():
    num_posts = int(input("Enter number of posts: "))
    scraper(DOMAIN, num_posts)
    with open('assets/json/posts.json') as posts_file:
        posts = json.load(posts_file)
        post = posts['posts']
        print("[INFO] Generating post images...")
        for p in post:
            if p['carousel']:
                create_carousel_images(p['id'])
            else:
                create_post_image(p['id'])
            create_story_image(p['id'])
        login()
        print("[INFO] Posting post images...")
        for p in post:
            if p['carousel']:
                post_carousel(p['id'])
            else:
                post_post(p['id'])
            time.sleep(2)
        print("[INFO] Posting story images...")
        for p in post:
            post_story(p['id'], p['link'])
            time.sleep(2)


def scrape_only():
    num_posts = int(input("Enter number of posts: "))
    scraper(DOMAIN, num_posts)


def clear_workspace():
    # clear insta/stories folder
    if os.path.exists('insta/stories'):
        for f in os.listdir('insta/stories'):
            if f.endswith(".jpg") or f.endswith(".png"):
                os.remove(f'insta/stories/{f}')
    else:
        os.makedirs('insta/stories')

    # clear insta/posts folder
    if os.path.exists('insta/posts'):
        for f in os.listdir('insta/posts'):
            if f.endswith(".jpg") or f.endswith(".png"):
                os.remove(os.path.join('insta/posts', f))
    else:
        os.makedirs('insta/posts')

    # clear insta/carousels folder
    if os.path.exists('insta/carousels/'):
        # delete all folders 
        for f in os.listdir('insta/carousels/'):
            if os.path.isdir(f'insta/carousels/{f}'):
                shutil.rmtree(f'insta/carousels/{f}')
    else:
        os.makedirs('insta/carousels')


def main(choice):
    if choice == 1:
        clear_workspace()
        print("shkence.bot: Running full run...")
        full_run()

    elif choice == 2:
        print("shkence.bot: Running scraper...")
        scrape_only()

    elif choice == 3 or choice == 4 or choice == 5:
        clear_workspace() 
        with open('assets/json/posts.json') as posts_file:
            posts = json.load(posts_file)
            post = posts['posts']
            for p in post:
                if choice == 3:
                    print("shkence.bot: Generating posts and story images...")
                    if p['carousel']:
                        create_carousel_images(p['id'])
                    else:
                        create_post_image(p['id'])
                    create_story_image(p['id'])
                elif choice == 4:
                    print("shkence.bot: Generating only post images...")
                    if p['carousel']:
                        create_carousel_images(p['id'])
                    else:
                        create_post_image(p['id'])
                elif choice == 5:
                    print("shkence.bot: Generating only story images...")
                    create_story_image(p['id'])
                    
    elif choice == 6 or choice == 7 or choice == 8:
        login()
        with open('assets/json/posts.json') as posts_file:
            posts = json.load(posts_file)
            post = posts['posts']
            if choice == 6:
                print("shkence.bot: Posting post and stories...")
                for p in post:
                    if p['carousel']:
                        post_carousel(p['id'])
                    else:
                        post_post(p['id'])
                    time.sleep(2)
                for p in post:
                    post_story(p['id'], p['link'])
                    time.sleep(2)
            elif choice == 7:
                print("shkence.bot: Posting only posts...")
                for p in post:
                    if p['carousel']:
                        post_carousel(p['id'])
                    else:
                        post_post(p['id'])
                    time.sleep(2)
            elif choice == 8:
                print("shkence.bot: Posting only stories...")
                for p in post:
                    post_story(p['id'], p['link'])
                    time.sleep(2)
    
    # elif choice == 9:
    #     print("shkence.bot: Posting all carousels...")
    #     login()
    #     with open('assets/json/posts.json') as posts_file:
    #         posts = json.load(posts_file)
    #         post = posts['posts']
    #         for p in post:
    #             post_paths = []
    #             for file in os.listdir(f'insta/carousels/{p["id"]}'):
    #                 if file.endswith(".jpg") or file.endswith(".png"):
    #                     post_paths.append(f'insta/carousels/{p["id"]}/{file}')
    #             post_carousel(p["id"], post_paths)

    elif choice == 9:
        clear_workspace()

    elif choice == 10:
        repo_update()

    elif choice == 11:
        promt_login()

    elif choice == 12:
        print("shkence.bot: Exiting...")
        exit()
        
    else:
        print("shkence.bot: Invalid choice.")
        

if __name__ == '__main__':
    main(start_message())
    while True:
        print("shkence.bot: What would you like to do next?")
        main(int(input()))
