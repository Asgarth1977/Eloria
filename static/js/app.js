document.addEventListener('DOMContentLoaded', () => {
    const chat = document.getElementById('chat');
    const input = document.getElementById('userInput');
    const sendButton = document.querySelector('.send-btn');

    // --- Load previous conversation if Flask passes it ---
    const conversation = window.conversation || [];  // optionally pass via template
    for (const msg of conversation) {
        const sender = msg.role === 'user' ? 'user' : 'ai';
        appendMessage(msg.content, sender, msg.timestamp);
    }

    // --- Send button ---
    sendButton.addEventListener('click', sendMessage);
    input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    // --- Helper: timestamp formatting ---
    function formatTimestamp(ts) {
        const dt = new Date(ts);
        return dt.toLocaleString(undefined, {
            year: "numeric",
            month: "short",
            day: "2-digit",
            hour: "2-digit",
            minute: "2-digit"
        });
    }

    // --- Append message to chat ---
    function appendMessage(text, sender, timestamp = new Date().toISOString()) {
        const div = document.createElement('div');
        div.classList.add('message', sender + '-message');

        const bubble = document.createElement('div');
        bubble.classList.add(sender + '-bubble');
        bubble.textContent = text;

        const tsDiv = document.createElement('div');
        tsDiv.className = 'timestamp';
        tsDiv.textContent = formatTimestamp(timestamp);

        bubble.appendChild(tsDiv);
        div.appendChild(bubble);
        chat.appendChild(div);
        chat.scrollTop = chat.scrollHeight;
    }

    // --- Send message to backend ---
    async function sendMessage() {
        const text = input.value.trim();
        if (!text) return;

        appendMessage(text, 'user');  // display immediately
        input.value = '';

        /*
        // For now: mock AI response (remove later when memory manager integrated)
        setTimeout(() => {
            appendMessage("AI response placeholder", 'ai');
        }, 500);

        // Later: send to Flask
        */
        try {
            const res = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text })
            });
            const data = await res.json();
            appendMessage(data.response, 'ai');
        } catch (err) {
            appendMessage("Error: Could not reach server.", 'ai');
            console.error(err);
        }
    }
});