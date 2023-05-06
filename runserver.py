"""regserver module
Server for the song recommendation application
"""

# library modules
import sys
from argparse import ArgumentParser
from os import path

# custom modules
from song import app

# CLI

def parse_args() -> dict:
    """Parse command-line arguments"""

    parser = ArgumentParser(description="Server for the song recommendation application",
                            allow_abbrev=False)

    parser.add_argument(
        "port",
        metavar="port",
        type=int,
        help="the port at which the server should listen"
    )

    args = parser.parse_args()

    return vars(args)

def server_run(port: int) -> None:
    """Run the Flask application server"""

    try:
        app.run(host='0.0.0.0', port=port, debug=True)
    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

def main():
    """Sets up and runs Flask application"""
    args = parse_args()
    port = args.get("port")
    server_run(port)


if __name__ == '__main__':
    main()