# 🎭 Gemini Multi-Agent Debate Console - Complete Project Documentation

## 📋 Project Overview

**Name:** Gemini Multi-Agent Debate Console (Turn-Based Edition)

**Description:** A web-based debate system where three AI agents (Pro, Con, Moderator) engage in structured debates on any topic. The system features turn-based rounds, animated character appearances, and real-time user interaction.

**Tech Stack:**
- **Backend:** Python 3.10+, Flask, Google Gemini API
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **AI Model:** Gemini 2.5 Flash (via google-generativeai SDK)

**Key Features:**
1. Turn-based debate rounds (1-5 rounds user-configurable)
2. Three specialized AI agents with distinct roles
3. Animated character appearances (Pro from left, Con from right, Moderator from top)
4. Agents directly respond to each other's arguments
5. Session-based conversation memory
6. Mid-debate user comments
7. Visual progress tracking
8. Rate limit handling with automatic delays

---

## 📁 Complete Folder Structure

```
gemini_debate_console/
│
├── .env                           # Environment variables (API key)
├── requirements.txt               # Python dependencies
├── README.md                      # Project documentation
│
├── backend/
│   ├── app.py                     # Main Flask server (turn-based version)
│   │
│   ├── agents/
│   │   ├── __init__.py           # Empty file (makes it a Python package)
│   │   ├── pro_agent.py          # Pro argument generator
│   │   ├── con_agent.py          # Con argument generator
│   │   └── moderator_agent.py    # Synthesis/moderation agent
│   │
│   ├── memory/
│   │   ├── __init__.py           # Empty file
│   │   └── session_store.py      # Conversation history manager
│   │
│   ├── prompts/
│   │   ├── pro_prompt.txt        # Pro agent system prompt (optional, not used in current version)
│   │   ├── con_prompt.txt        # Con agent system prompt (optional)
│   │   └── moderator_prompt.txt  # Moderator system prompt (optional)
│   │
│   └── utils/
│       ├── __init__.py           # Empty file
│       └── gemini_client.py      # Gemini API wrapper
│
└── frontend/
    ├── index.html                # Main UI (turn-based interface)
    ├── styles.css                # Styling with animations
    ├── app.js                    # Frontend logic
    ├── pro_agent.png            # Optional: Pro character image (150x150px+)
    ├── con_agent.png            # Optional: Con character image (150x150px+)
    └── moderator_agent.png      # Optional: Moderator character image (150x150px+)
```

---

## 📄 File-by-File Documentation

### Root Files

#### `.env`
**Purpose:** Store sensitive configuration (API key)

