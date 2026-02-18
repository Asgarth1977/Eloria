/*
    Main app.js file.
*/

// app.js

document.addEventListener("DOMContentLoaded", () => {
    const attachBtn = document.getElementById("attach-btn");
    const fileInput = document.getElementById("attach-input");

    if (!attachBtn || !fileInput) {
        console.error("Attach button or file input missing!");
        return;
    }

    // When + button is clicked, open the hidden file input
    attachBtn.onclick = () => {
        fileInput.click();
    };

    // Handle file selection
    fileInput.onchange = async (e) => {
        if (!e.target.files.length) return;

        const file = e.target.files[0];

        try {
            const text = await file.text();
            const data = JSON.parse(text);

            if (!Array.isArray(data)) {
                alert("Invalid memory file format.");
                return;
            }

            // Send to backend for injection
            const res = await fetch("/inject_memory", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ memory: data })
            });

            const result = await res.json();
            alert(result.status);

            // Clear input value so the same file can be selected again
            fileInput.value = "";
        } catch (err) {
            console.error(err);
            alert("Failed to read or parse file.");
        }
    };
});

document.addEventListener("DOMContentLoaded", function () {

    const menuToggle = document.getElementById("menuToggle");
    const drawer = document.getElementById("sideDrawer");
    const overlay = document.getElementById("overlay");

    const btnSettings = document.getElementById("btnSettings");
    const btnHistory = document.getElementById("btnHistory");
    const btnPrompts = document.getElementById("btnPrompts");
    const btnMemory = document.getElementById("btnMemory");

    const drawerButtons = document.querySelectorAll(".drawer-btn");

    // Open drawer
    menuToggle.addEventListener("click", function () {
        drawer.classList.add("active");
        overlay.classList.add("active");
        document.body.classList.add("drawer-open");
    });

    // Close drawer when clicking overlay
    overlay.addEventListener("click", function () {
        drawer.classList.remove("active");
        overlay.classList.remove("active");
        document.body.classList.remove("drawer-open");
    });

    // Button actions
    btnSettings.addEventListener("click", function () {
        console.log("Settings clicked");
    });

    btnHistory.addEventListener("click", function () {
        console.log("History clicked");
    });

    btnPrompts.addEventListener("click", function () {
        console.log("Prompts clicked");
    });

    btnMemory.addEventListener("click", function () {
        console.log("Memory clicked");
    });
    drawerButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            const panel = document.getElementById(btn.dataset.target);
            const isOpen = btn.classList.contains("active");

            drawerButtons.forEach(b => {
                b.classList.remove("active");
                const p = document.getElementById(b.dataset.target);
                p.style.display = "none";
            });

            if (!isOpen) {
                btn.classList.add("active");
                panel.style.display = "block";
            }
        });
    });

    // --- Dark Mode Toggle ---
    const darkModeToggle = document.getElementById("darkModeToggle");

    if (darkModeToggle) {
        if (localStorage.getItem("eloriaDarkMode") === "true") {
            document.body.classList.add("dark-mode");
            darkModeToggle.checked = true;
        }

        darkModeToggle.addEventListener("change", () => {
            document.body.classList.toggle("dark-mode");
            localStorage.setItem("eloriaDarkMode", document.body.classList.contains("dark-mode"));
        });
    }
});

// ----------------------------
// Splash / Matrix Setup
// ----------------------------
document.addEventListener("DOMContentLoaded", () => {
    const splash = document.getElementById("startupSplash");
    const appDiv = document.getElementById("app");
    const canvas = document.getElementById("splashCanvas");
    const ctx = canvas.getContext("2d");

    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    const columnWidth = 22; 
    const letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%^&*()ｱｲｳｴｵｶｷｸｹｺﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜﾝｦｧｨｩｪｫｯｬｭｮ日";
    const columns = Math.floor(canvas.width / columnWidth);
    const drops = Array(columns).fill(0);
    const speeds = drops.map(() => Math.random() * 0.2 + 0.05); // slight variance
    let matrixAnimationId;

    const progressBar = document.getElementById("loadingProgress");
    const startupText = document.getElementById("startupText");
    const text = letters.charAt(Math.floor(Math.random() * letters.length));

    const timers = Array(columns).fill(0);
    const chars = Array(columns).fill(text);
    const changeRate = 25 + Math.floor(Math.random() * 10); // frames before character changes

    let progress = 0;
    let finished = false;

    // ----------------------------
    // Matrix draw
    // ----------------------------
    function drawMatrix() {
        ctx.fillStyle = "rgba(0,0,0,0.3)"; // trails
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.font = "20px monospace";

        for (let i = 0; i < drops.length; i++) {
            timers[i]++;
            if (timers[i] >= changeRate) {
                chars[i] = letters.charAt(Math.floor(Math.random() * letters.length));
                timers[i] = 0;
            }

            ctx.fillStyle = Math.random() > 0.975 ? "#AAF" : "#0F0";
            ctx.fillText(chars[i], i * columnWidth, drops[i] * columnWidth);

            if (drops[i] * columnWidth > canvas.height && Math.random() > 0.975) {
                drops[i] = 0;
            }

            drops[i] += speeds[i];
        }

        matrixAnimationId = requestAnimationFrame(drawMatrix);
    }
    drawMatrix();

    // ----------------------------
    // Progress bar simulation
    // ----------------------------
    function updateProgress() {
        if (finished) return;

        progress += 0.1; // slow cinematic fill
        if (progress >= 99.5) {
            progress = 100;
            finished = true;
            progressBar.style.width = "100%";
            startupText.textContent = "System Online";

            setTimeout(appReady, 1600);
            return;
        }

        progressBar.style.width = progress + "%";

        if (progress > 25 && progress < 55) startupText.textContent = "Decrypting memory...";
        else if (progress >= 55 && progress < 85) startupText.textContent = "Booting neural core...";
        else if (progress >= 85) startupText.textContent = "Establishing consciousness...";

        requestAnimationFrame(updateProgress);
    }
    updateProgress();

    // ----------------------------
    // App ready
    // ----------------------------
    function appReady() {
        if (matrixAnimationId) cancelAnimationFrame(matrixAnimationId);
        if (canvas) canvas.remove();
        splash.style.display = "none";
        appDiv.style.display = "block";
    }

    window.addEventListener("resize", () => {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    });
});
