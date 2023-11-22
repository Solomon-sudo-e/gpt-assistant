function sendMessage() {
    var userInput = document.getElementById('user-input').value;

    // Append user's message to the chat display
    appendMessage('User', userInput);

    // Assume you have a backend API endpoint (replace with your actual endpoint)
    var backendEndpoint = 'http://127.0.0.1:5000';

    // Assume you are using fetch API to communicate with the backend
    fetch(backendEndpoint, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: userInput }),
    })
    .then(response => response.json())
    .then(data => {
        // Append the backend's response to the chat display
        appendMessage('Chatbot', data.response);
    })
    .catch(error => {
        console.error('Error:', error);
        appendMessage('Chatbot', 'Sorry, an error occurred.');
    });

    // Clear the user input field
    document.getElementById('user-input').value = '';
}

function appendMessage(sender, message) {
    var chatDisplay = document.getElementById('chat-display');
    var newMessage = document.createElement('div');
    newMessage.innerHTML = `<strong>${sender}:</strong> ${message}`;
    chatDisplay.appendChild(newMessage);

    // Scroll to the bottom of the chat display to show the latest message
    chatDisplay.scrollTop = chatDisplay.scrollHeight;
}