**Content:**
```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

**Important:** 
- Never commit this file to version control
- Get API key from: https://makersuite.google.com/app/apikey
- Free tier: 5 requests/minute

---

#### `requirements.txt`
**Purpose:** Python dependencies for pip installation

**Content:**
```txt
flask==3.0.0
flask-cors==4.0.0
google-generativeai==0.3.2
python-dotenv==1.0.0
```

**Installation:** `pip install -r requirements.txt`

---

### Backend Files

#### `backend/app.py`
**Purpose:** Main Flask server with turn-based debate endpoints

**Key Features:**
- `/debate/start` - Initialize new debate, return Pro's opening
- `/debate/next-turn` - Get next agent's response
- `/debate/add-comment` - Add user comment mid-debate
- `/history/<session_id>` - Retrieve conversation history
- `/clear/<session_id>` - Clear session
- Automatic 5-second delays between API calls (rate limiting)
- Turn management (Pro → Con → Moderator → Pro...)
- Round tracking and completion detection

**Key Variables:**
- `total_rounds` - Number of debate rounds
- `current_round` - Current round number
- `current_turn` - Current agent ('pro', 'con', 'moderator')
- `session_id` - Unique identifier for conversation

**Dependencies:**
```python
from flask import Flask, request, jsonify
from flask_cors import CORS
from agents.pro_agent import ProAgent
from agents.con_agent import ConAgent
from agents.moderator_agent import ModeratorAgent
from memory.session_store import SessionStore
```

**Port:** 5000 (default)

---

#### `backend/agents/pro_agent.py`
**Purpose:** Generate arguments IN FAVOR of the proposition

**Class:** `ProAgent`

**Key Method:** `generate_response(question, history=None)`

**Logic:**
1. Check if responding to Con's argument (look for last 'con' message in history)
2. If responding: Address Con's objections + present new supporting points
3. If opening: Present 2-3 strong reasons supporting the position
4. Target length: 200-250 words
5. Token limit: 1500 (ensures complete responses)

**Prompt Strategy:**
- Opening: "Present 2-3 clear, strong reasons supporting this position"
- Response: "Address their main objection + present 1-2 NEW strong points"
- Emphasizes: No bullet points, clear paragraphs, complete sentences

**API Call:**
```python
response = self.client.generate(
    prompt=prompt,
    max_tokens=1500,
    temperature=0.8
)
```

---

#### `backend/agents/con_agent.py`
**Purpose:** Generate arguments AGAINST the proposition

**Class:** `ConAgent`

**Key Method:** `generate_response(question, history=None)`

**Logic:**
1. Extract last Pro argument from history
2. Point out specific flaws in Pro's reasoning
3. Present 1-2 strong counterpoints
4. Target length: 200-250 words
5. Token limit: 1500

**Prompt Strategy:**
- "Point out specific flaws in their argument"
- "Explain WHY their reasoning is wrong or incomplete"
- "Present strong counterpoints"
- Conversational and engaging tone

**Key Difference from Pro:**
- ALWAYS responds to Pro's previous argument (except in edge cases)
- Focuses on critique and rebuttal
- Identifies risks, downsides, problems

---

#### `backend/agents/moderator_agent.py`
**Purpose:** Synthesize Pro and Con arguments into balanced analysis

**Class:** `ModeratorAgent`

**Key Method:** `generate_response(question, pro_argument, con_argument, history=None)`

**Logic:**
1. Receives BOTH Pro and Con arguments from current round
2. Determines round number from history
3. Summarizes the key clash/disagreement
4. Notes good points from each side
5. Identifies core tension or trade-off
6. Target length: 150-200 words
7. Token limit: 1200

**Prompt Strategy:**
- "Briefly summarize the key clash in THIS round"
- "Note any good points from each side"
- "Identify the core tension or trade-off"
- Balanced and fair

**Unique Feature:**
- Only agent that receives arguments from BOTH sides simultaneously
- Tracks round number for context

---

#### `backend/memory/session_store.py`
**Purpose:** Manage conversation history across sessions

**Class:** `SessionStore`

**Data Structure:**
```python
sessions = {
    'session_123': {
        'created_at': '2026-01-28T10:30:00',
        'messages': [
            {'role': 'user', 'content': '...', 'timestamp': '...'},
            {'role': 'pro', 'content': '...', 'timestamp': '...'},
            {'role': 'con', 'content': '...', 'timestamp': '...'},
            {'role': 'moderator', 'content': '...', 'timestamp': '...'}
        ]
    }
}
```

**Key Methods:**
- `get_history(session_id)` - Returns list of messages
- `add_message(session_id, role, content)` - Appends new message
- `clear_session(session_id)` - Deletes all messages
- `list_sessions()` - Returns all active session IDs
- `get_session_info(session_id)` - Returns metadata

**Storage:** In-memory (resets on server restart)

**Message Roles:**
- `'user'` - User's questions/comments
- `'pro'` - Pro agent's arguments
- `'con'` - Con agent's arguments
- `'moderator'` - Moderator's synthesis
- `'system'` - Internal state tracking

---

#### `backend/utils/gemini_client.py`
**Purpose:** Wrapper for Google Gemini API calls

**Class:** `GeminiClient`

**Initialization:**
1. Loads API key from environment
2. Configures `google.generativeai`
3. Tries multiple model names to find working one:
   - `models/gemini-2.5-flash` (primary)
   - `models/gemini-flash-latest` (fallback)
   - `models/gemini-2.0-flash`
   - `models/gemini-pro-latest`
   - `models/gemini-2.5-pro`

**Key Method:** `generate(prompt, max_tokens=1500, temperature=0.7, ...)`

**Features:**
- Automatic retry logic for rate limits (max_retries parameter)
- Extracts wait time from error messages
- Exponential backoff
- Token counting support

**Configuration:**
```python
generation_config = genai.GenerationConfig(
    max_output_tokens=max_tokens,
    temperature=temperature,
    top_p=top_p,
    top_k=top_k
)
```

**Error Handling:**
- Detects 429 rate limit errors
- Extracts retry delay from error message
- Waits specified time before retrying
- Default: 0 retries (fail fast) to avoid long waits

---

### Frontend Files

#### `frontend/index.html`
**Purpose:** User interface for turn-based debate system

**Key Sections:**

1. **Setup Section** (`#setup-section`)
   - Question/topic input textarea
   - Round selector buttons (1-5 rounds)
   - Start Debate button
   - Visible at start, hidden during debate

