document.addEventListener("DOMContentLoaded", () => {
    const sidebar = document.getElementById("sideDrawer");
    const toggleBtn = document.querySelector(".topbar .menu-toggle");

    // Hamburger toggle
    if (toggleBtn) {
        toggleBtn.addEventListener("click", (e) => {
            e.stopPropagation(); // prevent document click
            sidebar.classList.toggle("open");
        });
    }

    // Add × button inside sidebar if missing
    let collapseBtn = sidebar.querySelector(".sidebar-collapse-btn");
    if (!collapseBtn) {
        collapseBtn = document.createElement("button");
        collapseBtn.className = "sidebar-collapse-btn";
        collapseBtn.textContent = "×";
        sidebar.prepend(collapseBtn);
    }

    collapseBtn.addEventListener("click", (e) => {
        e.stopPropagation();
        sidebar.classList.remove("open");
    });

    // Click outside sidebar to close
    document.addEventListener("click", (e) => {
        if (!sidebar.contains(e.target) && !toggleBtn.contains(e.target)) {
            sidebar.classList.remove("open");
        }
    });

    // Stop clicks inside sidebar from bubbling up
    sidebar.addEventListener("click", (e) => e.stopPropagation());

    // Accordion panels
    const panels = document.querySelectorAll(".menu-panel");
    document.querySelectorAll(".sidebar-btn").forEach(btn => {
        btn.addEventListener("click", () => {
            const panelId = btn.id.replace("menu-", "panel-");
            const panel = document.getElementById(panelId);

            panels.forEach(p => {
                if (p !== panel) p.classList.remove("open");
            });

            if (panel) panel.classList.toggle("open");
        });
    });

    // DARK MODE TOGGLE
    const darkToggle = document.getElementById("darkModeToggle");
    if (darkToggle) {
        const savedMode = localStorage.getItem("darkMode");
        if (savedMode === "enabled") {
            document.body.classList.add("dark-mode");
            darkToggle.checked = true;
        } else {
            document.body.classList.remove("dark-mode");
            darkToggle.checked = false;
        }

        darkToggle.addEventListener("change", () => {
            if (darkToggle.checked) {
                document.body.classList.add("dark-mode");
                localStorage.setItem("darkMode", "enabled");
            } else {
                document.body.classList.remove("dark-mode");
                localStorage.setItem("darkMode", "disabled");
            }
        });
    }
});