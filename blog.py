#!/usr/bin/env python3
from cmd_parser import get_parser
from commands.sync import sync
from commands.list import list
from commands.backup import backup
from utils.set_env import set_env
from rich.traceback import install
install()

def main():
    parser = get_parser()
    args = vars(parser.parse_args())

    if args['command'] == 'sync':
        if args['mute']:
            sync(mute=1)
        else:
            sync()
    elif args['command'] == 'backup':
        backup()
    elif args['command'] == 'list':
        list()
    elif args['command'] == 'mode':
        if args['mode'] == 'dev':
            set_env('dev')
        elif args['mode'] == 'prod':
            set_env('prod')
        else:
            parser.parse_args(['mode', '--help'])

if __name__ == "__main__":
    main()

