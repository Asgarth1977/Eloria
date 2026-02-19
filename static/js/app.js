function formatTimestamp(ts) {
    const dt = new Date(ts);
    if (Number.isNaN(dt.getTime())) return "";
    return dt.toLocaleString(undefined, {
        year: "numeric",
        month: "short",
        day: "2-digit",
        hour: "2-digit",
        minute: "2-digit"
    });
}

function addMessage(text, sender, timestamp) {
    const chat = document.getElementById("chat");
    const div = document.createElement("div");
    div.className = `bubble ${sender}`;
    div.textContent = text;

    const ts = document.createElement("div");
    ts.className = "timestamp";
    ts.textContent = formatTimestamp(timestamp);

    div.appendChild(ts);
    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
}

window.addMessage = addMessage;

document.addEventListener("DOMContentLoaded", () => {
    const chat = document.getElementById("chat");
    const input = document.getElementById("input");
    const sendBtn = document.getElementById("send");
    const menuToggle = document.getElementById("menuToggle");
    const drawer = document.getElementById("sideDrawer");
    const darkModeToggle = document.getElementById("darkModeToggle");
    const attachBtn = document.getElementById("attach-btn");
    const attachInput = document.getElementById("attach-input");
    const newChatBtn = document.getElementById("newChatBtn");

    function loadConversation() {
        const node = document.getElementById("conversationData");
        if (!node?.textContent) return;
        const conversation = JSON.parse(node.textContent);
        for (const msg of conversation) {
            addMessage(msg.content, msg.role === "user" ? "user" : "ai", msg.timestamp);
        }
    }

    async function sendMessage() {
        const text = input.innerText.trim();
        if (!text) return;

        const now = new Date().toISOString();
        addMessage(text, "user", now);
        input.innerHTML = "";

        const res = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text })
        });

        const data = await res.json();
        addMessage(data.response, "ai", new Date().toISOString());
    }

    sendBtn.addEventListener("click", sendMessage);
    input.addEventListener("keydown", (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    menuToggle.addEventListener("click", () => drawer.classList.toggle("open"));

    document.querySelectorAll(".sidebar-btn").forEach((btn) => {
        btn.addEventListener("click", () => {
            const section = btn.id.replace("menu-", "panel-");
            document.querySelectorAll(".menu-panel").forEach((panel) => {
                if (panel.id === section) panel.classList.toggle("open");
                else panel.classList.remove("open");
            });
        });
    });

    const savedMode = localStorage.getItem("eloriaTheme") || "dark";
    if (savedMode === "light") {
        document.body.classList.add("light-mode");
        darkModeToggle.checked = false;
    }
    darkModeToggle.addEventListener("change", () => {
        const isDark = darkModeToggle.checked;
        document.body.classList.toggle("light-mode", !isDark);
        localStorage.setItem("eloriaTheme", isDark ? "dark" : "light");
    });

    attachBtn.addEventListener("click", () => attachInput.click());
    attachInput.addEventListener("change", async (e) => {
        if (!e.target.files?.length) return;
        const file = e.target.files[0];
        const text = await file.text();
        const payload = JSON.parse(text);
        if (!Array.isArray(payload)) {
            alert("Invalid memory JSON. Expected array of messages.");
            return;
        }

        const res = await fetch("/inject_memory", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ memory: payload })
        });
        const data = await res.json();
        alert(data.status || data.error || "Done");
        attachInput.value = "";
    });

    newChatBtn.addEventListener("click", () => {
        chat.innerHTML = "";
    });

    loadConversation();
    runStartupSplash();
});

function runStartupSplash() {
    const splash = document.getElementById("startupSplash");
    const appDiv = document.getElementById("app");
    const canvas = document.getElementById("splashCanvas");
    const ctx = canvas.getContext("2d");

    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    const columnWidth = 22;
    const letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%^&*()";
    const columns = Math.floor(canvas.width / columnWidth);
    const drops = Array(columns).fill(0);
    const speeds = drops.map(() => Math.random() * 0.2 + 0.05);
    const progressBar = document.getElementById("loadingProgress");
    const startupText = document.getElementById("startupText");

    let progress = 0;
    let anim;

    function drawMatrix() {
        ctx.fillStyle = "rgba(0,0,0,0.25)";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.font = "20px monospace";

        for (let i = 0; i < drops.length; i++) {
            ctx.fillStyle = "#0F0";
            const text = letters.charAt(Math.floor(Math.random() * letters.length));
            ctx.fillText(text, i * columnWidth, drops[i] * columnWidth);
            if (drops[i] * columnWidth > canvas.height && Math.random() > 0.975) drops[i] = 0;
            drops[i] += speeds[i];
        }

        anim = requestAnimationFrame(drawMatrix);
    }

    function updateProgress() {
        progress += 0.7;
        progressBar.style.width = `${Math.min(progress, 100)}%`;
        if (progress < 35) startupText.textContent = "Decrypting memory...";
        else if (progress < 70) startupText.textContent = "Booting neural core...";
        else startupText.textContent = "Establishing consciousness...";

        if (progress >= 100) {
            startupText.textContent = "System Online";
            setTimeout(() => {
                cancelAnimationFrame(anim);
                splash.style.display = "none";
                appDiv.style.display = "flex";
            }, 400);
            return;
        }
        requestAnimationFrame(updateProgress);
    }

    drawMatrix();
    updateProgress();
}
