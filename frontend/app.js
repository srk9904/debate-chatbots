const MOCK_MODE = false; // true: without backend

// Configuration
const API_BASE_URL = 'http://localhost:5000';

// State
let sessionId = generateSessionId();
let currentRound = 1;
let totalRounds = 2;
let currentAgentIndex = 0; // 0=pro, 1=con, 2=moderator
let currentRoundResponses = null; // Store all three responses
let debateActive = false;
let additionalRounds = 2; // Default additional rounds for continue

// DOM Elements
const setupSection = document.getElementById('setup-section');
const arenaSection = document.getElementById('arena-section');
const questionInput = document.getElementById('question-input');
const startDebateBtn = document.getElementById('start-debate-btn');
const nextTurnBtn = document.getElementById('next-turn-btn');
const addCommentBtn = document.getElementById('add-comment-btn');
const newDebateBtn = document.getElementById('new-debate-btn');
const continueDebateBtn = document.getElementById('continue-debate-btn');
const commentModal = document.getElementById('comment-modal');
const continueModal = document.getElementById('continue-modal');
const submitCommentBtn = document.getElementById('submit-comment-btn');
const cancelCommentBtn = document.getElementById('cancel-comment-btn');
const commentInput = document.getElementById('comment-input');
const continueRoundBtns = document.querySelectorAll('.continue-round-btn');
const continueWithCommentBtn = document.getElementById('continue-with-comment-btn');
const continueWithoutCommentBtn = document.getElementById('continue-without-comment-btn');
const cancelContinueBtn = document.getElementById('cancel-continue-btn');
const continueCommentInput = document.getElementById('continue-comment-input');
const errorMessage = document.getElementById('error-message');

// Round selector
const roundBtns = document.querySelectorAll('.round-btn');
const selectedRoundsSpan = document.getElementById('selected-rounds');

// Event Listeners
startDebateBtn.addEventListener('click', startDebate);
nextTurnBtn.addEventListener('click', showNextAgent);
addCommentBtn.addEventListener('click', () => commentModal.style.display = 'flex');
submitCommentBtn.addEventListener('click', submitComment);
cancelCommentBtn.addEventListener('click', () => commentModal.style.display = 'none');
newDebateBtn.addEventListener('click', resetDebate);
continueDebateBtn.addEventListener('click', () => continueModal.style.display = 'flex');
continueWithCommentBtn.addEventListener('click', continueWithComment);
continueWithoutCommentBtn.addEventListener('click', continueWithoutComment);
cancelContinueBtn.addEventListener('click', () => continueModal.style.display = 'none');

// Round selection
roundBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        roundBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        totalRounds = parseInt(btn.dataset.rounds);
        selectedRoundsSpan.textContent = totalRounds;
    });
});

// Continue round selection
continueRoundBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        continueRoundBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        additionalRounds = parseInt(btn.dataset.rounds);
    });
});

