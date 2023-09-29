from rich.console import Console
from rich import print
from utils.parse_md import parse_articles 
from utils.crud import get_articles, add_article, remove_article, update_article
from utils.compare import compare
from commands.backup import backup

console = Console()

def sync():
    backup()
    local_articles = parse_articles()
    server_articles = get_articles()

    to_add, to_remove, to_update = compare(local_articles, server_articles)

    if len(to_add) == 0 and len(to_remove) == 0 and len(to_update) == 0:
        console.print("No changes detected.", style="bold cyan")
        return

    for article in to_add:
        add_article(article)
        console.print(f"Added {article['title']}", style="green")

    for article in to_remove:
        remove_article(article['title'])
        console.print(f"Removed {article['title']}", style="red")

    for article in to_update:
        update_article(article['title'], article)

    console.print("Sync complete.", style="bold cyan")
