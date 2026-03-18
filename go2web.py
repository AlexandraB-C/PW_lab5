#!/usr/bin/env python3
import sys
from http_client import fetch
from parser import strip_html
from search import search
from cache import cache_get, cache_set


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
        do_search(" ".join(args[1:]))

    else:
        print(f"unknown flag: {args[0]}", file=sys.stderr)
        print_help()
        sys.exit(1)


def do_url(url):
    cached, found = cache_get(url)
    if found:
        print(cached)
        return

    try:
        resp = fetch(url)
    except Exception as e:
        print(f"error: {e}", file=sys.stderr)
        sys.exit(1)

    out = strip_html(resp.body)
    cache_set(url, out)
    print(out)


def do_search(term):
    try:
        results = search(term)
    except Exception as e:
        print(f"error: {e}", file=sys.stderr)
        sys.exit(1)

    if not results:
        print("no results found")
        return

    for i, r in enumerate(results, 1):
        print(f"{i}. {r['title']}")
        print(f"   {r['url']}")
        if r["desc"]:
            print(f"   {r['desc']}")
        print()


def print_help():
    print("go2web - simple web cli")
    print()
    print("usage:")
    print("  go2web -u <URL>          fetch a url and print it")
    print("  go2web -s <search term>  search and show top 10 results")
    print("  go2web -h                show this help")


if __name__ == "__main__":
    main()
