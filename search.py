import re
from http_client import fetch
from parser import strip_html


def search(term):
    # duckduckgo html version, no js needed
    q = term.replace(" ", "+")
    resp = fetch("https://html.duckduckgo.com/html/?q=" + q)
    if resp.status != 200:
        raise Exception(f"search returned status {resp.status}")
    return parse_ddg(resp.body)


def parse_ddg(body):
    results = []
    # each result block starts after class="result__a"
    chunks = body.split('class="result__a"')

    for chunk in chunks[1:]:
        if len(results) >= 10:
            break

        href = extract_attr(chunk, "href")
        # ddg wraps real urls in /l/?uddg= redirects
        if "uddg=" in href:
            href = ddg_unwrap(href)

        # title is between > and </a>
        title = ""
        m = re.search(r">([^<]+)</a>", chunk)
        if m:
            title = m.group(1).strip()

        # snippet is after result__snippet class
        desc = ""
        si = chunk.find("result__snippet")
        if si >= 0:
            m2 = re.search(r">(.+?)</", chunk[si:])
            if m2:
                desc = strip_html(m2.group(1)).strip()

        if not title or not href:
            continue

        results.append({"title": title, "url": href, "desc": desc})

    return results


def extract_attr(s, attr):
    needle = attr + '="'
    idx = s.find(needle)
    if idx < 0:
        return ""
    rest = s[idx + len(needle):]
    end = rest.find('"')
    return rest[:end] if end >= 0 else ""


def ddg_unwrap(href):
    # pull the real url out of uddg=<percent-encoded-url>
    idx = href.find("uddg=")
    if idx < 0:
        return href
    encoded = href[idx + 5:]
    if "&" in encoded:
        encoded = encoded[:encoded.index("&")]
    return url_decode(encoded)


def url_decode(s):
    result = []
    i = 0
    while i < len(s):
        if s[i] == "%" and i + 2 < len(s):
            result.append(chr(int(s[i+1:i+3], 16)))
            i += 3
        elif s[i] == "+":
            result.append(" ")
            i += 1
        else:
            result.append(s[i])
            i += 1
    return "".join(result)
