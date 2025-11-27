document.addEventListener("DOMContentLoaded", function () {
    const btn = document.getElementById("themeToggle");
    if (!btn) return;

    // Load saved theme from localStorage
    if (localStorage.getItem("theme") === "dark") {
        document.body.classList.add("dark-mode");
        btn.textContent = "☀️ Light Mode";
    } else {
        btn.textContent = "🌙 Dark Mode";
    }

    // Toggle theme on button click
    btn.addEventListener("click", function () {
        document.body.classList.toggle("dark-mode");

        if (document.body.classList.contains("dark-mode")) {
            btn.textContent = "☀️ Light Mode";
            localStorage.setItem("theme", "dark");
        } else {
            btn.textContent = "🌙 Dark Mode";
            localStorage.setItem("theme", "light");
        }
    });
});
