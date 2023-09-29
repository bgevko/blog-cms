#!/usr/bin/env python3
from cmd_parser import get_parser
from commands.sync import sync
from commands.list import list
from commands.backup import backup
from commands.force_update import force_update
from rich.traceback import install
install()


def main():
    parser = get_parser()
    args = vars(parser.parse_args())

    if args['command'] == 'sync':
        sync()
    elif args['command'] == 'list':
        list()
    elif args['command'] == 'backup':
        backup()
    elif args['command'] == 'force-update':
        force_update()

if __name__ == "__main__":
    main()

