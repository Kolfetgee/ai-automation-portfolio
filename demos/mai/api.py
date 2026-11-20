"""Safe localhost-only JSON API wrapper for a deterministic mock agent."""
from __future__ import annotations

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from .agent import Agent

MAX_PAYLOAD = 8192


def make_handler(agent: Agent):
    class Handler(BaseHTTPRequestHandler):
        def _send(self, status: int, payload: dict) -> None:
            encoded = json.dumps(payload, ensure_ascii=True).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(encoded)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(encoded)

        def do_GET(self) -> None:
            if self.path == "/health":
                self._send(200, {"status": "ok", "mode": "deterministic_mock"})
            else:
                self._send(404, {"error": "not_found"})

        def do_POST(self) -> None:
            if self.path != "/turn":
                self._send(404, {"error": "not_found"})
                return
            try:
                raw_size = self.headers.get("Content-Length", "")
                if not raw_size.isdecimal():
                    raise ValueError("Content-Length required")
                length = int(raw_size)
                if not 1 <= length <= MAX_PAYLOAD:
                    raise ValueError("Payload size out of bounds")
                if self.headers.get_content_type() != "application/json":
                    raise ValueError("Expected application/json")
                payload = json.loads(self.rfile.read(length))
                if not isinstance(payload, dict) or set(payload) != {"message"}:
                    raise ValueError("Expected exactly one JSON field: message")
                response = agent.turn(payload["message"])
            except (ValueError, TypeError, UnicodeDecodeError, json.JSONDecodeError):
                self._send(400, {"error": "invalid_request"})
                return
            self._send(200, response)

        def log_message(self, format: str, *args) -> None:
            # Avoid echoing arbitrary request contents to a log.
            pass

    return Handler


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description="Synthetic local memory/agent mock API")
    parser.add_argument("--port", type=int, default=8788)
    port = parser.parse_args().port
    if not 1024 <= port <= 65535:
        parser.error("port must be in 1024-65535")
    server = HTTPServer(("127.0.0.1", port), make_handler(Agent()))
    print(f"Local-only deterministic mock available at http://127.0.0.1:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
