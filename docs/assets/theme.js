// Apply a saved preference before painting; unavailable storage falls back to the device.
(() => {
  try {
    const theme = localStorage.getItem('ml-ai-it-theme');
    if (theme === 'light' || theme === 'dark') document.documentElement.dataset.theme = theme;
  } catch { /* Device preference remains available without storage. */ }
})();
