// Simple 10-minute countdown for Round 1.
// Auto-submits the form when time is over.

(function () {
  const display = document.getElementById("timer-display");
  const form = document.getElementById("round1-form");
  if (!display || !form || typeof durationSeconds === "undefined") {
    return;
  }

  let remaining = durationSeconds;

  function update() {
    const minutes = Math.floor(remaining / 60);
    const seconds = remaining % 60;
    display.textContent =
      String(minutes).padStart(2, "0") +
      ":" +
      String(seconds).padStart(2, "0");
  }

  update();

  const timerId = setInterval(() => {
    remaining -= 1;
    if (remaining <= 0) {
      clearInterval(timerId);
      display.textContent = "00:00 (Auto-submitting...)";
      form.submit();
      return;
    }
    update();
  }, 1000);
})();

