import os
import socket
import ssl

from html_entities import replace_html_entities

class URL:
    def __init__(self, url):
        self.view_source = False

        if url.startswith('view-source:'):
            url = url.split('view-source:')[1]
            self.scheme, url = url.split("://", 1)
            self.view_source = True
        elif '://' in url:
            self.scheme, url = url.split("://", 1)
        else:
            self.scheme, url = url.split(":", 1)

        assert self.scheme in ["http", "https", "file", "data"]

        if self.scheme == "http":
            self.port = 80
        elif self.scheme == "https":
            self.port = 443
        elif self.scheme == "file":
            self.file_path = url
        elif self.scheme == "data":
            self.data = url

        if "/" not in url:
            url = url + "/"
        self.host, url = url.split("/", 1)

        if ":" in self.host:
            self.host, port = self.host.split(":", 1)
            self.port = int(port)

        self.path = "/" + url
        self.socket = None

    def connect_socket(self):
        if self.socket is None:
            s = socket.socket(
                family=socket.AF_INET,
                type=socket.SOCK_STREAM,
                proto=socket.IPPROTO_TCP,
            )
            s.connect((self.host, self.port))

            if self.scheme == "https":
                ctx = ssl.create_default_context()
                s = ctx.wrap_socket(s, server_hostname=self.host)

            self.socket = s  # Save the socket for reuse
        return self.socket

    def close_socket(self):
        if self.socket:
            self.socket.close()
            self.socket = None

    def request(self, redirect_limit=5):
        if redirect_limit <= 0:
            raise Exception("Too many redirects")

        s = self.connect_socket()

        request = "GET {} HTTP/1.0\r\n".format(self.path)
        request += "Host: {}\r\n".format(self.host)
        request += "Connection: close\r\n"  # Close connection after the response
        request += "User-Agent: stokebrowser/1.0\r\n"
        request += "\r\n"

        s.send(request.encode("utf8"))

        response = s.makefile("r", encoding="utf8", newline="\r\n")

        # Read the status line
        statusline = response.readline()
        version, status, explanation = statusline.split(" ", 2)

        response_headers = {}
        while True:
            line = response.readline()
            if line == "\r\n":
                break
            header, value = line.split(":", 1)
            response_headers[header.casefold()] = value.strip()

        # Handle redirect (301, 302)
        if status == '301' or status == '302':
            redir = response_headers.get('location')
            if redir:
                print('*', 'redirect to', '*', redir)
                self.close_socket()  # Close current socket before redirecting
                return load(URL(redir), redirect_limit - 1)  # Recursive call with reduced limit
            else:
                raise Exception(f"Redirect status {status} without a Location header")

        # Ensure transfer-encoding and content-encoding are not in the headers
        assert "transfer-encoding" not in response_headers
        assert "content-encoding" not in response_headers

        content_length = int(response_headers.get('content-length', 0))
        content = response.read(content_length)  # Read the content based on content-length

        self.close_socket()  # Ensure socket is closed after the request
        return content

    def local_file(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                return file.read()
        else:
            return "404 Not Found: File does not exist."

    def raw_data(self):
        return self.data.split('text/html,', 1)

def show(body, view_source):
    if view_source:
        print(body, end="")
        return

    in_tag = False
    for c in body:
        if c == "<":
            in_tag = True
        elif c == ">":
            in_tag = False
        elif not in_tag:
            print(replace_html_entities(c), end="")

def get_body(url):
    if url.scheme == "file":
        return url.local_file()
    if url.scheme == "data":
        return url.raw_data()

    # Ensure the request returns a valid string, if not, default to empty string
    body = url.request()
    return body if body is not None else ""  # Ensure we return a non-None value


def load(url, redirect_limit=5):
    show(get_body(url), url.view_source)

if __name__ == "__main__":
    import sys
    arg = sys.argv[1] if len(sys.argv) > 1 else 'file:///Users/Sean.M.Stephenson/hello'
    load(URL(arg))