2. **Arena Section** (`#arena-section`)
   - Round indicator with progress bar
   - Debate stage (where characters appear)
   - Three character containers:
     - `#pro-character` - Left side, green theme
     - `#con-character` - Right side, red theme
     - `#moderator-character` - Top center, white/gold theme
   - Each has avatar + speech bubble
   - History panel (scrollable list of exchanges)
   - User interaction buttons:
     - Next Turn (advances debate)
     - Add Comment (opens modal)
     - New Debate (resets everything)

3. **Comment Modal** (`#comment-modal`)
   - Textarea for user input
   - Submit/Cancel buttons
   - Overlay with backdrop

4. **Character Structure:**
```html
<div class="character-container pro-character">
    <div class="character-avatar pro-avatar">
        <img src="pro_agent.png" onerror="[fallback SVG]">
    </div>
    <div class="speech-bubble pro-bubble">
        <p id="pro-speech"></p>
    </div>
</div>
```

**Image Fallback:**
If PNG images not found, displays colored circles with text:
- Pro: Green circle with "PRO"
- Con: Red circle with "CON"
- Mod: White circle with "MOD"

---

#### `frontend/styles.css`
**Purpose:** Styling and animations

**Color Scheme:**
- **Pro:** Green (#22c55e, #16a34a)
- **Con:** Red (#ef4444, #dc2626)
- **Moderator:** White/Gold (#ffffff, #d1af37, #fcc200)
- **Background:** Dark gradients (#0a0a0a, #1a1a2e)

**Key Animations:**

1. **`slideInFromLeft`** (Pro Agent)
```css
@keyframes slideInFromLeft {
    from { left: -300px; opacity: 0; }
    to { left: 20px; opacity: 1; }
}
```
Duration: 0.6s

2. **`slideInFromRight`** (Con Agent)
```css
@keyframes slideInFromRight {
    from { right: -300px; opacity: 0; }
    to { right: 20px; opacity: 1; }
}
```
Duration: 0.6s

3. **`slideInFromTop`** (Moderator)
```css
@keyframes slideInFromTop {
    from { top: -300px; opacity: 0; }
    to { top: 20px; opacity: 1; }
}
```
Duration: 0.6s

4. **`fadeOutSlow`** (All agents when leaving)
```css
@keyframes fadeOutSlow {
    from { opacity: 1; }
    to { opacity: 0; transform: scale(0.95); }
}
```
Duration: 0.4s

**Character Shadows/Glows:**
- Pro: `box-shadow: 0 0 40px rgba(34, 197, 94, 0.6)`
- Con: `box-shadow: 0 0 40px rgba(239, 68, 68, 0.6)`
- Mod: `box-shadow: 0 0 40px rgba(255, 255, 255, 0.6)`

**Speech Bubbles:**
- Max width: 600px
- Rounded corners: 20px
- Semi-transparent dark background
- Colored borders matching agent theme

**Responsive Design:**
- Breakpoint: 768px
- Smaller avatars on mobile (100px vs 150px)
- Stacked button layout
- Reduced padding

---

#### `frontend/app.js`
**Purpose:** Frontend logic and API communication

**Configuration:**
```javascript
const API_BASE_URL = 'http://localhost:5000';
```

**State Variables:**
```javascript
let sessionId = generateSessionId();
let currentRound = 1;
let totalRounds = 2;
let currentTurn = null;  // 'pro', 'con', or 'moderator'
let debateActive = false;
```

**Key Functions:**

1. **`startDebate()`**
   - Validates question input
   - Sends POST to `/debate/start`
   - Receives Pro's opening argument
   - Hides setup, shows arena
   - Initializes round tracking
   - Displays Pro character

2. **`nextTurn()`**
   - Hides current agent (fade out)
   - Waits 500ms for animation
   - Sends POST to `/debate/next-turn`
   - Receives next agent's response
   - Updates round/progress
   - Displays new agent
   - Checks if debate complete

3. **`showAgent(turn, content)`**
   - Maps turn to character ID
   - Updates speech bubble text
   - Sets display to flex
   - Triggers slide-in animation (50ms delay)
   - **Does NOT hide previous agent** (user controlled)

4. **`hideAllAgents()`**
   - Adds 'fade-out' class to all characters
   - Waits 400ms
   - Sets display to none
   - Removes fade-out class

5. **`addToHistory(agent, content, type)`**
   - Creates history item div
   - Color codes by agent type
   - Truncates to 200 chars for display
   - Appends to history panel
   - Auto-scrolls to bottom

6. **`submitComment()`**
   - Gets comment text
   - Sends POST to `/debate/add-comment`
   - Adds to history as 'user' type
   - Closes modal

7. **`debateComplete()`**
   - Hides Next Turn button
   - Shows New Debate button
   - Displays completion message

8. **`updateProgress()`**
   - Calculates percentage: `(currentRound / totalRounds) * 100`
   - Updates progress bar width

**Event Listeners:**
- Start Debate button click
- Next Turn button click
- Add Comment button click
- Comment modal submit/cancel
- Round selector buttons
- Keyboard support (Enter to submit)

**Session Management:**
```javascript
function generateSessionId() {
    return `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
}
```

**Error Handling:**
- Try-catch on all API calls
- User-friendly error messages
- Console logging for debugging

---

## 🔄 Debate Flow Diagram

```
User Input
    ↓
[Start Debate]
    ↓
Pro Agent (opening) → Display → User reads
    ↓ [Next Turn]
Con Agent (responds to Pro) → Display → User reads
    ↓ [Next Turn]
Moderator (synthesizes) → Display → User reads
    ↓ [Next Turn]
─────── Round 2 ─────────
Pro Agent (continues, addresses Con) → Display
    ↓ [Next Turn]
Con Agent (responds to new Pro points) → Display
    ↓ [Next Turn]
Moderator (synthesizes round 2) → Display
    ↓
[Debate Complete]
```

**User can inject comments at ANY point:**
```
... debate in progress ...
    ↓
[Add Comment] → User types clarification
    ↓
Comment added to history
    ↓
Future agents see comment in context
    ↓
... debate continues ...
```

---

## ⚙️ Configuration & Customization

### Change Number of Rounds
**Frontend HTML:**
```html
<button class="round-btn" data-rounds="1">1 Round</button>
<button class="round-btn" data-rounds="10">10 Rounds</button>
```

### Adjust Response Length
**Agent files:**
```python
# In prompt:
"Keep it concise (150-200 words)"  # Change word count

# In generate call:
max_tokens=1200  # Change token limit
```

### Change Animation Speed
**CSS:**
```css
animation: slideInFromLeft 0.6s ease-out;
                          ^^^^
                          Change duration (0.3s = faster, 1s = slower)
```

### Adjust Rate Limit Delays
**Backend app.py:**
```python
time.sleep(5)  # Change to 3 for faster, 10 for safer
```

### Use Different Gemini Model
**gemini_client.py:**
```python
model_options = [
    'models/gemini-2.5-pro',  # More powerful
    'models/gemini-2.0-flash-lite',  # Faster, cheaper
]
```

### Change Server Port
**Backend app.py:**
```python
app.run(host='0.0.0.0', port=5001, debug=True)
```

**Frontend app.js:**
```javascript
const API_BASE_URL = 'http://localhost:5001';
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)
- Modern web browser
- Gemini API key

### Step-by-Step Setup

1. **Create project structure:**
```bash
mkdir gemini_debate_console
cd gemini_debate_console
mkdir -p backend/agents backend/memory backend/prompts backend/utils frontend
```

2. **Create empty `__init__.py` files:**
```bash
touch backend/agents/__init__.py
touch backend/memory/__init__.py
touch backend/utils/__init__.py
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Create `.env` file:**
```bash
echo "GEMINI_API_KEY=your_api_key_here" > .env
```

5. **Start server:**
```bash
python backend/app.py
```

6. **Open frontend:**
Open `frontend/index.html` in browser
OR navigate to `http://localhost:5000`

---

## 🐛 Common Issues & Solutions

### Issue: "GEMINI_API_KEY not found"
**Solution:** Create `.env` file in project root with valid API key

### Issue: Rate limit errors (429)
**Solution:** 
- Wait 60 seconds between tests
- Increase delays in app.py: `time.sleep(10)`
- Use fail-fast mode: `max_retries=0` in gemini_client.py

### Issue: Responses cut off mid-sentence
**Solution:** Increase `max_tokens` in agent files (currently 1500)

### Issue: Agent images not loading
**Solution:** 
- Check image filenames match exactly
- Ensure images are in frontend folder
- System works without images (shows colored circles)

### Issue: CORS errors
**Solution:** Ensure `flask-cors` installed and `CORS(app)` called

### Issue: Agents not responding to each other
**Solution:** 
- Verify using correct agent files
- Check history is being passed correctly
- Restart server after changes

### Issue: Characters disappear too fast
**Solution:** 
- Check that app.js was updated
- Hard refresh browser (Ctrl+Shift+R)
- Verify `hideAllAgents()` only called on Next Turn

---

## 📊 API Endpoints Reference

### POST `/debate/start`
**Request:**
```json
{
    "question": "Should AI replace artists?",
    "session_id": "session_123",
    "rounds": 3
}
```

**Response:**
```json
{
    "success": true,
    "turn": "pro",
    "round": 1,
    "total_rounds": 3,
    "agent": "Pro Agent",
    "content": "Pro's opening argument...",
    "next_turn": "con",
    "session_id": "session_123"
}
```

### POST `/debate/next-turn`
**Request:**
```json
{
    "session_id": "session_123",
    "current_turn": "pro",
    "current_round": 1,
    "total_rounds": 3
}
```

**Response:**
```json
{
    "success": true,
    "turn": "con",
    "round": 1,
    "total_rounds": 3,
    "agent": "Con Agent",
    "content": "Con's response...",
    "next_turn": "moderator",
    "session_id": "session_123"
}
```

**Final Round Response:**
```json
{
    "success": true,
    "turn": "moderator",
    "round": 3,
    "total_rounds": 3,
    "agent": "Moderator",
    "content": "Final synthesis...",
    "next_turn": "complete",
    "debate_complete": true,
    "session_id": "session_123"
}
```

### POST `/debate/add-comment`
**Request:**
```json
{
    "session_id": "session_123",
    "comment": "What about ethical concerns?"
}
```

**Response:**
```json
{
    "success": true,
    "message": "Comment added to debate history"
}
```

### GET `/history/<session_id>`
**Response:**
```json
{
    "success": true,
    "session_id": "session_123",
    "history": [
        {"role": "user", "content": "...", "timestamp": "..."},
        {"role": "pro", "content": "...", "timestamp": "..."},
        {"role": "con", "content": "...", "timestamp": "..."}
    ]
}
```

### DELETE `/clear/<session_id>`
**Response:**
```json
{
    "success": true,
    "message": "Session session_123 cleared"
}
```

---

## 🎨 Character Image Specifications

### File Requirements
- **Format:** PNG with transparent background
- **Size:** 400x400px minimum (displayed at 150x150px)
- **File size:** Under 200KB each
- **Names:** 
  - `pro_agent.png`
  - `con_agent.png`
  - `moderator_agent.png`

### Design Guidelines

**Pro Agent:**
- Theme: Optimistic, supportive
- Colors: Green (#22c55e)
- Suggestions: Thumbs up, checkmark, friendly robot

**Con Agent:**
- Theme: Critical, analytical
- Colors: Red (#ef4444)
- Suggestions: Arms crossed, X-mark, skeptical expression

**Moderator:**
- Theme: Neutral, balanced
- Colors: White/Gold (#ffffff, #d1af37)
- Suggestions: Scales of justice, wise figure, balanced pose

### AI Generation Prompts

**Pro:**
```
Create a friendly, optimistic AI robot character for debates.
Green color accents (#22c55e). Modern, cute, approachable style.
Confident pose, giving thumbs up. Transparent background, PNG, 512x512px.
```

**Con:**
```
Create a skeptical, analytical AI robot character for debates.
Red color accents (#ef4444). Modern, intelligent, critical thinker.
Arms crossed, thoughtful expression. Transparent background, PNG, 512x512px.
```

**Moderator:**
```
Create a wise, neutral AI robot as a debate moderator.
White/gold colors (#ffffff, #d1af37). Elegant, balanced, authoritative.
Holding scales or open palms. Transparent background, PNG, 512x512px.
```

---

## 🔐 Security Considerations

### API Key Protection
- Never commit `.env` to git
- Add to `.gitignore`:
```
.env
__pycache__/
*.pyc
.DS_Store
```

### Rate Limiting
- Free tier: 5 requests/minute
- Implement delays (currently 5 seconds)
- Consider paid tier for production

### Input Validation
- Backend validates question is not empty
- Frontend prevents empty submissions
- XSS protection via `escapeHtml()` function

### CORS Configuration
- Currently allows all origins: `CORS(app)`
- For production, restrict origins:
```python
CORS(app, origins=['https://yourdomain.com'])
```

---

## 📈 Performance Metrics

### Response Times (Free Tier)
- Pro/Con generation: 3-8 seconds
- Moderator synthesis: 4-10 seconds
- Total debate round: 15-30 seconds (with delays)

### Token Usage Per Debate
- Pro: ~300-500 tokens
- Con: ~300-500 tokens
- Moderator: ~200-400 tokens
- Total: ~800-1400 tokens per round
- 3-round debate: ~2400-4200 tokens

### Rate Limits (Free Tier)
- 5 requests per minute
- 1500 requests per day
- 1 debate = 3 requests minimum
- Max ~30-40 debates per hour (with delays)

---

## 🚀 Future Enhancement Ideas

### Backend Enhancements
1. PostgreSQL database for persistent history
2. User authentication system
3. WebSocket for real-time updates
4. Export debate as PDF/Markdown
5. Multiple debate formats (Oxford, Lincoln-Douglas, etc.)
6. Configurable agent personalities
7. Citation/source tracking

### Frontend Enhancements
1. Dark/light theme toggle
2. Voice synthesis for agent responses
3. Animated avatars (Lottie files)
4. Mobile app version (React Native)
5. Real-time typing indicators
6. Share debate via URL
7. Voting system for "winner"
8. Replay mode for past debates

### AI Enhancements
1. Fact-checking integration
2. Source citation
3. Multi-language support
4. Custom agent personalities
5. Argument quality scoring
6. Logical fallacy detection
7. Evidence strength analysis

---

## 📝 Version History

**v2.0 (Current - Turn-Based Edition)**
- Turn-based debate system
- Animated character appearances
- Agents respond to each other
- User-controlled rounds
- Mid-debate comments
- Visual progress tracking

**v1.0 (Original)**
- All responses at once
- Basic three-panel layout
- No animations
- Static display

---

## 🤝 Contributing Guidelines

### Code Style
- Python: PEP 8
- JavaScript: ES6+
- CSS: BEM methodology recommended
- Comments: Explain "why", not "what"

### Testing Checklist
- [ ] Backend starts without errors
- [ ] Frontend connects to API
- [ ] Pro agent appears from left
- [ ] Con agent responds to Pro
- [ ] Moderator synthesizes correctly
- [ ] Progress bar updates
- [ ] Comments can be added
- [ ] New debate resets state
- [ ] Rate limits handled gracefully
- [ ] Responses are complete (no truncation)

### Pull Request Template
```markdown
## Description
[What changed and why]

## Testing
- [ ] Tested locally
- [ ] All agents working
- [ ] No console errors
- [ ] Animations smooth

## Screenshots
[If UI changes]
```

---

## 📚 Additional Resources

### Documentation
- Gemini API: https://ai.google.dev/docs
- Flask Docs: https://flask.palletsprojects.com/
- CSS Animations: https://developer.mozilla.org/en-US/docs/Web/CSS/animation

### Tools
- API Key: https://makersuite.google.com/app/apikey
- Rate Limit Monitor: https://ai.dev/rate-limit
- Image Compression: https://tinypng.com/

### Community
- Gemini Discord: [Link if available]
- GitHub Issues: [Your repo]
- Stack Overflow: Tag `google-gemini-api`

---

## 📞 Support & Contact

For issues or questions:
1. Check this documentation
2. Review troubleshooting section
3. Check Flask/Gemini logs
4. Open GitHub issue with:
   - Error message
   - Steps to reproduce
   - System info (Python version, OS)

---

**Last Updated:** January 28, 2026
**Documentation Version:** 2.0
**Project Status:** Active Development

---

This documentation should contain everything needed to recreate, understand, and extend the project. Good luck with your migration! 🎭