import requests
from collections import Counter

def count_words(subreddit, word_list, after=None, word_counter=None):
    """
    Recursively fetches and counts occurrences of given keywords in hot article titles from a Reddit subreddit.
    
    Args:
        subreddit (str): The name of the subreddit to retrieve hot articles from.
        word_list (list): A list of keywords to count occurrences of in article titles.
        after (str, optional): The 'after' parameter for pagination. Defaults to None.
        word_counter (collections.Counter, optional): A counter to keep track of keyword occurrences. Defaults to None.

    Returns:
        None
    """
    # If word_counter is not provided, initialize it as a Counter dictionary
    if word_counter is None:
        word_counter = Counter()

    # Set User-Agent header to avoid issues with Reddit's rate limiting
    headers = {'User-Agent': 'Your User Agent'}

    # Construct the URL to fetch hot posts from the specified subreddit
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    params = {'limit': 25}
    
    # If 'after' parameter exists, include it in the request
    if after:
        params['after'] = after
    
    # Make a GET request to the Reddit API
    response = requests.get(url, headers=headers, params=params)
    
    # If the response status code is 200 (OK)
    if response.status_code == 200:
        # Parse the JSON response data
        data = response.json()
        
        # Extract the list of posts from the response
        posts = data['data']['children']
        
        # Iterate through each post's title and each word in the word_list
        for post in posts:
            title = post['data']['title'].lower()
            for word in word_list:
                # Check if the word appears in the lowercase title (with spaces)
                if f" {word.lower()} " in f" {title} ":
                    # Increment the counter for the current word
                    word_counter[word.lower()] += 1

        # Get the 'after' parameter for pagination
        after = data['data']['after']
        
        # If there are more pages, recursively call the function with updated 'after' and word_counter
        if after:
            return count_words(subreddit, word_list, after, word_counter)
        else:
            # If no more pages, sort the word_counter and print the results
            sorted_counts = sorted(word_counter.items(), key=lambda x: (-x[1], x[0]))
            for word, count in sorted_counts:
                print(f"{word}: {count}")
