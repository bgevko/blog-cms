import argparse

def get_parser():
    parser = argparse.ArgumentParser(
        description="Manage your blog from the command line."
    )

    subparsers = parser.add_subparsers(dest='command')

    sync_parser = subparsers.add_parser('sync', help='Syncs obsidian vault with blog')  # noqa: F841
    list_parser = subparsers.add_parser('list', help='List blog from server')  # noqa: F841
    backup_parser = subparsers.add_parser('backup', help='Backup obsidian vault')  # noqa: F841
    force_update = subparsers.add_parser('force-update', help='Replaces every server articles from the local directory. In most cases, use the "sync" command instead.')  # noqa: F841
    

    return parser
