

def compare(local, server):
    """
    Takes in two lists of article objects and compares them. 
    Returns a list of articles that need to be added, removed, or updated.
    """
    to_add, to_remove, to_update = [], [], []

    # Create sets of article titles
    local_titles = {article['slug'] for article in local}
    server_titles = {article['slug'] for article in server}

    # Determine articles to add or remove using set differences
    to_add_titles = local_titles - server_titles
    to_remove_titles = server_titles - local_titles

    # Create lists of articles to add or remove
    to_add = [article for article in local if article['slug'] in to_add_titles]
    to_remove = [article for article in server if article['slug'] in to_remove_titles]

    # Create dict of server articles for easy access
    server_dict = {article['slug']: article for article in server}

    # Determine articles to update
    for article in local:
        server_article = server_dict.get(article['slug'], None)
        if server_article and article['content'] != server_article['content']:
            to_update.append(article)

    return to_add, to_remove, to_update
