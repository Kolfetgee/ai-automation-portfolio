const assert = require("node:assert/strict");
const { readFileSync } = require("node:fs");
const path = require("node:path");
const test = require("node:test");
const vm = require("node:vm");

const script = readFileSync(path.join(__dirname, "../demos/mai/web/console.js"), "utf8");

// Exercise the same submit listener as the browser, with an isolated form per test.
function consoleForm(fetch) {
  const elements = {};
  for (const id of ["message", "send", "feedback", "action", "state", "memory", "reply"]) {
    elements[id] = { textContent: "" };
  }
  let submitListener;
  elements.turn = {
    addEventListener(name, listener) {
      assert.equal(name, "submit");
      submitListener = listener;
    },
  };
  const document = { getElementById: (id) => elements[id] };
  vm.runInNewContext(script, { document, fetch });
  return {
    elements,
    submit(message) {
      elements.message.value = message;
      return submitListener({ preventDefault() {} });
    },
  };
}

test("posts JSON and renders reply, escalation and silence from the server", async () => {
  const cases = [
    ["recall", "reply", "READY", "<sample>", 2],
    ["unknown", "escalate", "READY", "Human review required.", 2],
    ["stop", "silence", "STOP", null, 2],
  ];
  for (const [message, action, state, text, memory_items] of cases) {
    const form = consoleForm(async (url, request) => {
      assert.equal(url, "/turn");
      assert.equal(request.method, "POST");
      assert.equal(request.headers["Content-Type"], "application/json");
      assert.deepEqual(JSON.parse(request.body), { message });
      return { ok: true, json: async () => ({ action, state, text, memory_items }) };
    });
    await form.submit(message);
    const view = form.elements;
    assert.equal(view.action.textContent, action);
    assert.equal(view.state.textContent, state);
    assert.equal(view.memory.textContent, "2");
    assert.equal(view.reply.textContent, text ?? "No reply (silence).");
  }
});

test("rejects blank input and retains the last result on request failures", async () => {
  let calls = 0;
  const form = consoleForm(async () => {
    if (++calls === 1) return { ok: false, status: 400 };
    throw new Error("offline");
  });
  const view = form.elements;
  view.message.focus = () => {};
  view.reply.textContent = "Previous reply.";
  await form.submit(" ");
  assert.equal(calls, 0);
  assert.match(view.feedback.textContent, /Enter a synthetic message/);
  await form.submit("remember:");
  assert.match(view.feedback.textContent, /Invalid input/);
  await form.submit("hello");
  assert.match(view.feedback.textContent, /Check the local server/);
  assert.equal(view.reply.textContent, "Previous reply.");
  assert.equal(view.send.disabled, false);
});
