const form = document.getElementById("turn");
const message = document.getElementById("message");
const send = document.getElementById("send");
const feedback = document.getElementById("feedback");

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  if (send.disabled) return;
  if (!message.value.trim()) {
    feedback.textContent = "Enter a synthetic message.";
    message.focus();
    return;
  }

  send.disabled = true;
  feedback.textContent = "Sending…";
  try {
    const response = await fetch("/turn", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: message.value }),
    });
    if (!response.ok) {
      feedback.textContent = response.status === 400
        ? "Invalid input. Use 1–500 characters, or 1–100 for a note."
        : "The local server could not complete this turn.";
      return;
    }
    const turn = await response.json();
    document.getElementById("action").textContent = turn.action;
    document.getElementById("state").textContent = turn.state;
    document.getElementById("memory").textContent = String(turn.memory_items);
    document.getElementById("reply").textContent = turn.text ?? "No reply (silence).";
    feedback.textContent = "";
  } catch {
    feedback.textContent = "Could not read a response. Check the local server and try again.";
  } finally {
    send.disabled = false;
  }
});
