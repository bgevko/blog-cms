from rich.console import Console
from rich import print
from utils.parse_md import parse_articles 
from utils.crud import get_articles, add_article, remove_article, update_article
from utils.compare import compare
from commands.backup import backup

console = Console()

def sync(mute=0):
    backup()
    local_articles = parse_articles()

    # Split local articles into three lists, blog, projects, and notes, based on the 'type' key
    local_articles = {
        'blog': [article for article in local_articles if article['type'] == 'blog'],
        'projects': [article for article in local_articles if article['type'] == 'projects'],
        'notes': [article for article in local_articles if article['type'] == 'notes']
    }
    console.print('Retrieving server articles...', style="yellow")
    server_articles = {
        'blog': get_articles('blog'),
        'projects': get_articles('projects'),
        'notes': get_articles('notes')
    }
    print("")
    sync_lists('blog', local_articles['blog'], server_articles['blog'], mute=mute)
    sync_lists('projects', local_articles['projects'], server_articles['projects'], mute=mute)
    sync_lists('notes', local_articles['notes'], server_articles['notes'], mute=mute)
    print("")
    console.print("Done!", style="bold green")

def sync_lists(type, local_articles, server_articles, mute=0):
    to_add, to_remove, to_update = compare(local_articles, server_articles)

    console.print(f"{type} ------------------------------------", style="bold cyan")
    if len(to_add) == 0 and len(to_remove) == 0 and len(to_update) == 0:
        console.print("No changes..\n", style="bold green")
        return

    console.print(f"{len(to_add)} articles to add, {len(to_remove)} articles to remove, and {len(to_update)} articles to update.", style="yellow")
    for article in to_add:
        add_article(article, type, mute=mute)

    for article in to_remove:
        remove_article(article['slug'], type, mute=mute)

    for article in to_update:
        update_article(article['slug'], article, type, mute=mute)

    print("")
