document.addEventListener("DOMContentLoaded", () => {
    const menuToggle = document.getElementById("menuToggle");
    const sideDrawer = document.getElementById("sideDrawer");
    const overlay = document.getElementById("overlay");

    // Toggle drawer open/close
    menuToggle.addEventListener("click", () => {
        sideDrawer.classList.toggle("open");
        overlay.classList.toggle("show");
    });

    // Click overlay to close drawer and panels
    overlay.addEventListener("click", () => {
        sideDrawer.classList.remove("open");
        overlay.classList.remove("show");
        closeAllPanels();
    });

    // Accordion buttons and panels
    const menuMapping = {
        "menu-settings": "panel-settings",
        "menu-history": "panel-history",
        "menu-prompts": "panel-prompts",
        "menu-memory": "panel-memory",
        "menu-debug": "panel-debug"
    };

    Object.keys(menuMapping).forEach(btnId => {
        const button = document.getElementById(btnId);
        const panel = document.getElementById(menuMapping[btnId]);

        if (button && panel) {
            button.addEventListener("click", () => {
                // Toggle current panel
                const isOpen = panel.style.maxHeight && panel.style.maxHeight !== "0px";

                // Close all other panels
                closeAllPanels();

                if (!isOpen) {
                    panel.style.maxHeight = panel.scrollHeight + "px"; // open panel
                }
            });
        }
    });

    function closeAllPanels() {
        document.querySelectorAll(".menu-panel").forEach(p => {
            p.style.maxHeight = "0px";
        });
    }

    // DARK MODE TOGGLE
    const darkToggle = document.getElementById("darkModeToggle");
    if (darkToggle) {
        if (localStorage.getItem("darkMode") === "enabled") {
            document.body.classList.add("dark-mode");
            darkToggle.checked = true;
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
