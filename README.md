# 🤖 Gemini Multi-Agent Debate Console

A sophisticated web application that simulates structured debates using three specialized AI agents powered by Google's Gemini API.

## 🎯 Overview

The Gemini Multi-Agent Debate Console demonstrates agentic AI reasoning through role specialization and structured collaboration:

- **Pro Agent** - Constructs compelling arguments in favor of any proposition
- **Con Agent** - Develops strong counterarguments and identifies risks
- **Moderator Agent** - Synthesizes both perspectives into balanced analysis

## ✨ Features

- 🎭 **Three Specialized AI Agents** - Each with distinct roles and reasoning patterns
- 💬 **Multi-turn Conversations** - Session memory enables follow-up questions
- 🎨 **Professional UI** - Clean, responsive interface with smooth animations
- ⚡ **Real-time Processing** - Instant feedback with loading states
- 🔄 **Session Management** - Maintains conversation context across exchanges
- 🌐 **RESTful API** - Clean backend architecture for easy integration

## 🏗 Architecture

```
Browser (HTML/CSS/JS)
        ↓ HTTP POST
Python Backend (Flask)
        ↓
Agent Controller
 ├── Pro Agent (Gemini API)
 ├── Con Agent (Gemini API)
 └── Moderator Agent (Gemini API)
        ↓
Response JSON → Frontend Panels
```

## 📁 Project Structure

```
gemini_debate_console/
│
├── backend/
│   ├── app.py                      # Flask server & routes
│   ├── agents/
│   │   ├── pro_agent.py           # Pro argument agent
│   │   ├── con_agent.py           # Con argument agent
│   │   └── moderator_agent.py     # Synthesis agent
│   ├── prompts/
│   │   ├── pro_prompt.txt         # Pro agent instructions
│   │   ├── con_prompt.txt         # Con agent instructions
│   │   └── moderator_prompt.txt   # Moderator instructions
│   ├── utils/
│   │   └── gemini_client.py       # Gemini API wrapper
│   └── memory/
│       └── session_store.py       # Conversation history
│
├── frontend/
│   ├── index.html                 # Main UI
│   ├── styles.css                 # Styling
│   └── app.js                     # Frontend logic
│
├── .env                           # API key (create this)
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))
- Modern web browser

### Installation

1. **Clone or download the project**

```bash
cd gemini_debate_console
```

2. **Set up Python environment**

```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure API key**

Create a `.env` file in the project root:

```bash
GEMINI_API_KEY=your_actual_api_key_here
```

⚠️ **Important**: Replace `your_actual_api_key_here` with your real Gemini API key

### Running the Application

1. **Start the backend server**

```bash
python backend/app.py
```

You should see:
```
Gemini Multi-Agent Debate Console
============================================================
API Key Status: ✓ Loaded
Server starting on http://localhost:5000
============================================================
```

2. **Open the frontend**

Simply open `frontend/index.html` in your web browser, or navigate to:
```
http://localhost:5000
```

## 💡 Usage

### Basic Debate Flow

1. **Enter a question or proposition** in the text area
   - Example: "Should AI replace junior developers?"
   - Example: "Is remote work better than office work?"

2. **Click "Start Debate"** to initiate the discussion

3. **Review the three perspectives:**
   - ✅ **Pro Agent** presents arguments in favor
   - ❌ **Con Agent** presents arguments against
   - ⚖️ **Moderator** provides balanced synthesis

4. **Ask follow-up questions** to dive deeper
   - Example: "What about the ethical implications?"
   - Example: "How does this affect small businesses?"

### Example Questions

- "Should we implement a 4-day work week?"
- "Is nuclear energy the solution to climate change?"
- "Should social media be regulated by governments?"
- "Will quantum computing make current encryption obsolete?"
- "Should we colonize Mars?"

## 🔧 API Endpoints

### POST `/debate`
Initiate or continue a debate

**Request:**
```json
{
  "question": "Should AI replace junior developers?",
  "session_id": "session_123"
}
```

