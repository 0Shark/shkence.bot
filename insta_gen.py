'''
    insta_gen.py
    
    InstaGen generates a post image (1080x1350) from the post id given.

    Usage:
        insta_gen.py <post_id> <post_type>

    Parameters:
        post_id: The post id to generate the post image from.
        post_type: The post type.
            - story: Generates a story image. (done)
            - post: Generates a post image. (done)
            - video: Generates a video. (in progress)
            - carousel: Generates carousel images. (in progress)


    Example:
        insta_gen.py 123456789 post
        
    Output:
        1) None if post id is not found.
        2) The path to the post image/video/reel/carousel created if post id is found.
'''

import json
import os
import sys
import textwrap
import time
import html

from PIL import Image, ImageDraw, ImageFont

font_path = 'assets/fonts/poppins.ttf'

# Check if post id exists


def check_id(post_id):
    post_id = int(post_id)
    with open('assets/json/posts.json') as posts_file:
        posts = json.load(posts_file)
        post = posts['posts']
        for p in post:
            if p['id'] == post_id:
                return True
    return False


# Get post image and load on memory
def get_post_image(post_id):
    post_id = int(post_id)
    post_image = Image.open(f'assets/thumbnails/{post_id}.jpg')
    return post_image


# Get post image text from json data
def get_post_image_text(post_id):
    post_id = int(post_id)
    with open('assets/json/posts.json') as posts_file:
        posts = json.load(posts_file)
        post = posts['posts']
        for p in post:
            if p['id'] == post_id:
                return [p['title'], p['category']]
    return None


# Resize post image to fit in instagram post
def get_resized_post_image(post_id, width, height):
    post_id = int(post_id)
    size = (width, height)
    ratio = width / height
    image = get_post_image(post_id)
    # crop to ratio, center
    w, h = image.size
    if w > ratio * h:  # width is larger then necessary
        x, y = (w - ratio * h) // 2, 0
    else:  # ratio*height >= width (height is larger)
        x, y = 0, (h - w / ratio) // 2
    image = image.crop((x, y, w - x, h - y))

    if image.size > size:  # don't stretch smaller images
        image.thumbnail(size, resample=Image.LANCZOS)

    image = image.resize(size, resample=0)
    return image


# Generate post image
def create_post_image(post_id):
    start_time = time.time()
    post_id = int(post_id)
    if not os.path.exists('assets/thumbnails'):
        os.makedirs('assets/thumbnails')

    if not os.path.exists(f'assets/thumbnails/{post_id}.jpg'):
        print(f'[INFO] Thumbnail for post id {post_id} not found.')
        return None

    if not check_id(post_id):
        print(f'[INFO] Post id {post_id} not found.')
        return None

    print(f'[INFO] Creating post image for post id {post_id}...')

    post_image = get_resized_post_image(post_id, 1080, 1350)
    post_image_text = get_post_image_text(post_id)
    post_image_title = textwrap.wrap(html.unescape(post_image_text[0]), width=40)
    post_image_category = html.unescape(post_image_text[1])
    post_image_font = ImageFont.truetype(font_path, size=45)
    post_image_category_font = ImageFont.truetype(font_path, size=30)
    post_image_draw = ImageDraw.Draw(post_image)

    # Getting text dimensions
    cat_width, cat_height = post_image_draw.textsize(
        post_image_category, font=post_image_category_font)
    # Positioning text 68% down the image and 30px from the left
    cat_y = int(post_image.size[1] * 0.68)
    # Adding rectangle fill
    post_image_draw.rectangle(
        (30, cat_y, cat_width + 40, cat_y + cat_height + 5), fill=(62, 62, 62))
    # Adding category text
    post_image_draw.text((35, cat_y), post_image_category,
                         fill='white', font=post_image_category_font)

    # Add title text
    for i, line in enumerate(post_image_title):
        # Getting text dimensions
        title_width, title_height = post_image_draw.textsize(
            line, font=post_image_font)
        # Positioning text 70.5% down the image and 30px from the left
        title_y = int(post_image.size[1] * 0.705) + 30 + (i * 80)
        # Adding rectangle fill
        post_image_draw.rectangle(
            (30, title_y, title_width + 40, title_y + title_height + 5), fill=(21, 101, 200))
        # Adding title text
        post_image_draw.text((35, title_y), line,
                             fill='white', font=post_image_font)

        if i == 2:
            break

    # Paste in overlay
    try:
        overlay = Image.open('assets/overlay.png')
        post_image.paste(overlay, (0, 0), overlay)
    except Exception:
        print('[ERROR] Overlay image not found.')
        return None

    post_image.convert('RGB').save(f'insta/posts/{post_id}.jpg')

    elapsed_time = time.time() - start_time

    print(
        f'[INFO] Created post image for post id {post_id} in {elapsed_time*1000:.2f}ms.')

    return f'insta/posts/{post_id}.jpg'


