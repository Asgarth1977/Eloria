// menu.js
document.addEventListener("DOMContentLoaded", () => {
    const sidebar = document.getElementById("sideDrawer");
    const toggleBtn = document.querySelector(".topbar .menu-toggle");

    // Hamburger toggle
    toggleBtn.addEventListener("click", e => {
        e.stopPropagation();
        sidebar.classList.toggle("open");
    });

    // × button
    const collapseBtn = sidebar.querySelector(".sidebar-collapse-btn");
    collapseBtn.addEventListener("click", e => {
        e.stopPropagation();
        sidebar.classList.remove("open");
    });

    // Click outside
    document.addEventListener("click", e => {
        if (!sidebar.contains(e.target) && !toggleBtn.contains(e.target)) {
            sidebar.classList.remove("open");
        }
    });
    sidebar.addEventListener("click", e => e.stopPropagation());

    // Accordion panels
    const panels = document.querySelectorAll(".menu-panel");
    document.querySelectorAll(".sidebar-btn").forEach(btn => {
        btn.addEventListener("click", () => {
            const panelId = btn.id.replace("menu-", "panel-");
            const panel = document.getElementById(panelId);
            panels.forEach(p => { if (p !== panel) p.classList.remove("open"); });
            if (panel) panel.classList.toggle("open");
        });
    });

    // Dark mode toggle
    const darkToggle = document.getElementById("darkModeToggle");
    const saved = localStorage.getItem("darkMode");
    if (saved === "enabled") { document.body.classList.add("dark-mode"); darkToggle.checked = true; }
    else { document.body.classList.remove("dark-mode"); darkToggle.checked = false; }

    darkToggle.addEventListener("change", () => {
        if (darkToggle.checked) { document.body.classList.add("dark-mode"); localStorage.setItem("darkMode","enabled"); }
        else { document.body.classList.remove("dark-mode"); localStorage.setItem("darkMode","disabled"); }
    });
});