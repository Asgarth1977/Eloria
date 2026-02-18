// Dark Mode toggle
document.addEventListener("DOMContentLoaded", () => {
    const darkToggle = document.getElementById("darkModeToggle");

    // Load saved preference
    if(localStorage.getItem("darkMode") === "enabled") {
        document.body.classList.add("dark-mode");
        darkToggle.checked = true;
    }

    // Listen for changes
    darkToggle.addEventListener("change", () => {
        if(darkToggle.checked){
            document.body.classList.add("dark-mode");
            localStorage.setItem("darkMode", "enabled");
        } else {
            document.body.classList.remove("dark-mode");
            localStorage.setItem("darkMode", "disabled");
        }
    });
});
