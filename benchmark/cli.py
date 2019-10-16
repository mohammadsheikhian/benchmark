from easycli import Root, SubCommand, Argument


__version__ = '0.1.0'
DEFAULT_TCP_PORT = 8585
DEFAULT_HOST = 'WPP.local'


class Run(SubCommand):
    __command__ = 'run'
    __aliases__ = ['r']
    __arguments__ = [
        Argument(
            '-u',
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
        print('Sub command 1, args:', args)


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
        Run,
    ]

    def __call__(self, args):
        if args.version:
            print(__version__)
            return

        return super().__call__(args)


def main():
        return Main().main()

