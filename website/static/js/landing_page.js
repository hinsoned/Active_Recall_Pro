// static/js/landing.js

// Theme toggle functionality
function initializeThemeToggle() {
    const themeToggles = document.querySelectorAll(".themeToggle");

    // Load saved theme on page load
    document.addEventListener("DOMContentLoaded", () => {
        const savedTheme = localStorage.getItem("theme") || "light";
        document.body.setAttribute("data-bs-theme", savedTheme);
        themeToggles.forEach(toggle => {
            toggle.checked = savedTheme === "dark";
        });
    });

    // Handle theme toggle changes
    themeToggles.forEach(toggle => {
        toggle.addEventListener("change", () => {
            const newTheme = toggle.checked ? "dark" : "light";
            document.body.setAttribute("data-bs-theme", newTheme);
            localStorage.setItem("theme", newTheme);
            themeToggles.forEach(t => t.checked = toggle.checked); // Sync all toggles
        });
    });
}

// Initialize the page
document.addEventListener("DOMContentLoaded", () => {
    initializeThemeToggle();
});