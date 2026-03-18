# go2web

A command-line web browser using raw TCP sockets. No HTTP libraries.

## Usage

```
go2web -h                   show help
go2web -u <URL>             fetch a URL and print the response
go2web -s <search term>     search and print top 10 results
```

## Setup

```bash
# Windows
go2web.bat -u https://example.com

# or directly
python go2web.py -u https://example.com
```

## Demo

![demo](demo.gif)

## Notes

- Uses raw TCP sockets (`socket` module) and `ssl` for HTTPS
- No `requests`, no `urllib.request`, no `http.client`
- File-based cache in `.cache/`
- Handles HTTP redirects (301, 302, 303, 307, 308)
- Content negotiation: JSON and HTML both supported
