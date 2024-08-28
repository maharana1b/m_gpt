document.addEventListener('DOMContentLoaded', function () {
    const chatForm = document.getElementById('chat-form');
    const chatWindow = document.getElementById('chat-window');
    const chatInput = document.getElementById('chat-input');

    chatForm.addEventListener('submit', function (e) {
        e.preventDefault();
        const userMessage = chatInput.value.trim();

        if (userMessage) {
            addMessage('user-message', userMessage);
            chatInput.value = '';

            // Example bot response
            setTimeout(() => {
                addMessage('bot-message', 'I am a chatbot. How can I assist you today?');
            }, 1000);
        }
    });

    function addMessage(className, text) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `chat-message ${className}`;
        messageDiv.textContent = text;
        chatWindow.appendChild(messageDiv);
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }
});
