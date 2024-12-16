const socket = io.connect();

// DOM elements
const chatBox = document.getElementById('chat-box');
const messageInput = document.getElementById('message-input');
const sendButton = document.getElementById('send-button');
const voiceButton = document.getElementById('voice-button');

// Add a new message to the chat box
function addMessageToChat(user, content, timestamp, avatar) {
    const message = document.createElement('div');
    message.classList.add('message');

    const avatarElement = document.createElement('div');
    avatarElement.classList.add('avatar');
    avatarElement.style.backgroundImage = `url(/static/images/${avatar})`;

    const contentElement = document.createElement('div');
    contentElement.classList.add('content');
    contentElement.classList.add(user === 'Model' ? 'model' : 'user');
    contentElement.innerHTML = `<p>${content}</p>`;

    const timestampElement = document.createElement('div');
    timestampElement.classList.add('timestamp');
    timestampElement.innerText = timestamp;

    message.appendChild(avatarElement);
    message.appendChild(contentElement);
    message.appendChild(timestampElement);
    chatBox.appendChild(message);
    chatBox.scrollTop = chatBox.scrollHeight; // Scroll to the bottom
}

// Fetch initial chat history
fetch('/display')
    .then((response) => response.json())
    .then((data) => {
        data.chat_history.forEach((msg) => {
            addMessageToChat(msg.user, msg.content, msg.time, msg.avatar);
        });
    });

// Listen for new messages via Socket.IO
socket.on('new_message', (msg) => {
    addMessageToChat(msg.user, msg.content, msg.time, msg.avatar);
});

// Send a new message
sendButton.addEventListener('click', () => {
    const content = messageInput.value.trim();
    if (content) {
        fetch('/input', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user: 'User 1', content }),
        });
        messageInput.value = '';
    }
});

// Start voice input
voiceButton.addEventListener('click', () => {
    fetch('/input', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user: 'User 1', voice: 'start' }),
    });
});
