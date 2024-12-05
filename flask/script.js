// Function to scroll movie list left
function scrollLeft(containerId) {
    const container = document.getElementById(containerId);
    container.scrollBy({ left: -300, behavior: 'smooth' });
}

// Function to scroll movie list right
function scrollRight(containerId) {
    const container = document.getElementById(containerId);
    container.scrollBy({ left: 300, behavior: 'smooth' });
}

// Open the chat menu
function openChatMenu() {
    document.getElementById("chatMenu").style.display = "block";
}

// Close the chat menu
function closeChatMenu() {
    document.getElementById("chatMenu").style.display = "none";
}

// Example function for sending a message (you can expand this as needed)
function sendMessage() {
    const chatInput = document.querySelector(".chat-input input[type='text']");
    const message = chatInput.value;
    if (message.trim() !== "") {
        const chatHistory = document.querySelector(".chat-history");
        const messageElement = document.createElement("p");
        messageElement.textContent = `You: ${message}`;
        chatHistory.appendChild(messageElement);
        chatInput.value = ""; // Clear input
        chatHistory.scrollTop = chatHistory.scrollHeight; // Scroll to bottom
    }
}