**Response:**
```json
{
  "success": true,
  "pro": "Pro agent's argument...",
  "con": "Con agent's argument...",
  "moderator": "Moderator's synthesis...",
  "session_id": "session_123"
}
```

### GET `/history/<session_id>`
Retrieve conversation history

### DELETE `/clear/<session_id>`
Clear session history

### GET `/sessions`
List all active sessions

## ⚙️ Configuration

### Changing the AI Model

Edit `backend/utils/gemini_client.py`:

```python
# For faster responses (default):
self.model_name = 'gemini-1.5-flash'

# For more complex reasoning:
self.model_name = 'gemini-1.5-pro'
```

### Adjusting Response Length

Edit agent files in `backend/agents/`:

```python
response = self.client.generate(
    prompt=full_prompt,
    max_tokens=500,  # Adjust this value
    temperature=0.8   # Adjust randomness (0.0-1.0)
)
```

### Customizing Agent Behavior

Edit the prompt files in `backend/prompts/`:
- `pro_prompt.txt` - Modify pro agent's reasoning style
- `con_prompt.txt` - Modify con agent's reasoning style  
- `moderator_prompt.txt` - Modify synthesis approach

## 🎨 Customizing the UI

The frontend styling can be customized in `frontend/styles.css`:

- **Colors**: Search for color values (e.g., `#D3AF37` for gold)
- **Fonts**: Modify `font-family` properties
- **Layout**: Adjust padding, margins, and flex properties
- **Animations**: Edit keyframe animations at the bottom

## 🐛 Troubleshooting

### "GEMINI_API_KEY not found"
- Ensure `.env` file exists in project root
- Verify the API key is correct
- Check that `python-dotenv` is installed

### "Connection refused" errors
- Verify backend server is running on port 5000
- Check if another application is using port 5000
- Try accessing http://localhost:5000 directly

### CORS errors
- Ensure `flask-cors` is installed
- Check that `CORS(app)` is called in `app.py`

### Slow responses
- Consider switching to `gemini-1.5-flash` for faster responses
- Reduce `max_tokens` in agent files
- Check your internet connection

### API quota exceeded
- Gemini API has rate limits
- Wait a few minutes before retrying
- Consider upgrading your API tier

## 📊 Performance

- **Average response time**: 3-8 seconds for complete debate
- **Concurrent sessions**: Supports multiple simultaneous users
- **Memory usage**: ~50-100MB for typical usage
- **API calls per debate**: 3 calls (one per agent)

## 🔒 Security Notes

- Never commit your `.env` file with real API keys
- Use environment variables in production
- Consider rate limiting for public deployments
- Sanitize user inputs before processing

## 🚢 Deployment

For production deployment:

1. Use a production WSGI server (e.g., Gunicorn)
2. Set up proper environment variables
3. Enable HTTPS
4. Configure rate limiting
5. Add authentication if needed

Example with Gunicorn:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 backend.app:app
```

## 🛠 Tech Stack

**Backend:**
- Python 3.10+
- Flask (web framework)
- Google Generative AI SDK
- python-dotenv (environment management)

**Frontend:**
- HTML5
- CSS3 (Flexbox, animations)
- Vanilla JavaScript (ES6+)
- Fetch API

**AI:**
- Google Gemini 1.5 Flash/Pro

## 📝 License

This project is provided as-is for educational and demonstration purposes.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation

## 📧 Support

For issues or questions:
1. Check the troubleshooting section
2. Review API documentation: https://ai.google.dev/docs
3. Open an issue on the project repository

## 🎓 Learning Resources

- [Gemini API Documentation](https://ai.google.dev/docs)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Python asyncio Guide](https://docs.python.org/3/library/asyncio.html)

## 🙏 Acknowledgments

- Google Gemini team for the powerful API
- Flask community for the excellent web framework
- All contributors and testers

---

**Built using Gemini API**

*Last updated: January 2026*