# Blog CMS
This is a Python command line tool that parses markdown files from a local directory and sends updated posts information to a specified endpoint. 

## Usage
### Clone the repo
```bash
git clone https://github.com/bgevko/blog-cms.git
```

```bash
### Create a virtual environment 
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies
```bash
pip3 install -r requirements.txt
```

### Create a `.env` file:
```text
API_URL=https://www.yoursite.com
DEV_API_URL=http://localhost:3000
ENV=prod
MD_DIR=/path/to/markdown_files
GIT_URL=https://github.com/yourgithub/your_blog_backup_repo.git
```

- `API_URL`: Production URL for your server
- `DEV_API_URL`: Set this to the same URL as your dev server.
- `ENV`: Set this to `prod` or `dev`. This will ensure the appropriate URL is used for the appropriate environment.
- `MD_DIR`: Directory to where your markdown files sit. I recommend making this an Obsidian vault.
- `GIT_URL`: Set up a repo for an additional source of backup for your markdown files. 

### Example.md
```md
---
preview: This is a preview of the article. It can be as short or as long as you want. The purpose of this block of text is to give the reader a preview of article contents.
tags:
  - Markdown
  - Example
---

# Main Content
The main content goes here
```

Each markdown article must have a `preview` and a `tags` attribute, placed between two `---` at the very top of the markdown file.

### Assumed Backend Endpoints (crud.py)
**get_articles()**: `GET API_URL/blog`
**add_article()**: `POST API_URL/blog`, **body**: `article_object` (see below)
**remove_article()**: `DELETE API_URL/blog/encoded_title_url` (title must be URL encoded on the backend)
**update_article()**: `PUT API_URL/blog/encoded_title_url`, **body**: `article_object`

### Assumed Article Structure (Can be changed in **crud.py** and **parse_md.py** )

```Python
 data = response.json()
    articles = []

    for article in data:
        articles.append({
            'title': article['title'],
            'publishDate': article['publishDate'],
            'editDate': article['editDate'],
            'preview': article['preview'],
            'content': article['content'],
            'tags': article['tags']
        })

```

#### Mangoose Schema I used:
```js
const articleSchema = mongoose.Schema({
	title:          { type: String, required: true },
  publishDate:    { type: Date,   required: true },
  editDate:       { type: Date,   required: true },
  preview:        { type: String, required: true},
  content:        { type: String, required: true },
  tags:           { type: [String], required: true, set: tags => [...new Set(tags)] },
  readTime:       { type: Number, default: 1},
  relativePath:   { type: String, required: true },
});
```

The `get_articles` in `crud.py` assumes the returned method from the request will be a list of objects containing (at a minimum) the following attributes: `title`, `publishDate`, `editDate`, `preview`, `content`, `tags`. Other attributes can be used in the Schema, but the tool won't work if one or more of these are missing. 


### Usage Command
From the terminal, in the root directory:

- Test to see if the GET endpoint works
```bash
 python3 blog.py list
```

- The sync command makes the server articles reflect exactly what's in the markdown directory. If you add, change, or remove a file, this command will perform the appropriate operations. 
```bash
python3 blog.py sync
```

- The backup command command is called every time the sync command is used. It can also be called manually:
```bash
python3 blog.py backup
```

### (Optional but recommended) Make this script available from anywhere in the terminal
You can create a system link and call this script from anywhere in the terminal:
- From the directory of the file, link it to `/usr/local/bin/blog:
  ```bash
  sudo -ln -s $(pwd)/blog.py /usr/local/bin/blog
  ```
- Give the file executable permissions:
  ```bash
  chmod +x $(pwd)/blog.py
  ```
- Restart your terminal
- Now, you should be able to call the command like this from anywhere in your terminal, not just the root directory:
```bash
blog list
blog sync
blog update
```
