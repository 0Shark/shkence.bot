import json
import os

config_path = 'assets/json/config.json'

DOMAIN = 'https://shkence.info'
INSTAGRAM_USERNAME = ''
INSTAGRAM_PASSWORD = ''

def promt_login():
    global INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD
    print('Login to Instagram')
    INSTAGRAM_USERNAME = input('Username: ')
    INSTAGRAM_PASSWORD = input('Password: ')

    with open(config_path, 'w') as f:
        json.dump({'username': INSTAGRAM_USERNAME, 'password': INSTAGRAM_PASSWORD}, f)
    

if (os.path.exists(config_path)):
    with open(config_path) as f:
        config = json.load(f)
        INSTAGRAM_USERNAME = config['username']
        INSTAGRAM_PASSWORD = config['password']
else:
    promt_login()