class AsuraAIChat {
    constructor() {
        this.chatMessages = document.getElementById('chatMessages');
        this.messageInput = document.getElementById('messageInput');
        this.chatForm = document.getElementById('chatForm');
        this.sendButton = document.getElementById('sendButton');
        this.typingIndicator = document.getElementById('typingIndicator');
        
        this.initializeEventListeners();
        this.messageInput.focus();
    }
    
    initializeEventListeners() {
        // Form submission
        this.chatForm.addEventListener('submit', (e) => {
            e.preventDefault();
            this.sendMessage();
        });
        
        // Enter key handling
        this.messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        // Auto-resize input (if needed)
        this.messageInput.addEventListener('input', () => {
            this.validateInput();
        });
    }
    
    validateInput() {
        const message = this.messageInput.value.trim();
        this.sendButton.disabled = message.length === 0;
    }
    
    async sendMessage() {
        const message = this.messageInput.value.trim();
        
        if (!message) {
            return;
        }
        
        // Disable input while processing
        this.setInputState(false);
        
        // Add user message to chat
        this.addMessage(message, 'user');
        
        // Clear input
        this.messageInput.value = '';
        this.validateInput();
        
        // Show typing indicator
        this.showTypingIndicator();
        
        try {
            // Send message to backend
            const response = await this.sendToBackend(message);
            
            // Hide typing indicator
            this.hideTypingIndicator();
            
            // Add AI response to chat
            this.addMessage(response.response, 'ai');
            
        } catch (error) {
            console.error('Error sending message:', error);
            
            // Hide typing indicator
            this.hideTypingIndicator();
            
            // Add error message
            this.addMessage(
                'I apologize, but I encountered an error processing your request. Please try again.',
                'ai'
            );
        }
        
        // Re-enable input
        this.setInputState(true);
        this.messageInput.focus();
    }
    
    async sendToBackend(message) {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Failed to get response');
        }
        
        return await response.json();
    }
    
    addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const avatarDiv = document.createElement('div');
        avatarDiv.className = 'message-avatar';
        
        if (sender === 'ai') {
            avatarDiv.innerHTML = '<i class="fas fa-robot"></i>';
        } else {
            avatarDiv.innerHTML = '<i class="fas fa-user"></i>';
        }
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        
        const textDiv = document.createElement('div');
        textDiv.className = 'message-text';
        
        // Safely render formatted text using DOM methods
        this.renderFormattedText(textDiv, text);
        
        const timeDiv = document.createElement('div');
        timeDiv.className = 'message-time';
        timeDiv.textContent = this.getCurrentTime();
        
        contentDiv.appendChild(textDiv);
        contentDiv.appendChild(timeDiv);
        
        messageDiv.appendChild(avatarDiv);
        messageDiv.appendChild(contentDiv);
        
        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
    }
    
    renderFormattedText(container, text) {
        // Clear container
        container.textContent = '';
        
        // Split text by lines to handle line breaks and lists
        const lines = text.split('\n');
        let currentList = null;
        
        for (let i = 0; i < lines.length; i++) {
            const line = lines[i];
            
            // Check if line is a bullet point
            const bulletMatch = line.match(/^\s*[-•]\s+(.+)$/);
            if (bulletMatch) {
                // Create or continue list
                if (!currentList) {
                    currentList = document.createElement('ul');
                    container.appendChild(currentList);
                }
                const li = document.createElement('li');
                this.renderFormattedTextInline(li, bulletMatch[1]);
                currentList.appendChild(li);
            } else {
                // End current list if exists
                currentList = null;
                
                // Create paragraph for regular text
                if (line.trim()) {
                    const p = document.createElement('div');
                    this.renderFormattedTextInline(p, line);
                    container.appendChild(p);
                } else if (i < lines.length - 1) {
                    // Add line break for empty lines (except last)
                    container.appendChild(document.createElement('br'));
                }
            }
        }
    }
    
    renderFormattedTextInline(container, text) {
        // Process inline formatting like **bold** safely
        const parts = text.split(/(\*\*.*?\*\*)/);
        
        for (const part of parts) {
            if (part.startsWith('**') && part.endsWith('**') && part.length > 4) {
                // Bold text
                const strong = document.createElement('strong');
                strong.textContent = part.slice(2, -2);
                container.appendChild(strong);
            } else if (part) {
                // Regular text
                container.appendChild(document.createTextNode(part));
            }
        }
    }
    
    getCurrentTime() {
        const now = new Date();
        return now.toLocaleTimeString([], { 
            hour: '2-digit', 
            minute: '2-digit' 
        });
    }
    
    setInputState(enabled) {
        this.messageInput.disabled = !enabled;
        this.sendButton.disabled = !enabled;
    }
    
    showTypingIndicator() {
        this.typingIndicator.style.display = 'block';
        this.scrollToBottom();
    }
    
    hideTypingIndicator() {
        this.typingIndicator.style.display = 'none';
    }
    
    scrollToBottom() {
        // Smooth scroll to bottom with a small delay to ensure content is rendered
        setTimeout(() => {
            this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
        }, 100);
    }
    
    // Method to handle iframe resize if needed
    handleResize() {
        this.scrollToBottom();
    }
}

// Initialize chat when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const chat = new AsuraAIChat();
    
    // Handle window resize for iframe compatibility
    window.addEventListener('resize', () => {
        chat.handleResize();
    });
    
    // Global error handler
    window.addEventListener('error', (e) => {
        console.error('Global error:', e.error);
    });
    
    // Make chat instance globally available if needed
    window.asuraChat = chat;
});
