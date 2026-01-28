// Configuration
const API_BASE_URL = 'http://localhost:5000';

// State management
let sessionId = generateSessionId();
let isDebating = false;

// DOM Elements
const questionInput = document.getElementById('question-input');
const debateBtn = document.getElementById('debate-btn');
const followupInput = document.getElementById('followup-input');
const followupBtn = document.getElementById('followup-btn');
const resultsSection = document.getElementById('results-section');
const proContent = document.getElementById('pro-content');
const conContent = document.getElementById('con-content');
const moderatorContent = document.getElementById('moderator-content');
const errorMessage = document.getElementById('error-message');

// Event Listeners
debateBtn.addEventListener('click', handleDebateStart);
followupBtn.addEventListener('click', handleFollowup);

// Allow Enter key to submit (with Shift+Enter for new line)
questionInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        handleDebateStart();
    }
});

followupInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        handleFollowup();
    }
});

/**
 * Generate a unique session ID
 */
function generateSessionId() {
    return `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
}

/**
 * Handle initial debate start
 */
async function handleDebateStart() {
    const question = questionInput.value.trim();
    
    if (!question) {
        showError('Please enter a question or proposition.');
        return;
    }

    if (isDebating) return;

    hideError();
    setLoadingState(debateBtn, true);
    isDebating = true;

    try {
        // Show results section with loading state
        resultsSection.style.display = 'block';
        setLoadingPanels();
        scrollToResults();

        // Call backend API
        const response = await fetch(`${API_BASE_URL}/debate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                question: question,
                session_id: sessionId
            })
        });

        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }

        const data = await response.json();

        // Populate panels with responses
        displayResults(data);

    } catch (error) {
        console.error('Error:', error);
        showError(`Failed to start debate: ${error.message}. Make sure the backend server is running.`);
        resultsSection.style.display = 'none';
    } finally {
        setLoadingState(debateBtn, false);
        isDebating = false;
    }
}

/**
 * Handle follow-up questions
 */
async function handleFollowup() {
    const question = followupInput.value.trim();
    
    if (!question) {
        showError('Please enter a follow-up question.');
        return;
    }

    if (isDebating) return;

    hideError();
    setLoadingState(followupBtn, true);
    isDebating = true;

    try {
        // Set loading state for panels
        setLoadingPanels();
        scrollToResults();

        // Call backend API with same session
        const response = await fetch(`${API_BASE_URL}/debate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                question: question,
                session_id: sessionId
            })
        });

        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }

        const data = await response.json();

        // Display new responses
        displayResults(data);
        
        // Clear follow-up input
        followupInput.value = '';

    } catch (error) {
        console.error('Error:', error);
        showError(`Failed to continue debate: ${error.message}`);
    } finally {
        setLoadingState(followupBtn, false);
        isDebating = false;
    }
}

/**
 * Display debate results in panels
 */
function displayResults(data) {
    // Animate and display Pro agent response
    proContent.classList.remove('loading');
    proContent.innerHTML = formatResponse(data.pro);
    proContent.classList.add('fade-in');

    // Animate and display Con agent response
    conContent.classList.remove('loading');
    conContent.innerHTML = formatResponse(data.con);
    conContent.classList.add('fade-in');

    // Animate and display Moderator response
    moderatorContent.classList.remove('loading');
    moderatorContent.innerHTML = formatResponse(data.moderator);
    moderatorContent.classList.add('fade-in');
}

/**
 * Format response text with basic HTML
 */
function formatResponse(text) {
    if (!text) return '<p class="placeholder">No response received.</p>';
    
    // Convert newlines to paragraphs
    const paragraphs = text.split('\n\n').filter(p => p.trim());
    
    if (paragraphs.length === 0) {
        return `<p>${escapeHtml(text)}</p>`;
    }
    
    return paragraphs.map(p => `<p>${escapeHtml(p.trim())}</p>`).join('');
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Set loading state for panels
 */
function setLoadingPanels() {
    proContent.classList.add('loading');
    proContent.innerHTML = '';
    
    conContent.classList.add('loading');
    conContent.innerHTML = '';
    
    moderatorContent.classList.add('loading');
    moderatorContent.innerHTML = '';
}

/**
 * Set button loading state
 */
function setLoadingState(button, loading) {
    const btnText = button.querySelector('.btn-text');
    const btnLoader = button.querySelector('.btn-loader');
    
    if (loading) {
        btnText.style.display = 'none';
        btnLoader.style.display = 'flex';
        button.disabled = true;
    } else {
        btnText.style.display = 'block';
        btnLoader.style.display = 'none';
        button.disabled = false;
    }
}

/**
 * Show error message
 */
function showError(message) {
    errorMessage.textContent = message;
    errorMessage.style.display = 'block';
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        hideError();
    }, 5000);
}

/**
 * Hide error message
 */
function hideError() {
    errorMessage.style.display = 'none';
}

/**
 * Scroll to results section
 */
function scrollToResults() {
    setTimeout(() => {
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 100);
}

/**
 * Display debate results in panels
 */
function displayResults(data) {
    console.log('=== DISPLAYING RESULTS ===');
    console.log('Pro length:', data.pro?.length || 0);
    console.log('Con length:', data.con?.length || 0);
    console.log('Moderator length:', data.moderator?.length || 0);
    console.log('Pro content:', data.pro);
    console.log('Con content:', data.con);
    console.log('Moderator content:', data.moderator);
    
    // Animate and display Pro agent response
    proContent.classList.remove('loading');
    proContent.innerHTML = formatResponse(data.pro);
    proContent.classList.add('fade-in');

    // Animate and display Con agent response
    conContent.classList.remove('loading');
    conContent.innerHTML = formatResponse(data.con);
    conContent.classList.add('fade-in');

    // Animate and display Moderator response
    moderatorContent.classList.remove('loading');
    moderatorContent.innerHTML = formatResponse(data.moderator);
    moderatorContent.classList.add('fade-in');
    
    console.log('=== DISPLAY COMPLETE ===');
}

/**
 * Format response text with basic HTML
 */
function formatResponse(text) {
    if (!text) return '<p class="placeholder">No response received.</p>';
    
    console.log('Formatting text of length:', text.length);
    
    // Convert newlines to paragraphs
    const paragraphs = text.split('\n\n').filter(p => p.trim());
    
    if (paragraphs.length === 0) {
        return `<p>${escapeHtml(text)}</p>`;
    }
    
    const formatted = paragraphs.map(p => `<p>${escapeHtml(p.trim())}</p>`).join('');
    console.log('Formatted HTML length:', formatted.length);
    
    return formatted;
}
/**
 * Initialize app
 */
function init() {
    console.log('Gemini Multi-Agent Debate Console initialized');
    console.log('Session ID:', sessionId);
    console.log('API Base URL:', API_BASE_URL);
}

// Run initialization
init();