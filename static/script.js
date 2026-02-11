// Function to switch between dashboard tabs
function showSection(id) {
    const sections = ['chat-sec', 'roadmap-sec', 'quiz-sec', 'youtube-sec'];
    sections.forEach(sec => {
        const el = document.getElementById(sec);
        if (el) el.style.display = 'none';
    });
    
    const target = document.getElementById(id);
    if (target) target.style.display = 'block';
}

// Function to redirect to external AI
function redirectAI(platform) {
    const inputElement = document.getElementById('chat-input');
    
    if (!inputElement) {
        console.error("Missing chat-input ID in HTML");
        return;
    }

    const userInput = inputElement.value;
    
    if (!userInput.trim()) {
        alert("Please type a question first!");
        return;
    }

    const encodedPrompt = encodeURIComponent(userInput);
    let url = platform === 'chatgpt' 
        ? `https://chatgpt.com/?q=${encodedPrompt}` 
        : `https://gemini.google.com/app?q=${encodedPrompt}`;

    window.open(url, '_blank');
}

// Updated askAI to render HTML tags correctly
async function askAI(mode) {
    const outputDiv = document.getElementById(`${mode}-output`);
    const inputId = mode === 'roadmap' ? 'topic-input' : 'quiz-topic-input';
    const userInput = document.getElementById(inputId).value;

    if (!userInput) return alert("Please enter a topic!");

    outputDiv.innerHTML = "<em>Searching Database...</em>";

    try {
        const response = await fetch('/ai_engine', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ mode: mode, topic: userInput })
        });
        
        const data = await response.json();
        
        // Use .innerHTML to render bold tags and convert \n to <br>
        outputDiv.innerHTML = data.result.replace(/\n/g, '<br>'); 

    } catch (error) {
        outputDiv.innerHTML = "Error: Could not retrieve data.";
    }
}
// Add this to the bottom of script.js
document.addEventListener('keypress', function (e) {
    if (e.key === 'Enter' && document.activeElement.id === 'chat-input') {
        redirectAI('chatgpt'); // Or askAI('chat')
    }
});