function generateSessionId() {
    return `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
}

async function startDebate() {
    const question = questionInput.value.trim();
    if (!question) {
        showError('Please enter a debate topic.');
        return;
    }

    hideError();
    setLoadingState(startDebateBtn, true);

    // ===== MOCK MODE =====
    if (MOCK_MODE) {
        await new Promise(r => setTimeout(r, 400));

        // Mock responses for all three agents
        currentRoundResponses = {
            pro: "Mock Pro opening: I strongly support this proposition because it offers significant benefits. First, it increases efficiency across the board. Second, it reduces costs substantially. Third, it opens new opportunities that weren't previously available.",
            con: "Mock Con response: I must respectfully disagree with the Pro side's assessment. Their argument overlooks several critical flaws. First, the efficiency gains are overstated and context-dependent. Second, the cost analysis ignores hidden expenses. Third, the supposed opportunities come with significant risks.",
            moderator: "Mock Moderator synthesis: Both sides present compelling arguments that highlight the core tension in this debate. The Pro side emphasizes efficiency and opportunity, while the Con side raises valid concerns about overlooked costs and risks. The central question becomes whether the benefits outweigh the potential downsides in practice."
        };

        setupSection.style.display = 'none';
        arenaSection.style.display = 'block';

        currentRound = 1;
        currentAgentIndex = 0;
        debateActive = true;

        document.getElementById('current-round').textContent = currentRound;
        document.getElementById('total-rounds').textContent = totalRounds;
        updateProgress();

        showCurrentAgent();

        setLoadingState(startDebateBtn, false);
        return;
    }

    // ===== REAL BACKEND (SINGLE API CALL) =====
    try {
        console.log('🚀 Starting debate with single API call...');
        
        const response = await fetch(`${API_BASE_URL}/debate/start`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                question: question,
                session_id: sessionId,
                rounds: totalRounds
            })
        });

        if (!response.ok) throw new Error(`Server error: ${response.status}`);
        const data = await response.json();

        console.log('✅ Received all responses:', {
            pro: data.responses.pro.length + ' chars',
            con: data.responses.con.length + ' chars',
            mod: data.responses.moderator.length + ' chars'
        });

        // Store all three responses
        currentRoundResponses = data.responses;
        currentRound = data.round;
        currentAgentIndex = 0;
        debateActive = true;

        setupSection.style.display = 'none';
        arenaSection.style.display = 'block';

        document.getElementById('current-round').textContent = currentRound;
        document.getElementById('total-rounds').textContent = totalRounds;
        updateProgress();

        showCurrentAgent();

    } catch (error) {
        console.error('Error:', error);
        showError(`Failed to start debate: ${error.message}`);
    } finally {
        setLoadingState(startDebateBtn, false);
    }
}

function showCurrentAgent() {
    const agents = ['pro', 'con', 'moderator'];
    const agentNames = ['Pro Agent', 'Con Agent', 'Moderator'];
    
    const agentType = agents[currentAgentIndex];
    const agentName = agentNames[currentAgentIndex];
    const content = currentRoundResponses[agentType];
    
    console.log(`📢 Showing ${agentName}:`, content.substring(0, 100) + '...');
    
    showAgent(agentType, content);
    addToHistory(agentName, content, agentType);
}

async function showNextAgent() {
    if (!debateActive) return;

    // Hide current agent
    hideAllAgents();
    await new Promise(resolve => setTimeout(resolve, 500));

    currentAgentIndex++;

    // ===== MOCK MODE =====
    if (MOCK_MODE) {
        // Check if we've shown all three agents for this round
        if (currentAgentIndex > 2) {
            // Round complete
            if (currentRound >= totalRounds) {
                debateComplete();
                return;
            }
            
            // Generate mock next round
            await new Promise(r => setTimeout(r, 400));
            
            currentRoundResponses = {
                pro: `Mock Pro Round ${currentRound + 1}: Building on previous points, I maintain that this proposition holds strong merit despite objections raised.`,
                con: `Mock Con Round ${currentRound + 1}: The Pro side still fails to address fundamental concerns I outlined previously.`,
                moderator: `Mock Moderator Round ${currentRound + 1}: As the debate continues, we see both sides refining their positions based on the ongoing exchange.`
            };
            
            currentRound++;
            currentAgentIndex = 0;
            
            document.getElementById('current-round').textContent = currentRound;
            updateProgress();
            
            showCurrentAgent();
        } else {
            // Show next agent in current round
            showCurrentAgent();
        }
        return;
    }

    // ===== REAL BACKEND =====
    // Check if we've shown all three agents for this round
    if (currentAgentIndex > 2) {
        // Round complete, check if we need another round
        if (currentRound >= totalRounds) {
            debateComplete();
            return;
        }
        
        // Load next round
        await loadNextRound();
    } else {
        // Show next agent in current round
        showCurrentAgent();
    }
}

async function loadNextRound() {
    setLoadingState(nextTurnBtn, true);
    hideError();

    try {
        console.log(`🔄 Loading Round ${currentRound + 1} with single API call...`);
        
        const response = await fetch(`${API_BASE_URL}/debate/next-round`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                session_id: sessionId,
                current_round: currentRound,
                total_rounds: totalRounds
            })
        });

        if (!response.ok) throw new Error(`Server error: ${response.status}`);
        const data = await response.json();

        if (data.debate_complete && !data.responses) {
            debateComplete();
            return;
        }

        console.log('✅ Received Round ' + data.round + ' responses');

        // Store new round responses
        currentRoundResponses = data.responses;
        currentRound = data.round;
        currentAgentIndex = 0;
        
        document.getElementById('current-round').textContent = currentRound;
        updateProgress();

        // Show first agent of new round (Pro)
        showCurrentAgent();

    } catch (error) {
        console.error('Error:', error);
        showError(`Failed to load next round: ${error.message}`);
    } finally {
        setLoadingState(nextTurnBtn, false);
    }
}

function showAgent(turn, content) {
    const agentMap = {
        'pro': 'pro-character',
        'con': 'con-character',
        'moderator': 'moderator-character'
    };

    const speechMap = {
        'pro': 'pro-speech',
        'con': 'con-speech',
        'moderator': 'moderator-speech'
    };

    const characterId = agentMap[turn];
    const speechId = speechMap[turn];

    if (characterId && speechId) {
        const character = document.getElementById(characterId);
        const speech = document.getElementById(speechId);
        const bubble = speech.closest('.speech-bubble');

        speech.textContent = content;
        
        // Dynamic sizing based on content length
        if (content.length > 500) {
            bubble.classList.add('long-content');
        } else {
            bubble.classList.remove('long-content');
        }
        
        character.style.display = 'flex';

        // Stage tint control
        const stage = document.querySelector('.debate-stage');
        stage.classList.remove('pro-active','con-active','moderator-active');
        stage.classList.add(`${turn}-active`);

        // Trigger animation
        setTimeout(() => {
            character.classList.add('active');
        }, 50);
    }
}

function hideAllAgents() {
    ['pro-character', 'con-character', 'moderator-character'].forEach(id => {
        const el = document.getElementById(id);
        el.classList.remove('active');
        el.classList.add('fade-out');
        setTimeout(() => {
            el.style.display = 'none';
            el.classList.remove('fade-out');
        }, 400);
    });

    // Remove stage tint when clearing
    document.querySelector('.debate-stage')
        .classList.remove('pro-active','con-active','moderator-active');
}

function addToHistory(agent, content, type) {
    const historyContent = document.getElementById('history-content');
    
    const item = document.createElement('div');
    item.className = `history-item ${type}`;
    
    const agentLabel = document.createElement('strong');
    agentLabel.textContent = agent;
    
    // Preview text (truncated)
    const previewText = document.createElement('p');
    previewText.className = 'preview-text';
    previewText.textContent = content.substring(0, 200) + (content.length > 200 ? '...' : '');
    
    // Full text (hidden by default)
    const fullText = document.createElement('div');
    fullText.className = 'full-text';
    fullText.textContent = content;
    
    // Expand hint
    if (content.length > 200) {
        const expandHint = document.createElement('span');
        expandHint.className = 'expand-hint';
        expandHint.textContent = '(Click to expand)';
        item.appendChild(agentLabel);
        item.appendChild(previewText);
        item.appendChild(expandHint);
        item.appendChild(fullText);
        
        // Toggle expand on click
        item.addEventListener('click', () => {
            item.classList.toggle('expanded');
        });
    } else {
        item.appendChild(agentLabel);
        item.appendChild(previewText);
    }
    
    historyContent.appendChild(item);
    
    // Scroll to bottom
    historyContent.scrollTop = historyContent.scrollHeight;
}

async function submitComment() {
    const comment = commentInput.value.trim();
    
    if (!comment) return;

    try {
        if (!MOCK_MODE) {
            await fetch(`${API_BASE_URL}/debate/add-comment`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    session_id: sessionId,
                    comment: comment
                })
            });
        }

        addToHistory('You', comment, 'user');
        commentInput.value = '';
        commentModal.style.display = 'none';

    } catch (error) {
        console.error('Error:', error);
        showError('Failed to add comment');
    }
}

async function continueWithComment() {
    const comment = continueCommentInput.value.trim();
    
    if (!comment) {
        showError('Please enter a comment or use "Continue Without Comment"');
        return;
    }

    // Add comment to history
    if (!MOCK_MODE) {
        try {
            await fetch(`${API_BASE_URL}/debate/add-comment`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    session_id: sessionId,
                    comment: comment
                })
            });
        } catch (error) {
            console.error('Error adding comment:', error);
        }
    }

    addToHistory('You', comment, 'user');
    continueCommentInput.value = '';
    continueModal.style.display = 'none';

    // Continue the debate
    await continueDebateRounds();
}

async function continueWithoutComment() {
    continueModal.style.display = 'none';
    await continueDebateRounds();
}

async function continueDebateRounds() {
    // Extend total rounds
    totalRounds += additionalRounds;
    document.getElementById('total-rounds').textContent = totalRounds;
    updateProgress();

    // Re-enable debate controls
    debateActive = true;
    nextTurnBtn.style.display = 'block';
    addCommentBtn.style.display = 'block';
    newDebateBtn.style.display = 'none';
    continueDebateBtn.style.display = 'none';

    hideError();
    
    console.log(`🔄 Continuing debate for ${additionalRounds} more rounds (total now: ${totalRounds})`);

    // Automatically load next round
    if (MOCK_MODE) {
        // Generate mock next round
        await new Promise(r => setTimeout(r, 400));
        
        currentRoundResponses = {
            pro: `Mock Pro Round ${currentRound + 1}: Continuing the debate with fresh perspective.`,
            con: `Mock Con Round ${currentRound + 1}: Addressing the new direction of this discussion.`,
            moderator: `Mock Moderator Round ${currentRound + 1}: Synthesizing the continued exchange.`
        };
        
        currentRound++;
        currentAgentIndex = 0;
        
        document.getElementById('current-round').textContent = currentRound;
        updateProgress();
        
        showCurrentAgent();
    } else {
        await loadNextRound();
    }
}

function debateComplete() {
    debateActive = false;
    nextTurnBtn.style.display = 'none';
    addCommentBtn.style.display = 'none';
    newDebateBtn.style.display = 'block';
    continueDebateBtn.style.display = 'block'; // Show continue button
    
    showError('🎉 Debate Complete! You can continue for more rounds or start a new debate.');
    setTimeout(() => hideError(), 8000);
}

function resetDebate() {
    sessionId = generateSessionId();
    currentRound = 1;
    currentAgentIndex = 0;
    currentRoundResponses = null;
    debateActive = false;
    
    setupSection.style.display = 'block';
    arenaSection.style.display = 'none';
    questionInput.value = '';
    document.getElementById('history-content').innerHTML = '';
    nextTurnBtn.style.display = 'block';
    addCommentBtn.style.display = 'block';
    newDebateBtn.style.display = 'none';
    continueDebateBtn.style.display = 'none'; // Hide continue button

    hideAllAgents();
    hideError();
}

function updateProgress() {
    const percentage = (currentRound / totalRounds) * 100;
    document.getElementById('progress-fill').style.width = percentage + '%';
}

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

function showError(message) {
    errorMessage.textContent = message;
    errorMessage.style.display = 'block';
}

function hideError() {
    errorMessage.style.display = 'none';
}

console.log('🎭 Gemini Debate Arena v3.1 initialized (Improved Readability + Dynamic Sizing)');
console.log('Mock Mode:', MOCK_MODE ? 'ENABLED' : 'DISABLED');
console.log('Session ID:', sessionId);