# Generate story image
def create_story_image(post_id):
    start_time = time.time()
    post_id = int(post_id)

    if not os.path.exists(f'assets/thumbnails/{post_id}.jpg'):
        print(f'[INFO] Thumbnail for post id {post_id} not found.')
        return None

    if not check_id(post_id):
        print(f'[INFO] Post id {post_id} not found.')
        return None

    print(f'[INFO] Creating story image for post id {post_id}...')

    post_image = get_resized_post_image(post_id, 720, 1280)
    post_image_text = get_post_image_text(post_id)
    post_image_title = textwrap.wrap(html.unescape(post_image_text[0]), width=30)
    post_image_category = html.unescape(post_image_text[1])
    post_image_font = ImageFont.truetype(font_path, size=35)
    post_image_category_font = ImageFont.truetype(font_path, size=30)
    post_image_draw = ImageDraw.Draw(post_image)

    # Getting text dimensions
    cat_width, cat_height = post_image_draw.textsize(
        post_image_category, font=post_image_category_font)
    # Positioning text 68% down the image and 30px from the left
    cat_y = int(post_image.size[1] * 0.68)
    # Adding rectangle fill
    post_image_draw.rectangle(
        (30, cat_y, cat_width + 40, cat_y + cat_height + 5), fill=(62, 62, 62))
    # Adding category text
    post_image_draw.text((35, cat_y), post_image_category,
                         fill='white', font=post_image_category_font)
    # Add title text
    for i, line in enumerate(post_image_title):
        # Getting text dimensions
        title_width, title_height = post_image_draw.textsize(
            line, font=post_image_font)
        # Positioning text 70.5% down the image and 30px from the left
        title_y = int(post_image.size[1] * 0.705) + 30 + (i * 70)
        # Adding rectangle fill
        post_image_draw.rectangle(
            (30, title_y, title_width + 40, title_y + title_height + 5), fill=(21, 101, 200))
        # Adding title text
        post_image_draw.text((35, title_y), line,
                             fill='white', font=post_image_font)

        if i == 2:
            break

    # Paste in link sticker
    try:
        link_sticker = Image.open('assets/link.png')
        post_image.paste(link_sticker, (0, 0), link_sticker)
    except Exception:
        print('[ERROR] Link sticker not found.')
        return None
        
    post_image.convert('RGB').save(f'insta/stories/{post_id}.jpg')
    elapsed_time = time.time() - start_time
    print(
        f'[INFO] Created story image for post id {post_id} in {elapsed_time*1000:.2f}ms.')

    return f'insta/stories/{post_id}.jpg'


if __name__ == '__main__':
    if len(sys.argv) <= 3:
        post_id = sys.argv[1]

        if sys.argv[1] == '-h' or sys.argv[1] == '--help':
            print('[HELP] Usage: python3 insta_gen.py <post_id> <image_type>')
            print('[HELP] Image types: post, story, video, carousel')
            print('[HELP] Example: python3 insta_gen.py 12345 post')
            exit()

        post_type = sys.argv[2]
        if check_id(post_id):
            post_path = None

            if post_type == 'post':
                post_path = create_post_image(post_id)
            elif post_type == 'story':
                post_path = create_story_image(post_id)

            if post_path is not None:
                print(f'[INFO] Post image saved to {post_path}.')
                print(
                    f'[INFO] Would you like to open the image in your default image viewer? (y/n)')
                if input().lower() == 'y':
                    os.chdir(os.path.dirname(post_path))
                    os.system(f'{os.path.basename(post_path)}')
                    exit()
            else:
                print(f'[ERROR] Post image is already saved.')
                exit()
        else:
            print('[ERROR] Post id is not valid.')
    else:
        print('[ERROR] Invalid arguments.')
