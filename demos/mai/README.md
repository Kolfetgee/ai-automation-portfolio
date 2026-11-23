# MAI-inspired stateful agent mock

This is a **generic, newly written** local demonstration of a stateful agent interface: finite local memory, deterministic response rules, explicit escalation when a rule is missing, STOP/silence, and a small JSON-over-HTTP API. It is **not an LLM**, not the MAI project's private implementation, and it contains **no game assets, characters, names, scripts, or third-party data**.

## Open the local console

From the repository root, run:

```bash
python -m demos.mai.api --port 8788
```

Open **http://127.0.0.1:8788/** in a browser. The page uses plain HTML, CSS and JavaScript served by the Python process. It needs no build step, network service or API key.

| Send in order | Look for |
| --- | --- |
| `hello` | A fixed greeting and the `reply` action. |
| `remember: blue`, then `recall` | The reply contains `blue`. A fresh server shows one memory item. |
| `unlisted command` | `escalate` requests human review. |
| `stop`, then `hello` | Both turns return `silence` and state `STOP`. |

The page shows the latest successful turn in this tab. Refreshing clears that display. All clients of the same process share one agent and its five-note buffer. Restart the server for a fresh demonstration.

Run `python -m unittest tests.test_mai -v` to check the HTTP routes and agent. Run `node --test tests/mai_console.test.cjs` with Node.js 20+ to check the browser submit handler. Node.js is only needed for that test.

## Use the JSON API

With the server running, try these from a second shell (Bash syntax):

```bash
curl http://127.0.0.1:8788/health
curl -X POST http://127.0.0.1:8788/turn -H "Content-Type: application/json" -d '{"message":"hello"}'
curl -X POST http://127.0.0.1:8788/turn -H "Content-Type: application/json" -d '{"message":"remember: synthetic project flag"}'
curl -X POST http://127.0.0.1:8788/turn -H "Content-Type: application/json" -d '{"message":"recall"}'
```

Use `Ctrl+C` to stop the server. The server binds only to `127.0.0.1`. The memory exists in RAM only and resets when the process exits. No authentication, encryption, persistence, model calls, or external APIs are present. Do not enter private, medical, customer, or company information.

The mock's purpose is to demonstrate **control flow**, HTTP validation and predictable behavior before connecting a real model. A real business integration would require explicit data governance, authorization, logging and security decisions, model evaluations, monitoring and human approval.
