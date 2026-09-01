const CHATBOT_RESPONSES = {
    'hello': 'Hello! How can I help you today?',
    'hi': 'Hi there! Welcome to Hospital Management System. How can I assist you?',
    'appointment': 'To book an appointment, please contact our reception desk or call us at +1-234-567-8900.',
    'doctor': 'We have experienced doctors in various departments including Cardiology, Neurology, Orthopedics, and more.',
    'timing': 'Our hospital is open 24/7. OPD timing: 9:00 AM to 5:00 PM (Mon-Sat).',
    'emergency': 'For emergencies, please call +1-234-567-8999 or visit our Emergency Department immediately.',
    'bill': 'For billing inquiries, please contact our billing department or check your account dashboard.',
    'pharmacy': 'Our pharmacy is open 24/7 with a wide range of medicines available.',
    'lab': 'Lab services are available from 7:00 AM to 8:00 PM. Reports are typically ready within 24 hours.',
    'location': 'We are located at 123 Health Street, Medical City. We have ample parking available.',
    'feedback': 'We value your feedback! Please share your experience at feedback@hospital.com.',
    'thank you': "You're welcome! Is there anything else I can help you with?",
    'thanks': "You're welcome! Feel free to ask if you need anything else.",
    'bye': 'Goodbye! Take care and stay healthy!',
    'default': "I'm sorry, I didn't understand that. Please contact our help desk for assistance."
};

function getChatbotResponse(message) {
    const msg = message.toLowerCase().trim();
    for (const [key, response] of Object.entries(CHATBOT_RESPONSES)) {
        if (msg.includes(key)) {
            return response;
        }
    }
    return CHATBOT_RESPONSES['default'];
}

function toggleChatbot() {
    const box = document.getElementById('chatbot-box');
    box.classList.toggle('open');
    if (box.classList.contains('open') && box.querySelector('.message') === null) {
        addChatbotMessage('bot', 'Hello! I am your hospital assistant. How can I help you today?');
    }
}

function addChatbotMessage(sender, text) {
    const container = document.getElementById('chatbot-messages');
    const msg = document.createElement('div');
    msg.className = `message ${sender}`;
    msg.textContent = text;
    container.appendChild(msg);
    container.scrollTop = container.scrollHeight;
}

function sendChatbotMessage() {
    const input = document.getElementById('chatbot-input-field');
    const message = input.value.trim();
    if (!message) return;

    addChatbotMessage('user', message);
    input.value = '';

    setTimeout(() => {
        const response = getChatbotResponse(message);
        addChatbotMessage('bot', response);
    }, 500);
}

document.addEventListener('DOMContentLoaded', function() {
    const input = document.getElementById('chatbot-input-field');
    if (input) {
        input.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendChatbotMessage();
            }
        });
    }
});
