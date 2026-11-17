'use strict';
// Progressive enhancement. All installation text is usable without JavaScript.
for (const button of document.querySelectorAll('[data-copy]')) {
  button.hidden = false;
  const label = button.textContent;
  button.addEventListener('click', async () => {
    const code = document.getElementById(button.dataset.copy);
    const status = document.getElementById('copy-status');
    if (!code || !status) return;
    try {
      await navigator.clipboard.writeText(code.textContent);
      button.textContent = button.dataset.done;
      status.textContent = button.dataset.done;
    } catch {
      const range = document.createRange();
      range.selectNodeContents(code);
      const selection = window.getSelection();
      selection.removeAllRanges();
      selection.addRange(range);
      status.textContent = button.dataset.fail;
    }
    window.setTimeout(() => { button.textContent = label; }, 1800);
  });
}
