import socket
import ssl


# open a raw tcp connection
def connect(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, int(port)))
    return s


# wrap tcp with tls for https
def connect_tls(host, port):
    ctx = ssl.create_default_context()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, int(port)))
    return ctx.wrap_socket(s, server_hostname=host)
