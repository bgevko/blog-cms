from rich.console import Console
from urllib.parse import quote
from utils.get_api_url import get_api_url
import requests


from dotenv import load_dotenv
load_dotenv()
console = Console()

API_URL = get_api_url()

if not API_URL:
    raise Exception("API_URL is not set")

def get_articles():
    response = requests.get(API_URL + "/blog")
    console.print('Retrieving articles from server...', style="yellow")

    if response.status_code != 200:
        raise Exception("Could not fetch blog posts")

    data = response.json()
    articles = []

    for article in data:
        articles.append({
            'title': article['title'],
            'publishDate': article['publishDate'],
            'editDate': article['editDate'],
            'preview': article['preview'],
            'content': article['content'],
            'tags': article['tags'],
            'relatedArticles': article['relatedArticles']
        })

    if len(articles) == 0:
        console.print("No articles found on server.", style="bold red")
    else:
        console.print(f"Found {len(articles)} articles on server.", style="green")
    return articles

def add_article(article):
    response = requests.post(API_URL + "/blog", json=article)
    if response.status_code != 201:
        console.print(f"Status code: {response.status_code} for add_article({article['title']}),", style="bold red")

def remove_article(title):
    response = requests.delete(API_URL + "/blog/" + quote(title))
    if response.status_code != 204:
        console.print(f"Status code: {response.status_code} for remove_article({title}),", style="bold red")

def update_article(title, article):
    response = requests.put(API_URL + "/blog/" + quote(title), json=article)
    if response.status_code != 200:
        console.print(f"Status code: {response.status_code} for update_article({title}),", style="bold red")

