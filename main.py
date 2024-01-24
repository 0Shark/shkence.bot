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
        failed_posts = []
        for p in post:
            if p['carousel']:
                try:
                    create_carousel_images(p['id'])
                except Exception as e:
                    print(e)
                    print(f"[ERROR] Error generating carousel images for post {p['id']} Skipping...")
                    failed_posts.append(p)
                    continue
            else:
                try:
                    create_post_image(p['id'])
                except Exception as e:
                    print(e)
                    print(f"[ERROR] Error generating post image for post {p['id']} Skipping...")
                    failed_posts.append(p)
                    continue
            try:
                create_story_image(p['id'])
            except Exception as e:
                print(e)
                print(f"[ERROR] Error generating story image for post {p['id']} Skipping...")
                failed_posts.append(p)
                continue

        for p in failed_posts:
            post.remove(p)

        login()
        print("[INFO] Posting post images...")

        failed_posts = []

        for p in post:
            if p['carousel']:
                try:
                    post_carousel(p['id'])
                except Exception as e:
                    print(e)
                    print(f"[ERROR] Error posting carousel for post {p['id']} Skipping...")
                    failed_posts.append(p)
                    continue
            else:
                try:
                    post_post(p['id'])
                except Exception as e:
                    print(e)
                    print(f"[ERROR] Error posting post {p['id']} Skipping...")
                    failed_posts.append(p)
                    continue
            time.sleep(2)

        print("[INFO] Posting story images...")
        for p in post:
            try:
                post_story(p['id'], p['link'])
                time.sleep(2)
            except Exception as e:
                print(e)
                print(f"[ERROR] Error posting story for post {p['id']} Skipping...")
                continue


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


# Not fully implemented yet
def setup_autobot():
    print("shkence.bot: Setting up autobot...")
    posts_per_day = int(
        input("Enter number of posts you would like to post per day: "))
    hours_between_posts = int(
        input("Enter number of hours you would like to wait between posts: "))

    with open('assets/json/settings.json', 'w') as settings_file:
        settings = {
            "posts_per_day": posts_per_day,
            "hours_between_posts": hours_between_posts
        }
        json.dump(settings, settings_file, indent=4)

    print("shkence.bot: Autobot setup complete.")

    # Start autobot.py
    os.system('py autobot.py')



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
                try:
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
                except Exception as e:
                    print(e)
                    print(f"[ERROR] Error generating images for post {p['id']} Skipping...")
                    continue


    elif choice == 6 or choice == 7 or choice == 8:
        login()
        with open('assets/json/posts.json') as posts_file:
            posts = json.load(posts_file)
            post = posts['posts']
            if choice == 6:
                print("shkence.bot: Posting post and stories...")
                failed_posts = []
                for p in post:
                    try:
                        if p['carousel']:
                            post_carousel(p['id'])
                        else:
                            post_post(p['id'])
                        time.sleep(2)
                    except Exception as e:
                        print(e)
                        print(f"[ERROR] Error posting post {p['id']} Skipping...")
                        failed_posts.append(p)
                        continue

                for p in failed_posts:
                    post.remove(p)

                for p in post:
                    try:
                        post_story(p['id'], p['link'])
                        time.sleep(2)
                    except Exception as e:
                        print(e)
                        print(f"[ERROR] Error posting story for post {p['id']} Skipping...")
                        continue
            elif choice == 7:
                print("shkence.bot: Posting only posts...")
                for p in post:
                    try:
                        if p['carousel']:
                            post_carousel(p['id'])
                        else:
                            post_post(p['id'])
                        time.sleep(2)
                    except Exception as e:
                        print(e)
                        print(f"[ERROR] Error posting post {p['id']} Skipping...")
                        continue
            elif choice == 8:
                print("shkence.bot: Posting only stories...")
                for p in post:
                    try:
                        post_story(p['id'], p['link'])
                        time.sleep(2)
                    except Exception as e:
                        print(e)
                        print(f"[ERROR] Error posting story for post {p['id']} Skipping...")
                        continue

    elif choice == 9:
        clear_workspace()

    elif choice == 10:
        repo_update()

    elif choice == 11:
        promt_login()

    elif choice == 12:
        setup_autobot()

    elif choice == 13:
        print("shkence.bot: Exiting...")
        exit()

    else:
        print("shkence.bot: Invalid choice.")


if __name__ == '__main__':
    main(start_message())
    while True:
        print("shkence.bot: What would you like to do next?")
        main(int(input()))
