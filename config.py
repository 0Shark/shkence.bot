import json
import os
from instagrapi import Client

config_path = 'assets/json/config.json'

DOMAIN = 'https://shkence.info'
INSTAGRAM_USERNAME = ''
INSTAGRAM_PASSWORD = ''
SESSIONID = ''

def promt_login():
    global INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD
    print('Login to Instagram')
    INSTAGRAM_USERNAME = input('Username: ')
    INSTAGRAM_PASSWORD = input('Password: ')

    cl = Client()
    cl.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
    settings = cl.get_settings()
    print('Login successful')
    SESSIONID = settings['uuids']['client_session_id']
    with open(config_path, 'w') as f:
        json.dump({
            'username': INSTAGRAM_USERNAME,
            'password': INSTAGRAM_PASSWORD, 
            'session_id': SESSIONID
        }, f)
    

if (os.path.exists(config_path)):
    with open(config_path) as f:
        config = json.load(f)
        INSTAGRAM_USERNAME = config['username']
        INSTAGRAM_PASSWORD = config['password']
        SESSIONID = config['session_id']
else:
    promt_login()