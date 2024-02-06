import argparse

def get_parser():
    parser = argparse.ArgumentParser(
        description="Manage your blog from the command line."
    )

    subparsers = parser.add_subparsers(dest='command')

    sync_parser = subparsers.add_parser('sync', help='Syncs obsidian vault with blog')  # noqa: F841
    sync_parser.add_argument('-m', '--mute', help="Don't create an activity log for this sync", action='store_true')  # noqa: F841
    list_parser = subparsers.add_parser('list', help='List blog from server')  # noqa: F841
    backup_parser = subparsers.add_parser('backup', help='Backup obsidian vault')  # noqa: F841
    mode_parser = subparsers.add_parser('mode', help='Set mode to either dev or prod')  # noqa: F841
    mode_parser.add_argument('mode', choices=['dev', 'prod'], help='Set mode to either dev or prod')  # noqa: F841
    publish_parser = subparsers.add_parser('publish', help='Publish blog')  # noqa: F841

    return parser
