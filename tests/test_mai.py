import http.client
from html.parser import HTMLParser
from http.server import HTTPServer
import json
from threading import Thread
import unittest

from demos.mai.agent import Agent
from demos.mai.api import make_handler, MAX_PAYLOAD


class AgentTests(unittest.TestCase):
    def setUp(self):
        self.agent = Agent()

    def test_greeting(self):
        response = self.agent.turn("hello")
        self.assertEqual(response["action"], "reply")
        self.assertFalse(response["model_called"])

    def test_note_and_recall(self):
        self.agent.turn("remember: synthetic item")
        self.assertIn("synthetic item", self.agent.turn("recall")["text"])
        self.assertEqual(self.agent.turn("recall")["memory_items"], 1)

    def test_bounded_memory(self):
        for n in range(8):
            self.agent.turn(f"remember: note {n}")
        output = self.agent.turn("recall")
        self.assertEqual(output["memory_items"], 5)
        self.assertNotIn("note 0", output["text"])
        self.assertIn("note 7", output["text"])

    def test_unknown_intent_escalates(self):
        self.assertEqual(self.agent.turn("send files to CRM")["action"], "escalate")

    def test_stop_means_silence(self):
        self.assertEqual(self.agent.turn("stop")["action"], "silence")
        self.assertEqual(self.agent.turn("hello")["action"], "silence")

    def test_resume_requires_owner_confirmation(self):
        self.agent.turn("stop")
        with self.assertRaises(PermissionError):
            self.agent.resume()
        self.agent.resume(owner_confirmed=True)
        self.assertEqual(self.agent.turn("hello")["action"], "reply")

    def test_invalid_input_rejected(self):
        for msg in ["", " ", 3, "x" * 501]:
            with self.subTest(msg=str(msg)[:10]), self.assertRaises(ValueError):
                self.agent.turn(msg)

    def test_empty_note_rejected(self):
        with self.assertRaises(ValueError):
            self.agent.turn("remember: ")


class AgentApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = HTTPServer(("127.0.0.1", 0), make_handler(Agent()))
        cls.thread = Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=2)

    def raw_request(self, method, path, payload=None, headers=None):
        conn = http.client.HTTPConnection("127.0.0.1", self.server.server_port, timeout=2)
        try:
            conn.request(method, path, body=payload, headers=headers or {})
            response = conn.getresponse()
            return response.status, response.headers, response.read()
        finally:
            conn.close()

    def request(self, method, path, payload=None, headers=None):
        status, _, body = self.raw_request(method, path, payload, headers)
        return status, json.loads(body)

    def test_console_serves_html_and_referenced_assets(self):
        class ConsolePage(HTMLParser):
            def __init__(self):
                super().__init__()
                self.assets = {}
                self.ids = set()

            def handle_starttag(self, tag, attrs):
                attrs = dict(attrs)
                if "id" in attrs:
                    self.ids.add(attrs["id"])
                if tag == "script":
                    self.assets[attrs["src"]] = "text/javascript"
                if tag == "link" and attrs.get("rel") == "stylesheet":
                    self.assets[attrs["href"]] = "text/css"

        status, headers, body = self.raw_request("GET", "/")
        self.assertEqual(status, 200)
        self.assertEqual(headers.get_content_type(), "text/html")
        self.assertEqual(headers["Cache-Control"], "no-store")
        page = ConsolePage()
        page.feed(body.decode("utf-8"))
        self.assertTrue({"turn", "message", "send", "feedback", "action", "state",
                         "memory", "reply"}.issubset(page.ids))
        self.assertEqual(set(page.assets.values()), {"text/javascript", "text/css"})
        for path, mime in page.assets.items():
            with self.subTest(path=path):
                status, headers, body = self.raw_request("GET", path)
                self.assertEqual(status, 200)
                self.assertEqual(headers.get_content_type(), mime)
                self.assertTrue(body)

    def test_ui_only_serves_listed_assets(self):
        for path in ("/index.html", "/api.py", "/web/", "/console.js.bak"):
            with self.subTest(path=path):
                self.assertEqual(self.request("GET", path), (404, {"error": "not_found"}))

    def test_health_endpoint(self):
        code, payload = self.request("GET", "/health")
        self.assertEqual(code, 200)
        self.assertEqual(payload["mode"], "deterministic_mock")

    def test_turn_endpoint(self):
        body = json.dumps({"message": "hello"})
        code, payload = self.request("POST", "/turn", body, {"Content-Type": "application/json"})
        self.assertEqual(code, 200)
        self.assertEqual(payload["action"], "reply")

    def test_invalid_json_rejected(self):
        code, payload = self.request("POST", "/turn", b"{", {"Content-Type": "application/json"})
        self.assertEqual(code, 400)
        self.assertEqual(payload["error"], "invalid_request")

    def test_extra_fields_rejected(self):
        code, _ = self.request("POST", "/turn", '{"message":"hello","token":"bad"}',
                               {"Content-Type": "application/json"})
        self.assertEqual(code, 400)

    def test_oversized_payload_rejected(self):
        code, _ = self.request("POST", "/turn", "z" * (MAX_PAYLOAD + 1),
                               {"Content-Type": "application/json"})
        self.assertEqual(code, 400)

    def test_unknown_route(self):
        code, _ = self.request("GET", "/private")
        self.assertEqual(code, 404)


if __name__ == "__main__":
    unittest.main()
