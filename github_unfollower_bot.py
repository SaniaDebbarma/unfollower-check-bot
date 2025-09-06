# -*- coding: utf-8 -*-
"""
GitHub Unfollower Bot

This script identifies users you follow on GitHub who do not follow you back
and provides an option to unfollow them.

To use this script, you will need a GitHub Personal Access Token (PAT) with
the 'user:follow' scope.
"""
import requests
import getpass

# Base URL for the GitHub API
API_URL = "https://api.github.com"

def get_paginated_data(url, headers):
    """
    Fetches all items from a paginated GitHub API endpoint.

    Args:
        url (str): The starting URL of the API endpoint.
        headers (dict): The headers to include in the request.

    Returns:
        list: A list of all items retrieved from all pages.
        Returns None if there was an error.
    """
    data = []
    while url:
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  

            data.extend(response.json())

           
            if 'next' in response.links:
                url = response.links['next']['url']
            else:
                url = None
        except requests.exceptions.RequestException as e:
            print(f"\nAn error occurred: {e}")
            if response.status_code == 401:
                print("Error: 401 Unauthorized. Please check your Personal Access Token.")
            elif response.status_code == 403:
                print("Error: 403 Forbidden. Your token may not have the 'user:follow' scope, or you may have hit a rate limit.")
            return None
    return data

def unfollow_user(username, headers):
    """
    Unfollows a specified user on GitHub.

    Args:
        username (str): The username of the user to unfollow.
        headers (dict): The headers for the API request, including authentication.

    Returns:
        bool: True if the user was unfollowed successfully, False otherwise.
    """
    url = f"{API_URL}/user/following/{username}"
    try:
        response = requests.delete(url, headers=headers)
        response.raise_for_status()
       
        return response.status_code == 204
    except requests.exceptions.RequestException as e:
        print(f"\nFailed to unfollow {username}: {e}")
        return False

def main():
    """
    Main function to run the GitHub unfollower bot.
    """
    print("--- GitHub Unfollower Bot ---")
    print("This script will help you find and unfollow users who don't follow you back.")
    
    
    username = input("Enter your GitHub username: ")
    print("\nPlease provide a GitHub Personal Access Token (PAT).")
    print("It needs the 'user:follow' scope to unfollow users.")
    print("Your token will not be displayed as you type.")
    token = getpass.getpass("Enter your GitHub PAT: ")

    if not username or not token:
        print("\nUsername and token cannot be empty. Exiting.")
        return

    
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    # --- Step 1: Get the list of users you are following ---
    print(f"\nFetching list of users {username} is following...")
    following_url = f"{API_URL}/users/{username}/following"
    following_list = get_paginated_data(following_url, headers)

    if following_list is None:
        print("Could not retrieve the 'following' list. Exiting.")
        return
        
   
    following_set = {user['login'] for user in following_list}
    print(f"Found {len(following_set)} users you follow.")

  
    print(f"\nFetching list of {username}'s followers...")
    followers_url = f"{API_URL}/users/{username}/followers"
    followers_list = get_paginated_data(followers_url, headers)

    if followers_list is None:
        print("Could not retrieve the 'followers' list. Exiting.")
        return
        
    followers_set = {user['login'] for user in followers_list}
    print(f"Found {len(followers_set)} followers.")

    
    not_following_back = following_set - followers_set
    
    print("-" * 30)
    if not not_following_back:
        print("\nGreat news! Everyone you follow also follows you back.")
        return

    print(f"\nFound {len(not_following_back)} users who do not follow you back:")
    for user in sorted(list(not_following_back)):
        print(f"- {user}")
        
    print("-" * 30)
    
   
    confirm = input("\nDo you want to unfollow these users? (yes/no): ").lower()
    
    if confirm in ['yes', 'y']:
        print("\nStarting the unfollow process...")
        unfollowed_count = 0
        for user_to_unfollow in sorted(list(not_following_back)):
            action = input(f"Unfollow {user_to_unfollow}? (y/n/all/quit): ").lower()
            
            if action == 'quit':
                break
                
            if action == 'y' or action == 'all':
                print(f"Unfollowing {user_to_unfollow}...")
                if unfollow_user(user_to_unfollow, headers):
                    print(f"Successfully unfollowed {user_to_unfollow}.")
                    unfollowed_count += 1
                else:
                    print(f"Could not unfollow {user_to_unfollow}.")
            else:
                print(f"Skipping {user_to_unfollow}.")
        
        print(f"\nProcess complete. Unfollowed {unfollowed_count} user(s).")
    else:
        print("\nNo action taken. Exiting.")

if __name__ == "__main__":
    main()
