# 🚦 Rate Limiting Solution for Free Tier

## The Problem
Gemini API free tier limits:
- **5 requests per minute** per model
- Each debate = 3 API calls (Pro + Con + Moderator)
- Error 429: "You exceeded your current quota"

## ✅ Solution Implemented

### Option 1: Use Updated app.py (RECOMMENDED)
I've created `app_with_rate_limiting.py` that automatically:
- Adds 5-second delays between each agent call
- Handles retry logic with exponential backoff
- Shows clear progress messages

**To use:**
```bash
# Replace your app.py or run this version directly:
python backend/app_with_rate_limiting.py
```

**Expected behavior:**
- Each debate takes ~15-20 seconds total
- You'll see: "⏳ Waiting 5 seconds to respect rate limits..."
- Automatic retries if rate limit hit

### Option 2: Update gemini_client.py Only
Replace `backend/utils/gemini_client.py` with the new version that includes:
- Automatic retry logic
- Extracts wait time from error messages
- Up to 3 retry attempts with delays

## 📊 Rate Limit Details

### Free Tier Limits:
```
Model: gemini-2.5-flash
Limit: 5 requests per minute
Window: Rolling 60-second window
```

### Your Usage:
```
1 debate = 3 requests
Max debates per minute: 1 (with delays)
Max debates per hour: ~30-40
```

## 🎯 Best Practices

1. **Add delays between requests** (5 seconds minimum)
2. **Wait 60 seconds** between debates if you hit the limit
3. **Use the retry logic** - it automatically waits the required time
4. **Monitor usage** at: https://ai.dev/rate-limit

## 💰 Upgrade Options

To remove rate limits, upgrade your API plan:
- **Pay-as-you-go**: $0.075 per 1M tokens
- **Higher limits**: 360 requests per minute
- **Visit**: https://ai.google.dev/pricing

## 🔧 Quick Fixes

### If you still hit rate limits:

1. **Increase delays in app.py:**
```python
time.sleep(10)  # Change from 5 to 10 seconds
```

2. **Reduce max_retries:**
```python
response = self.client.generate(
    prompt=full_prompt,
    max_tokens=500,
    temperature=0.8,
    max_retries=1  # Fail faster instead of waiting
)
```

3. **Switch to a different model:**
```python
# In gemini_client.py, try:
model_options = [
    'models/gemini-2.0-flash',  # Might have separate quota
    'models/gemini-flash-lite-latest',  # Lighter model
]
```

## 📝 Testing

After applying the fix:

1. **Start the server:**
```bash
python backend/app_with_rate_limiting.py
```

2. **Watch the console** - you should see:
```
🟢 Calling Pro Agent...
✓ Pro Agent responded (247 chars)

⏳ Waiting 5 seconds to respect rate limits...

🔴 Calling Con Agent...
✓ Con Agent responded (263 chars)

⏳ Waiting 5 seconds to respect rate limits...

⚖️  Calling Moderator Agent...
✓ Moderator responded (312 chars)

✅ Debate completed successfully
```

3. **Total time:** ~15-20 seconds per debate

## ❓ Still Having Issues?

**Wait a full minute** before trying again. The rate limit is a rolling window, so:
- If you made 5 requests at 12:00:00
- You can make another request at 12:01:01
- The window resets continuously

**Check your quota:**
Visit https://ai.dev/rate-limit to see your current usage.