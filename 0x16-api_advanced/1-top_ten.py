#!/usr/bin/python3
"""
Reddit Top Ten Hot Posts

This script queries the Reddit API to retrieve the titles of the first 10 hot posts for a given subreddit.
If the subreddit is not valid or does not exist, the script prints None.
"""

import requests

def top_ten(subreddit):
    """
    Retrieve and print the titles of the first 10 hot posts for a given subreddit.

    This function queries the Reddit API using the '/hot.json' endpoint to obtain the titles
    of the first 10 hot posts from the specified subreddit.

    Args:
        subreddit (str): The name of the subreddit.

    Returns:
        None
    """
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)'}
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    params = {'limit': 10}
    response = requests.get(url, headers=headers, allow_redirects=False, params=params)

    if response.status_code == 200:
        data = response.json()
        posts = data['data']['children'][:10]

        print(f"Top 10 hot posts in /r/{subreddit}:")
        for post in posts:
            print(post['data']['title'])
    else:
        print(None)
        return
