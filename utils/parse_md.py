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
    titles = set()
    related_titles = set()

    for md_file in os.listdir(MD_DIR):
        if md_file.endswith('.md'):
            try:
                with open(os.path.join(MD_DIR, md_file), 'r', encoding='utf-8') as f:
                    post = frontmatter.load(f)
            except Exception as e:
                raise Exception(f"Error parsing {md_file}: {e}")

            try:
                title = os.path.splitext(md_file)[0]
            except Exception as e:
                raise Exception(f"Error parsing {md_file}: {e}")

            try:
                preview = post.metadata.get('preview', '')
            except Exception as e:
                raise Exception(f"Error parsing {md_file}: {e}")

            try:
                content = post.content
            except Exception as e:
                raise Exception(f"Error parsing {md_file}: {e}")

            try:
                tags = post.metadata.get('tags', [])
            except Exception as e:
                raise Exception(f"Error parsing {md_file}: {e}")

            try:
                relatedArticles = post.metadata.get('relatedArticles', [])
            except Exception as e:
                raise Exception(f"Error parsing {md_file}: {e}")

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
                'tags': tags,
                'relatedArticles': relatedArticles
            }

            # Collect titles and related article titles (for validation)
            articles.append(article)
            titles.add(title)

            for relatedArticle in relatedArticles:
                related_titles.add(relatedArticle)

    if len(articles) == 0:
        console.print("No articles found in local directory.", style="bold red")
    else:
        console.print(f"Found {len(articles)} articles in local directory.", style="green")

    # Make sure all related articles exist
    for relatedArticle in related_titles:
        if relatedArticle not in titles:
            raise Exception(f"Related article {relatedArticle} does not match any existing article title. Please check your metadata.")

    return articles


