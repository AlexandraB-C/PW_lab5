#!/usr/bin/env python3
import sys
from http_client import fetch
from parser import strip_html


def main():
    args = sys.argv[1:]

    if not args or args[0] == "-h":
        print_help()
        return

    if args[0] == "-u":
        if len(args) < 2:
            print("usage: go2web -u <URL>", file=sys.stderr)
            sys.exit(1)
        do_url(args[1])

    elif args[0] == "-s":
        if len(args) < 2:
            print("usage: go2web -s <search term>", file=sys.stderr)
            sys.exit(1)
        print("search not implemented yet", file=sys.stderr)
        sys.exit(1)

    else:
        print(f"unknown flag: {args[0]}", file=sys.stderr)
        print_help()
        sys.exit(1)


def do_url(url):
    try:
        resp = fetch(url)
    except Exception as e:
        print(f"error: {e}", file=sys.stderr)
        sys.exit(1)

    print(strip_html(resp.body))


def print_help():
    print("go2web - simple web cli")
    print()
    print("usage:")
    print("  go2web -u <URL>          fetch a url and print it")
    print("  go2web -s <search term>  search and show top 10 results")
    print("  go2web -h                show this help")


if __name__ == "__main__":
    main()
