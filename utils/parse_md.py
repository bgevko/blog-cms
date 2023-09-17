import os
import frontmatter
from dotenv import load_dotenv
from datetime import datetime
from rich.console import Console
from zoneinfo import ZoneInfo

load_dotenv() 
console = Console()

MD_DIR = os.getenv("MD_DIR")

if not MD_DIR:
    raise Exception("MD_DIR is not set")

def parse_articles():
    console.print("Parsing articles from local directory...", style="yellow")
    articles = []
    for md_file in os.listdir(MD_DIR):
        if md_file.endswith('.md'):
            with open(os.path.join(MD_DIR, md_file), 'r', encoding='utf-8') as f:
                post = frontmatter.load(f)

            title = os.path.splitext(md_file)[0]
            preview = post.metadata.get('preview', '')
            content = post.content
            tags = post.metadata.get('tags', [])

            # Created date
            publishDate = datetime.fromtimestamp(
                os.path.getctime(os.path.join(MD_DIR, md_file))
            ).astimezone(ZoneInfo("UTC")).replace(microsecond=0)

            # Last modified date
            editDate = datetime.fromtimestamp(
                os.path.getmtime(os.path.join(MD_DIR, md_file))
            ).astimezone(ZoneInfo("UTC")).replace(microsecond=0)

            # Format date to match mongodb date format
            publishDate = publishDate.strftime("%Y-%m-%dT%H:%M:%S.000Z")
            editDate = editDate.strftime("%Y-%m-%dT%H:%M:%S.000Z")

            # Stop if metadata is not set
            if not preview:
                raise Exception(f"Preview is not set for {md_file}")

            if not tags:
                raise Exception(f"Tags are not set for {md_file}")

            article = {
                'title': title,
                'publishDate': publishDate,
                'editDate': editDate,
                'preview': preview,
                'content': content,
                'tags': tags
            }

            articles.append(article)

    if len(articles) == 0:
        console.print("No articles found in local directory.", style="bold red")
    else:
        console.print(f"Found {len(articles)} articles in local directory.", style="green")
    return articles


