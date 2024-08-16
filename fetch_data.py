from instagram_private_api import Client, ClientCompatPatch
import os
from getpass import getpass


# Authenticate user
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
    followers = api.user_followers(api.authenticated_user_id)
    return followers



# def compare_follows(following, followers):
    