import html
from http import HTTPStatus
import http.server
import io
import os

import sys
import urllib

dir_path = os.path.dirname(os.path.realpath(__file__))


class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, directory=f"{dir_path}/..", **kwargs):
        super().__init__(directory=directory, *args, **kwargs)

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        super().end_headers()

    def list_directory(self, path):
        try:
            file_list = os.listdir(path + "/game_recordings")
        except OSError:
            self.send_error(HTTPStatus.NOT_FOUND, "No permission to list directory")
            return None
        file_list.sort(key=lambda a: a.lower())
        r = []
        try:
            displaypath = urllib.parse.unquote(self.path, errors="surrogatepass")
        except UnicodeDecodeError:
            displaypath = urllib.parse.unquote(self.path)
        displaypath = html.escape(displaypath, quote=False)
        enc = sys.getfilesystemencoding()
        title = "Recorded games"
        r.append("<!DOCTYPE HTML>")
        r.append('<html lang="en">')
        r.append("<head>")
        r.append(f'<meta charset="{enc}">')
        r.append(f"<title>{title}</title>\n</head>")
        r.append(f"<body>\n<h1>{title}</h1>")
        r.append("<hr>\n<ul>")
        for name in file_list:
            displayname = name.replace(".json.gz", "")
            r.append(
                f'<li><a href="http://localhost:8000/game_draw/browser_display.html?f={displayname}">{displayname}</a></li>'
            )

        r.append("</ul>\n<hr>\n</body>\n</html>\n")
        encoded = "\n".join(r).encode(enc, "surrogateescape")
        f = io.BytesIO()
        f.write(encoded)
        f.seek(0)
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-type", "text/html; charset=%s" % enc)
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        return f


def run(port=8000):
    http.server.test(HandlerClass=CustomHTTPRequestHandler, port=port)

if __name__ == '__main__':
    run()
