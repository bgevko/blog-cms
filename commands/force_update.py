from rich.console import Console
from utils.parse_md import parse_articles 
from utils.crud import get_articles, add_article, remove_article 
from commands.backup import backup

console = Console()

def force_update():
    """ Pushes all local articles to the server. In most cases, you should use sync() instead."""
    backup()
    local_articles = parse_articles()
    server_articles = get_articles()

    console.print("Initiating force update...", style="yellow")

    # Remove all articles from server
    for article in server_articles:
        remove_article(article['title'])
        console.print(f"Removed {article['title']}", style="red")

    # Add all articles from local directory
    for article in local_articles:
        add_article(article)
        console.print(f"Added {article['title']}", style="green")

    console.print("Force update complete.", style="bold cyan")
