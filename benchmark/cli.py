from easycli import Root, SubCommand, Argument

from benchmark.thread_request import run


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
        Argument(
            '-f',
            '--form',
            action='append',
            type=str,
            help='Form Parameters',
        ),
        Argument(
            '-H',
            '--headers',
            action='append',
            type=str,
            help='Headers',
        ),
    ]

    def __call__(self, args):
        headers = dict(tuple(i.split('=')) for i in args.headers) \
            if args.headers else None
        form = dict(tuple(i.split('=')) for i in args.form) \
            if args.form else None

        run(
            args.number,
            args.thread,
            args.url,
            args.method,
            form,
            headers
        )


def main():
        return Main().main()

