from urllib.parse import urlparse
from tcp import connect, connect_tls


class Response:
    def __init__(self, status, headers, body):
        self.status = status
        self.headers = headers  # lowercase keys
        self.body = body


# send a GET request and return a Response
def fetch(url):
    parsed = urlparse(url)
    host = parsed.hostname
    port = parsed.port
    path = parsed.path or "/"
    if parsed.query:
        path += "?" + parsed.query

    if parsed.scheme == "https":
        port = port or 443
        conn = connect_tls(host, str(port))
    else:
        port = port or 80
        conn = connect(host, str(port))

    req = f"GET {path} HTTP/1.1\r\n"
    req += f"Host: {host}\r\n"
    req += "Connection: close\r\n"
    req += "User-Agent: go2web/1.0\r\n"
    req += "Accept-Encoding: identity\r\n"
    req += "\r\n"

    conn.sendall(req.encode())

    # read everything
    data = b""
    while True:
        chunk = conn.recv(4096)
        if not chunk:
            break
        data += chunk
    conn.close()

    return _parse(data.decode("utf-8", errors="replace"))


def _parse(raw):
    idx = raw.find("\r\n\r\n")
    if idx < 0:
        raise Exception("bad response")

    head = raw[:idx]
    body = raw[idx + 4:]

    lines = head.split("\r\n")
    status = int(lines[0].split(" ")[1])

    headers = {}
    for line in lines[1:]:
        if ":" in line:
            k, v = line.split(":", 1)
            headers[k.strip().lower()] = v.strip()

    # handle chunked
    if "chunked" in headers.get("transfer-encoding", ""):
        body = _dechunk(body)

    return Response(status, headers, body)


def _dechunk(s):
    result = []
    while s:
        nl = s.find("\r\n")
        if nl < 0:
            break
        size_str = s[:nl].split(";")[0].strip()
        try:
            n = int(size_str, 16)
        except ValueError:
            break
        if n == 0:
            break
        s = s[nl + 2:]
        result.append(s[:n])
        s = s[n + 2:]
    return "".join(result)
