const webSocket = new WebSocket("ws://127.0.0.1:8000/hoge");
const text_message = document.querySelector("#textMessage");
const send_button = document.querySelector("#sendMessage");

webSocket.onopen = () => {
    messageTextArea.value += "Server connect...\n";
};

webSocket.onmessage = (message) => {
    messageTextArea.value += "Recieve From Server => " + message.data + "\n";
};

send_button.addEventListener("click", () => {
    sendMessage(text_message.value);
});

function sendMessage(message) {
    messageTextArea.value += "Send to Server => " + message + "\n";
    webSocket.send(message);
    text_message.value = "";
}
