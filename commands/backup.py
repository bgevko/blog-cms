import os
from git import Repo
from dotenv import load_dotenv
from rich.console import Console

load_dotenv()
console = Console()

# Path to the repository
path = os.getenv('GIT_LOCAL_DIR')
git_url = os.getenv('GIT_URL')


def backup():
    console.print('Attempting to push to git...', style='yellow')

    try:
        # Commit message
        msg = 'Content: Automated backup'

        # Create Repo object
        repo = Repo(path)

        # Check if there are any changes
        if repo.is_dirty():
            # Add all files to index
            repo.git.add('--all')

            # Commit changes
            repo.index.commit(msg)

            # Push changes
            origin = repo.remote(name='origin')
            origin.push()

            console.print('Backup successful', style='green')
        else:
            console.print('No changes', style='yellow')
    except Exception as e:
        console.print('Backup failed', style='red')
        print(e)
