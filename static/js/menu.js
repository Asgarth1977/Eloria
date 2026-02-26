// menu.js
document.addEventListener("DOMContentLoaded", () => {
    const sidebar = document.getElementById("sidebar");
    const toggleBtn = document.getElementById("sidebarToggle");
    const logo = document.querySelector("#sidebar .logo");

    if (!sidebar) return;

    function toggleSidebar(){
        sidebar.classList.toggle("collapsed");
    }

    if (toggleBtn){
        toggleBtn.addEventListener("click", toggleSidebar);
    }

    if (logo){
        logo.addEventListener("click", toggleSidebar);
    }

    // Stop clicks inside sidebar from closing
    sidebar.addEventListener("click", (e) => e.stopPropagation());

    // History button placeholder: attach fetch to 3-day messages
    const historyBtn = document.getElementById("btn-history");
    if (historyBtn) {
        historyBtn.addEventListener("click", async () => {
            try {
                const res = await fetch("/load_3_days", { method: "POST" });
                const data = await res.json();
                if (data.success) {
                    console.log("3-day history:", data.messages);
                    // TODO: display in chat
                } else console.error(data.error);
            } catch (err) { console.error(err); }
        });
    }
});