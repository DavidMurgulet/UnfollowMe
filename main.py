from instagram_private_api import Client, ClientCompatPatch
import os
import json
import codecs
from getpass import getpass


# GPT helpers
def to_json(python_object):
    if isinstance(python_object, bytes):
        return {'__class__': 'bytes',
                '__value__': codecs.encode(python_object, 'base64').decode()}
    raise TypeError(repr(python_object) + ' is not JSON serializable')


def from_json(json_object):
    if '__class__' in json_object and json_object['__class__'] == 'bytes':
        return codecs.decode(json_object['__value__'].encode(), 'base64')
    return json_object


def onlogin_callback(api, new_settings_file):
    cache_settings = api.settings
    with open(new_settings_file, 'w') as outfile:
        json.dump(cache_settings, outfile, default=to_json)
        print('SAVED: {0!s}'.format(new_settings_file))



def authenticate_user():
    username = input("Enter your username: ")
    password = getpass("Enter your password: ")

    try:
        api = Client(username, password)
        print("Successfully authenticated")
        return api
    except Exception as e:
        print("Failed to authenticate")
        print(e)
        return None
    
def get_following(api):
    rank_token = api.generate_uuid(False, None)
    following = api.user_following(api.authenticated_user_id, rank_token)
    return following


def get_followers(api):
    followers = []
    next_max_id = None

    while True:
        results = api.user_followers(api.authenticated_user_id, count=50, max_id=next_max_id)
        followers.extend(results.get('users', []))
        
        next_max_id = results.get('next_max_id')
        if not next_max_id:
            break
    
    for follower in followers:
        print(follower['username'])

    return followers


def main():
    client = authenticate_user()
    if client:
        following = get_following(client)
        for follows in following:
            print(follows)

if __name__ == "__main__":
    main()
