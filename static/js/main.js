document.addEventListener('DOMContentLoaded', () => {
    const chatHistory = document.getElementById('chat-history');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const typingIndicator = document.getElementById('typing-indicator');
    const clearChatBtn = document.getElementById('clear-chat');
    const themeToggle = document.getElementById('theme-toggle');
    const authWrapper = document.getElementById('auth-wrapper');

    // Auth elements
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');
    const profileInfo = document.getElementById('profile-info');
    const showRegister = document.getElementById('show-register');
    const showLogin = document.getElementById('show-login');
    const userDisplayName = document.getElementById('user-display-name');
    const chatCount = document.getElementById('chat-count');

    let currentUser = null;

    // --- Theme Toggle ---
    themeToggle.addEventListener('click', () => {
        document.body.classList.toggle('dark-mode');
        const icon = themeToggle.querySelector('i');
        if (document.body.classList.contains('dark-mode')) {
            icon.className = 'fas fa-sun';
        } else {
            icon.className = 'fas fa-moon';
        }
    });

    // --- Auth View Switching ---
    showRegister.addEventListener('click', () => {
        loginForm.classList.add('hidden');
        registerForm.classList.remove('hidden');
    });

    showLogin.addEventListener('click', () => {
        registerForm.classList.add('hidden');
        loginForm.classList.remove('hidden');
    });

    // --- Authentication Logic ---
    document.getElementById('register-form-element').addEventListener('submit', async (e) => {
        e.preventDefault();
        const fullName = document.getElementById('reg-name').value;
        const email = document.getElementById('reg-email').value;
        const password = document.getElementById('reg-password').value;
        const confirmPassword = document.getElementById('reg-confirm-password').value;

        if (password !== confirmPassword) {
            alert("Passwords do not match!");
            return;
        }

        try {
            const response = await fetch('/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ full_name: fullName, email, password })
            });
            const data = await response.json();
            if (response.ok) {
                alert(data.message);
                showLogin.click();
            } else {
                alert(data.error || "Registration failed. Please try again.");
            }
        } catch (err) {
            console.error(err);
            alert("Registration failed. Please check your internet connection or try again later.");
        }
    });

    document.getElementById('login-form-element').addEventListener('submit', async (e) => {
        e.preventDefault();
        const email = document.getElementById('login-email').value;
        const password = document.getElementById('login-password').value;
        const remember = document.getElementById('remember-me').checked;

        try {
            const response = await fetch('/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password, remember })
            });
            const data = await response.json();
            if (response.ok) {
                currentUser = data.user;
                updateAuthUI();
                loadChatHistory();
            } else {
                alert(data.error || "Login failed. Please try again.");
            }
        } catch (err) {
            console.error(err);
            alert("Login failed. Please check your internet connection or try again later.");
        }
    });

    document.getElementById('logout-btn').addEventListener('click', async () => {
        await fetch('/logout', { method: 'POST' });
        currentUser = null;
        updateAuthUI();
        chatHistory.innerHTML = '<div class="message bot"><div class="message-content">Hello! I am Hemadri, your Smart AI Learning Assistant. How can I help you today?</div></div>';
    });

    function updateAuthUI() {
        if (currentUser) {
            loginForm.classList.add('hidden');
            registerForm.classList.add('hidden');
            profileInfo.classList.remove('hidden');
            userDisplayName.textContent = `Welcome, ${currentUser.full_name}!`;
        } else {
            profileInfo.classList.add('hidden');
            loginForm.classList.remove('hidden');
        }
    }

    // --- Chat Logic ---
    async function sendMessage() {
        const message = userInput.value.trim();
        if (!message) return;

        if (!currentUser) {
            alert("Please login to start chatting!");
            return;
        }

        // Append user message
        appendMessage('user', message);
        userInput.value = '';

        // Show typing indicator
        typingIndicator.style.display = 'flex';
        chatHistory.scrollTop = chatHistory.scrollHeight;

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message })
            });
            const data = await response.json();

            // Hide typing indicator
            typingIndicator.style.display = 'none';

            if (response.ok) {
                appendMessage('bot', data.response);
                updateChatCount();
            } else {
                appendMessage('bot', "Sorry, I encountered an error. Please try again.");
            }
        } catch (err) {
            typingIndicator.style.display = 'none';
            console.error(err);
        }
    }

    function appendMessage(sender, text) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${sender}`;
        msgDiv.innerHTML = `
            <div class="message-content">${text}</div>
            <span class="timestamp">${new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
        `;
        chatHistory.appendChild(msgDiv);
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }

    async function loadChatHistory() {
        const response = await fetch('/history');
        if (response.ok) {
            const history = await response.json();
            chatHistory.innerHTML = '';
            history.forEach(chat => {
                appendMessage('user', chat.message);
                appendMessage('bot', chat.response);
            });
            updateChatCount();
        }
    }

    async function updateChatCount() {
        const response = await fetch('/history');
        if (response.ok) {
            const history = await response.json();
            chatCount.textContent = history.length / 2;
        }
    }

    sendBtn.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });

    clearChatBtn.addEventListener('click', async () => {
        if (confirm("Are you sure you want to clear the chat history?")) {
            await fetch('/clear_chat', { method: 'POST' });
            chatHistory.innerHTML = '';
            appendMessage('bot', "Chat history cleared. How can I help you now?");
            updateChatCount();
        }
    });

    // --- PDF Export ---
    document.getElementById('export-chat').addEventListener('click', () => {
        const element = document.getElementById('chat-history');
        const opt = {
            margin: 1,
            filename: 'Hemadri_Chat_History.pdf',
            image: { type: 'jpeg', quality: 0.98 },
            html2canvas: { scale: 2 },
            jsPDF: { unit: 'in', format: 'letter', orientation: 'portrait' }
        };
        html2pdf().set(opt).from(element).save();
    });
});
