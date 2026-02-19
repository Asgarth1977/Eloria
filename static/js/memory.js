// memory.js
document.addEventListener("DOMContentLoaded", () => {
    const loadBtn = document.getElementById("load3Days");
    const summarizeBtn = document.getElementById("summarizeNow");

    if (loadBtn) {
        loadBtn.addEventListener("click", async () => {
            try {
                const res = await fetch("/load_3_days", { method: "POST" });
                const data = await res.json();
                console.log(data);

                if (data.success && Array.isArray(data.messages) && data.messages.length) {
                    for (const msg of data.messages) {
                        addMessage(msg.content, msg.role === "user" ? "user" : "ai", msg.timestamp);
                    }
                } else if (!data.success) {
                    alert("Error loading 3-day memory: " + data.error);
                } else {
                    alert("No messages found for the 3 days before yesterday.");
                }
            } catch (err) {
                console.error(err);
                alert("Failed to fetch 3-day memory.");
            }
        });
    }

    if (summarizeBtn) {
        summarizeBtn.addEventListener("click", async () => {
            try {
                const res = await fetch("/summarize_now", { method: "POST" });
                const data = await res.json();
                if (data.success) alert("Summary saved:\n" + data.summary);
                else alert("Error summarizing: " + data.error);
            } catch (err) {
                console.error(err);
                alert("Failed to summarize.");
            }
        });
    }
});
