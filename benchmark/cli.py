from easycli import Root, SubCommand, Argument


__version__ = '0.1.0'


class Main(Root):
    __help__ = 'Benchmark'
    __completion__ = True
    __arguments__ = [
        Argument(
            '-V',
            '--version',
            action='store_true',
            help='Show version',
        ),
        Argument(
            'url',
            type=str,
            help='URL',
        ),
        Argument(
            '-t',
            '--thread',
            type=int,
            default=1,
            help='Count of Threads',
        ),
        Argument(
            '-n',
            '--number',
            type=int,
            default=1,
            help='Count of Requests',
        ),
        Argument(
            '-m',
            '--method',
            type=str,
            default='GET',
            help='HTTP Method Name',
        ),
    ]

    def __call__(self, args):
        print('Root command, args:', args)
        if args.version:
            print(__version__)
            return


def main():
        return Main().main()

