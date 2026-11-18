import json
import logging
import os
import re
import sqlite3
from datetime import datetime, timezone
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = Path(os.environ.get("PORTFOLIO_DB_PATH", BASE_DIR / "data" / "messages.sqlite3"))
HOST = os.environ.get("PORTFOLIO_HOST", "127.0.0.1")
PORT = int(os.environ.get("PORT", "8000"))
MAX_REQUEST_SIZE = 32 * 1024
EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def initialize_database():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS contact_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                message TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )


class PortfolioHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(BASE_DIR), **kwargs)

    def do_GET(self):
        if urlsplit(self.path).path == "/api/health":
            self._send_json(200, {"status": "ok"})
            return
        super().do_GET()

    def do_POST(self):
        if urlsplit(self.path).path != "/api/contact":
            self._send_json(404, {"error": "Not found."})
            return

        if self.headers.get_content_type() != "application/json":
            self._send_json(415, {"error": "Content-Type must be application/json."})
            return

        try:
            request_size = int(self.headers.get("Content-Length", ""))
        except ValueError:
            self._send_json(400, {"error": "A valid Content-Length is required."})
            return
        if request_size < 0 or request_size > MAX_REQUEST_SIZE:
            self._send_json(413, {"error": "The request is too large."})
            return

        try:
            payload = json.loads(self.rfile.read(request_size).decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            self._send_json(400, {"error": "The request must contain valid JSON."})
            return
        if not isinstance(payload, dict):
            self._send_json(400, {"error": "The request must be a JSON object."})
            return

        name = payload.get("name")
        email = payload.get("email")
        message = payload.get("message")
        if not all(isinstance(value, str) for value in (name, email, message)):
            self._send_json(400, {"error": "Name, email, and message are required."})
            return

        name, email, message = name.strip(), email.strip(), message.strip()
        if not name or len(name) > 100:
            self._send_json(400, {"error": "Name must be between 1 and 100 characters."})
            return
        if len(email) > 254 or not EMAIL_PATTERN.fullmatch(email):
            self._send_json(400, {"error": "Enter a valid email address."})
            return
        if not message or len(message) > 5000:
            self._send_json(400, {"error": "Message must be between 1 and 5000 characters."})
            return

        try:
            with sqlite3.connect(DB_PATH) as connection:
                connection.execute(
                    "INSERT INTO contact_messages (name, email, message, created_at) VALUES (?, ?, ?, ?)",
                    (name, email, message, datetime.now(timezone.utc).isoformat()),
                )
        except sqlite3.Error:
            logging.exception("Could not save contact message")
            self._send_json(500, {"error": "Your message could not be saved. Please try again later."})
            return

        self._send_json(201, {"message": "Thanks for reaching out! Your message has been received."})

    def _send_json(self, status, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    initialize_database()
    server = ThreadingHTTPServer((HOST, PORT), PortfolioHandler)
    print("Portfolio server running at http://{}:{}".format(HOST, PORT), flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping portfolio server.", flush=True)
    finally:
        server.server_close()
