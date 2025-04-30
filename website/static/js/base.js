// static/js/base.js
document.addEventListener("DOMContentLoaded", () => {
    // --- Theme Toggle Logic ---
    const themeToggles = document.querySelectorAll(".themeToggle");
  
    // Load user's theme preference on page load
    const savedTheme = localStorage.getItem("theme") || "light";
    document.documentElement.setAttribute("data-bs-theme", savedTheme);
    themeToggles.forEach((themeToggle) => {
      themeToggle.checked = savedTheme === "dark";
    });
  
    // Listen for theme toggle changes
    themeToggles.forEach((themeToggle) => {
      themeToggle.addEventListener("change", () => {
        const newTheme = themeToggle.checked ? "dark" : "light";
        document.documentElement.setAttribute("data-bs-theme", newTheme);
        localStorage.setItem("theme", newTheme);
        // Sync all toggles
        themeToggles.forEach((toggle) => {
          toggle.checked = themeToggle.checked;
        });
      });
    });
  
    // --- Auto-Dismiss Alerts Logic ---
    /*
    const alerts = document.querySelectorAll(".alert");
    alerts.forEach((alert) => {
      setTimeout(() => {
        const alertInstance = new bootstrap.Alert(alert);
        alertInstance.close();
      }, 5000);
    });
    */
  });