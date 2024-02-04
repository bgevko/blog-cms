import os
import frontmatter
from dotenv import load_dotenv
from rich.console import Console

load_dotenv() 
console = Console()

BLOG_DIR = os.getenv("BLOG_DIR")
NOTES_DIR = os.getenv("NOTES_DIR")
PROJECTS_DIR = os.getenv("PROJECTS_DIR")

if not BLOG_DIR or not NOTES_DIR or not PROJECTS_DIR:
    raise Exception("One or more of BLOG_DIR, NOTES_DIR, PROJECTS_DIR is not set")

def parse_articles():
    articles = []
    console.print("Parsing articles from local directory...", style="yellow")
    articles.extend(parse_articles_from(BLOG_DIR))
    articles.extend(parse_articles_from(NOTES_DIR))
    articles.extend(parse_articles_from(PROJECTS_DIR))
    print("")
    return articles

def parse_articles_from(path):
    articles = []

    for md_file in os.listdir(path):
        article_type = path.split('/')[-1]
        if md_file.endswith('.mdx'):
            try:
                with open(os.path.join(path, md_file), 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception as e:
                raise Exception(f"Error parsing {md_file}: {e}")

            try:
                slug = os.path.splitext(md_file)[0]
            except Exception as e:
                raise Exception(f"Error parsing {md_file}: {e}")

            try:
                title = frontmatter.loads(content).metadata.get('title')
            except Exception as e:
                raise Exception(f"Error parsing {md_file}: {e}")

            article = {
                'type': article_type,
                'slug': slug,
                'content': content,
                'title': title
            }
            articles.append(article)

    if len(articles) == 0:
        console.print("No articles found in local directory.", style="bold red")
    else:
        console.print(f"Found {len(articles)} articles in {path}.", style="green")

    return articles


