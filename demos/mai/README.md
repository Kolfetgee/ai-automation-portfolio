# MAI-inspired stateful agent mock

This is a **generic, newly written** local demonstration of a stateful agent interface: finite local memory, deterministic response rules, explicit escalation when a rule is missing, STOP/silence, and a small JSON-over-HTTP API. It is **not an LLM**, not the MAI project's private implementation, and it contains **no game assets, characters, names, scripts, or third-party data**.

```bash
python -m demos.mai.api --port 8788
curl http://127.0.0.1:8788/health
curl -X POST http://127.0.0.1:8788/turn -H "Content-Type: application/json" -d '{"message":"hello"}'
curl -X POST http://127.0.0.1:8788/turn -H "Content-Type: application/json" -d '{"message":"remember: synthetic project flag"}'
curl -X POST http://127.0.0.1:8788/turn -H "Content-Type: application/json" -d '{"message":"recall"}'
```

Use `Ctrl+C` to stop the server. The server binds only to `127.0.0.1`. The memory exists in RAM only and resets when the process exits. No authentication, encryption, persistence, model calls, or external APIs are present. Do not enter private, medical, customer, or company information.

The mock's purpose is to demonstrate **control flow**, HTTP validation and predictable behavior before connecting a real model. A real business integration would require explicit data governance, authorization, logging and security decisions, model evaluations, monitoring and human approval.
