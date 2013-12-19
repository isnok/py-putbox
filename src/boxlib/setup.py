from argparse import ArgumentParser

parser = ArgumentParser(description="putbox launcher")

parser.add_argument(
        '-d', '--debug', default=False, action="store_true",
        help="debug flag (may add some debug output)"
    )
parser.add_argument(
        "-p", "--port", type=int, default=7331,
        help="port to serve on"
    )
parser.add_argument(
        "-i", "--interface", type=str, default='',
        help="interface to serve on"
    )
parser.add_argument(
        "-P", "--passwordfile", type=str, default='putbox.passwd',
        help="password file to use"
    )
parser.add_argument(
        "-D", "--database", type=str, default='linkstore.db',
        help="sqlite3 db file to use"
    )

args = parser.parse_args()
