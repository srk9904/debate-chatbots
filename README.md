# 🎭 Gemini Multi-Agent Debate Arena

![Version](https://img.shields.io/badge/version-3.1-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

A dynamic web-based debate system where three AI agents (Pro, Con, Moderator) engage in structured debates on any topic using Google's Gemini API. Features turn-based rounds, animated character appearances, and real-time user interaction.

![Debate Arena Demo](https://via.placeholder.com/800x400.png?text=Gemini+Debate+Arena)

## ✨ Features

### 🤖 Three Specialized AI Agents
- **Pro Agent**: Argues in favor of the proposition with supporting evidence
- **Con Agent**: Challenges arguments with counterpoints and critiques
- **Moderator**: Provides balanced synthesis and identifies key tensions

### 🎬 Dynamic Presentation
- **Animated Entrances**: Pro slides in from left, Con from right, Moderator from top
- **Turn-Based Flow**: User-controlled progression through each argument
- **Visual Progress**: Round indicator and progress bar tracking
- **Smart Formatting**: Automatic bullet points for long responses, paragraphs for short ones

### 💡 Enhanced User Experience
- **Configurable Rounds**: Choose 1-5 debate rounds
- **Mid-Debate Comments**: Add clarifications or questions anytime
- **Continue Feature**: Extend debates with additional rounds
- **Expandable History**: Click any history item to see full response
- **Dynamic Sizing**: Speech bubbles adjust to content length
- **Responsive Design**: Works on desktop, tablet, and mobile

### 🚀 Performance Optimized
- **Single API Call Per Round**: All three agents respond in one request
- **Rate Limit Friendly**: Built-in delays and retry logic
- **Session Memory**: Maintains conversation context across rounds
- **Mock Mode**: Test without API calls

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
- [Customization](#customization)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## 🔧 Prerequisites

- **Python**: 3.10 or higher
- **pip**: Python package manager
- **Gemini API Key**: Get one free at [Google AI Studio](https://makersuite.google.com/app/apikey)
- **Modern Browser**: Chrome, Firefox, Safari, or Edge

### Rate Limits (Free Tier)
- 15 requests per minute
- 1500 requests per day
- Each debate round = 1 API call (3 responses)

## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/gemini-debate-arena.git
cd gemini-debate-arena
```

### 2. Create Project Structure

```bash
# Create necessary directories
mkdir -p backend/agents backend/memory backend/utils frontend
```

### 3. Create Required Files

Create empty `__init__.py` files to make directories Python packages:

```bash
touch backend/agents/__init__.py
touch backend/memory/__init__.py
touch backend/utils/__init__.py
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

**requirements.txt:**
```txt
flask==3.0.0
flask-cors==4.0.0
google-generativeai==0.3.2
python-dotenv==1.0.0
```

### 5. Set Up Environment Variables

Create a `.env` file in the project root:

```bash
echo "GEMINI_API_KEY=your_actual_api_key_here" > .env
```

**Important**: Never commit `.env` to version control!

### 6. Add to .gitignore

Create or update `.gitignore`:

```bash
cat > .gitignore << 'EOF'
# Environment
.env
*.env

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
*.log
EOF
```

## ⚙️ Configuration

### Get Your Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Get API Key"
4. Copy your key and add it to `.env`

### Update API Base URL

If running on a different port or host, update `frontend/app.js`:

```javascript
const API_BASE_URL = 'http://localhost:5000';  // Change port if needed
```

## 🚀 Usage

### 1. Start the Backend Server

```bash
python backend/app.py
```

You should see:
```
🎭 Gemini Multi-Agent Debate Console v3.1
============================================================
API Key: ✓ Loaded
...
Server: http://localhost:5000
```

### 2. Open the Frontend

**Option A**: Direct file access
```bash
# Open in default browser
open frontend/index.html  # macOS
xdg-open frontend/index.html  # Linux
start frontend/index.html  # Windows
```

**Option B**: Serve via Flask (recommended)
```bash
# Frontend is automatically served at http://localhost:5000
# Just navigate to http://localhost:5000 in your browser
```

### 3. Start a Debate

1. Enter a debate topic (e.g., "Should AI replace human artists?")
2. Select number of rounds (1-5)
3. Click "⚔️ Start Debate"
4. Watch as Pro, Con, and Moderator present their arguments
5. Click "▶️ Next Turn" to advance through each agent
6. Add comments or continue the debate when complete

## 📁 Project Structure

```
gemini-debate-arena/
│
├── .env                          # API key (DO NOT COMMIT)
├── .gitignore                    # Git ignore rules
├── requirements.txt              # Python dependencies
├── README.md                     # This file
├── IMPROVEMENTS.md              # Version 3.1 changelog
│
├── backend/
│   ├── app.py                   # Main Flask server
│   │
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── pro_agent.py         # Pro argument generator
│   │   ├── con_agent.py         # Con argument generator
│   │   └── moderator_agent.py   # Moderator synthesis
│   │
│   ├── memory/
│   │   ├── __init__.py
│   │   └── session_store.py     # Conversation history
│   │
│   └── utils/
│       ├── __init__.py
│       └── gemini_client.py     # Gemini API wrapper
│
└── frontend/
    ├── index.html               # Main UI
    ├── styles.css               # Styling & animations
    ├── app.js                   # Frontend logic
    ├── pro_agent.png            # Optional: Pro avatar
    ├── con_agent.png            # Optional: Con avatar
    └── moderator_agent.png      # Optional: Moderator avatar
```

## 🔌 API Endpoints

### POST `/debate/start`
Start a new debate

**Request:**
```json
{
    "question": "Should AI replace human artists?",
    "session_id": "session_abc123",
    "rounds": 3
}
```

**Response:**
```json
{
    "success": true,
    "round": 1,
    "total_rounds": 3,
    "responses": {
        "pro": "Pro's argument...",
        "con": "Con's argument...",
        "moderator": "Moderator's synthesis..."
    },
    "session_id": "session_abc123"
}
```

### POST `/debate/next-round`
Get next round responses

**Request:**
```json
{
    "session_id": "session_abc123",
    "current_round": 1,
    "total_rounds": 3
}
```

### POST `/debate/add-comment`
Add user comment mid-debate

**Request:**
```json
{
    "session_id": "session_abc123",
    "comment": "What about ethical concerns?"
}
```

### GET `/history/<session_id>`
Retrieve debate history

### DELETE `/clear/<session_id>`
Clear session data

## 🎨 Customization

### Adjust Response Length

Edit `backend/app.py` prompts:

```python
# Change word limits
- Keep TOTAL response under 250 words  # Change to 150, 300, etc.
```

### Change Animation Speed

Edit `frontend/styles.css`:

```css
.pro-character.active {
    animation: slideInFromLeft 0.6s ease-out;
    /* Change 0.6s to 0.3s (faster) or 1s (slower) */
}
```

### Customize Colors

Edit `frontend/styles.css` color variables:

```css
/* Pro: Green */
#22c55e → your color

/* Con: Red */
#ef4444 → your color

/* Moderator: Gold */
#d1af37 → your color
```

### Add Custom Avatars

Replace placeholder images in `frontend/`:
- `pro_agent.png` (150x150px minimum)
- `con_agent.png` (150x150px minimum)
- `moderator_agent.png` (150x150px minimum)

## 🐛 Troubleshooting

### Issue: "GEMINI_API_KEY not found"
**Solution**: Create `.env` file in project root with valid API key

### Issue: Rate limit errors (429)
**Solution**: 
- Wait 60 seconds between tests
- Free tier: 15 requests/minute
- Consider upgrading to paid tier

### Issue: Responses cut off mid-sentence
**Solution**: Increase `max_tokens` in `backend/app.py` (currently 3000)

### Issue: CORS errors
**Solution**: 
- Ensure `flask-cors` is installed
- Check `CORS(app)` is called in `app.py`

### Issue: Agents not responding to each other
**Solution**: 
- Verify using correct agent files from this repo
- Restart server after changes
- Clear browser cache (Ctrl+Shift+R)

### Issue: Frontend can't connect to backend
**Solution**:
- Check backend is running on port 5000
- Verify `API_BASE_URL` in `app.js` matches server
- Check browser console for errors

## 🔄 Git Commands Reference

### Initial Setup (First Time)

```bash
# Initialize git repository
git init

# Add all files
git add .

# First commit
git commit -m "Initial commit: Gemini Debate Arena v3.1"

# Link to GitHub repository
git remote add origin https://github.com/yourusername/gemini-debate-arena.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Pushing to Existing Repository

```bash
# Check status
git status

# Add modified files
git add .

# Commit changes
git commit -m "Add improvements: dynamic sizing and expandable history"

# Push to GitHub
git push origin main
```

### Common Git Commands

```bash
# See what changed
git status
git diff

# Add specific files
git add backend/app.py
git add frontend/styles.css

# Commit with message
git commit -m "Your descriptive message"

# Push changes
git push

# Pull latest changes
git pull

# View commit history
git log --oneline

# Create a new branch
git checkout -b feature/new-feature

# Switch branches
git checkout main
```

## 📊 Version History

### v3.1 (Current - February 2026)
- ✨ Smart formatting: automatic bullet points for long responses
- 🔄 Dynamic speech bubble sizing
- 📜 Expandable history items (click to see full text)
- 🎯 Enforced word limits for conciseness
- 🐛 Fixed overflow issues

### v3.0 (January 2026)
- 🚀 Single API call per round (3x fewer requests)
- 🔄 Continue debate feature
- 💬 Mid-debate comments
- 📊 Better history tracking

### v2.0 (January 2026)
- 🎬 Turn-based debate system
- ✨ Animated character appearances
- 🗣️ Agents respond to each other
- 🎮 User-controlled progression

### v1.0 (Initial)
- ⚙️ Basic three-agent system
- 📝 Simple debate interface
- 🔌 Gemini API integration

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 for Python code
- Use ES6+ for JavaScript
- Comment complex logic
- Test before submitting PR
- Update README for new features


## 🙏 Acknowledgments

- **JumpStartNinjas LLP**: Providing resources, guidance, and development support
- **Google Gemini API**: Powers the AI agents
- **Flask**: Web framework
- **Community Contributors**: Thanks to everyone who has contributed!

---

**Made using Google Gemini**

*Last Updated: February 2026*