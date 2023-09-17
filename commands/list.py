from utils.crud import get_articles

def list():
    articles = get_articles()

    for article in articles:
        id = article['_id']
        title = article['title']
        date = article['editDate'].split('T')
        daymonthyear = date[0].split('-')
        time = date[1].split('.')[0]

        print(f"{id} | {title} | {daymonthyear[2]}/{daymonthyear[1]}/{daymonthyear[0]} | {time}")  # noqa: E501


