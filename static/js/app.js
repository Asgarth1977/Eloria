// app.js
document.addEventListener('DOMContentLoaded', () => {
    const sidebar = document.getElementById('sidebar');
    const toggle = document.getElementById('sidebarToggle');
    const mainContainer = document.querySelector('.main-container');
    const sendButton = document.getElementById('sendButton');
    const userInput = document.getElementById('userInput');
    const messageArea = document.getElementById('messageArea');
    const logo = document.getElementById('sidebarLogo');

    toggle.addEventListener('click', () => {
        sidebar.classList.toggle('open');
        mainContainer.classList.toggle('shifted');
    });
        // Both the button and the logo can toggle
    toggle.addEventListener('click', toggleSidebar);
    logo.addEventListener('click', toggleSidebar);    
    function toggleSidebar() {
        sidebar.classList.toggle('collapsed');
    }
    

    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            sendMessage();
        }
    });

    function sendMessage() {
        const text = userInput.value.trim();
        if (!text) return;
        appendMessage(text, 'user');
        userInput.value = '';

        setTimeout(() => {
            appendMessage('AI Response', 'ai');
        }, 1000);
    }

    function appendMessage(text, type) {
        const div = document.createElement('div');
        div.classList.add('message', `${type}-message`);
        const bubble = document.createElement('div');
        bubble.classList.add(`${type}-bubble`);
        bubble.textContent = text;
        div.appendChild(bubble);
        messageArea.appendChild(div);
        messageArea.scrollTop = messageArea.scrollHeight;
    }
});