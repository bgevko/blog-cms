from rich.console import Console
from urllib.parse import quote
from utils.get_api_url import get_api_url
import os
import requests


from dotenv import load_dotenv
load_dotenv()
console = Console()

API_URL = get_api_url()
headers = {
    'Authorization': f"Bearer {os.getenv('SECRET_KEY')}"
}

if not API_URL:
    raise Exception("API_URL is not set")

def get_articles(type):
    if type not in ['blog', 'projects', 'notes']:
        raise Exception("Invalid type, must be one of: blog, projects, notes")

    response = requests.get(API_URL + f"/api/{type}")

    if response.status_code != 200:
        raise Exception("Could not fetch articles, error code: " + str(response.status_code))

    data = response.json()
    articles = []

    for article in data:
        articles.append({
            'postID': article['postID'],
            'content': article['content'],
            'slug': article['slug']
        })

    if len(articles) == 0:
        console.print("No articles found on server.", style="bold red")
    else:
        console.print(f"Found {len(articles)} {type} articles.", style="green")
    return articles

def add_article(article, type):
    response = requests.post(API_URL + f"/api/{type}", json=article, headers=headers)
    if response.status_code == 200:
        console.print(f"Added article. Status code: {response.status_code} for add_article({article['slug']}),", style="bold green")
    else:
        console.print(f"Could not add article. Status code: {response.status_code} for add_article({article['slug']}),", style="bold red")

def remove_article(slug, type):
    response = requests.delete(API_URL + f"/api/{type}/" + quote(slug), headers=headers)
    if response.status_code == 200:
        console.print(f"Removed article. Status code: {response.status_code} for remove_article({slug}),", style="bold green")
    else:
        console.print(f"Could not remove article. Status code: {response.status_code} for remove_article({slug}),", style="bold red")

def update_article(slug, article, type):
    response = requests.put(API_URL + f"/api/{type}/" + quote(slug), json=article, headers=headers)
    if response.status_code == 200:
        console.print(f"Updated article. Status code: {response.status_code} for update_article({slug}),", style="bold green")
    else:
        console.print(f"Could not update article. Status code: {response.status_code} for update_article({slug}),", style="bold red")

