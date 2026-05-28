(function () {
  const keyElement = document.querySelector("#api-key");
  const copyButton = document.querySelector("#copy-key");
  const copyMessage = document.querySelector("#copy-message");
  const usedCallsInput = document.querySelector("#used-calls");
  const quotaInput = document.querySelector("#quota");
  const quotaOutput = document.querySelector("#quota-output");

  function updateQuota() {
    if (!usedCallsInput || !quotaInput || !quotaOutput) return;

    const usedCalls = Number(usedCallsInput.value);
    const quota = Number(quotaInput.value);
    const percentage = quota > 0 ? Math.min((usedCalls / quota) * 100, 999) : 0;

    quotaOutput.value = `${percentage.toFixed(1)}% quota used`;
    quotaOutput.textContent = quotaOutput.value;
  }

  async function copyApiKey() {
    if (!keyElement || !copyMessage) return;

    const key = keyElement.textContent.trim();

    try {
      if (navigator.clipboard) {
        await navigator.clipboard.writeText(key);
      }
      copyMessage.textContent = "API key copied.";
    } catch (_error) {
      copyMessage.textContent = key;
    }
  }

  copyButton?.addEventListener("click", copyApiKey);
  usedCallsInput?.addEventListener("input", updateQuota);
  quotaInput?.addEventListener("input", updateQuota);
  updateQuota();
})();
