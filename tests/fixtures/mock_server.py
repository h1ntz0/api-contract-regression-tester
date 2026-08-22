import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
from urllib.parse import urlparse, parse_qs


class MockApiHandler(BaseHTTPRequestHandler):
    users = [
        {"id": 1, "username": "john_doe", "email": "john@example.com", "role": "user", "active": True},
        {"id": 2, "username": "alice_admin", "email": "alice@example.com", "role": "admin", "active": True},
    ]
    products = [
        {"id": 101, "title": "Mechanical Keyboard", "price": 89.99, "in_stock": True},
        {"id": 102, "title": "Wireless Mouse", "price": 49.50, "in_stock": True},
    ]

    def log_message(self, format, *args):
        pass  # Suppress default server access logs

    def _send_json(self, status: int, data: any):
        payload = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/users":
            self._send_json(200, self.users)
        elif path.startswith("/users/"):
            uid_str = path.split("/")[-1]
            try:
                uid = int(uid_str)
                user = next((u for u in self.users if u["id"] == uid), None)
                if user:
                    self._send_json(200, user)
                else:
                    self._send_json(404, {"error": "User not found"})
            except ValueError:
                self._send_json(400, {"error": "Invalid user ID format"})
        elif path == "/products":
            self._send_json(200, self.products)
        else:
            self._send_json(404, {"error": "Endpoint not found"})

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path == "/users":
            content_length = int(self.headers.get("Content-Length", 0))
            body_bytes = self.rfile.read(content_length)
            try:
                data = json.loads(body_bytes.decode("utf-8"))
            except Exception:
                self._send_json(400, {"error": "Invalid JSON payload"})
                return

            # Required fields check
            if "username" not in data or "email" not in data or "role" not in data:
                self._send_json(400, {"error": "Missing required fields"})
                return

            if data["role"] not in ("admin", "user", "guest"):
                self._send_json(400, {"error": "Invalid role enum"})
                return

            new_user = {
                "id": len(self.users) + 1,
                "username": data["username"],
                "email": data["email"],
                "role": data["role"],
                "active": data.get("active", True),
            }
            self.users.append(new_user)
            self._send_json(201, new_user)
        else:
            self._send_json(404, {"error": "Endpoint not found"})

    def do_DELETE(self):
        parsed = urlparse(self.path)
        if parsed.path.startswith("/users/"):
            uid_str = parsed.path.split("/")[-1]
            try:
                uid = int(uid_str)
                user = next((u for u in self.users if u["id"] == uid), None)
                if user:
                    self.users.remove(user)
                    self.send_response(204)
                    self.end_headers()
                else:
                    self._send_json(404, {"error": "User not found"})
            except ValueError:
                self._send_json(400, {"error": "Invalid user ID format"})
        else:
            self._send_json(404, {"error": "Endpoint not found"})


def run_mock_server(host="127.0.0.1", port=8000) -> HTTPServer:
    server = HTTPServer((host, port), MockApiHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server
