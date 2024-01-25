from utils.crud import get_articles

def list():
    articles = get_articles('blog')

    for article in articles:
        postID = article['postID']
        content = article['content']
        slug = article['slug']

        print( f"PostID: {postID} | slug: {slug}")  # noqa: E501
        print( f"Content: ------------------------------------\n{content}\n")  # noqa: E501


