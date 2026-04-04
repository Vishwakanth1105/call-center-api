# Deployment Guide - Render

## Step 1: Prepare Your GitHub Repository

1. **Create a new GitHub repository** (e.g., `call-center-compliance-api`)

2. **Push your code:**
```bash
cd call-center-api
git init
git add .
git commit -m "Initial commit: Call Center Compliance API"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/call-center-compliance-api.git
git push -u origin main
```

## Step 2: Deploy to Render

### Option A: Using render.yaml (Recommended)

1. Go to [render.com](https://render.com) and sign up/login
2. Click **"New +"** → **"Blueprint"**
3. Connect your GitHub repository
4. Render will automatically detect `render.yaml`
5. Set the secret environment variables:
   - `GROQ_API_KEY`: `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`
   - `GEMINI_API_KEY`: `AIzaSyA6nmuCv43jMkSWSb1qngc4yrnMtmY4Mu0`
6. Click **"Apply"**

### Option B: Manual Setup

1. Go to [render.com](https://render.com) and sign up/login
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: `call-center-compliance-api`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120`
5. Add environment variables:
   - `API_KEY`: `sk_track3_987654321`
   - `GROQ_API_KEY`: `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`
   - `GEMINI_API_KEY`: `AIzaSyA6nmuCv43jMkSWSb1qngc4yrnMtmY4Mu0`
6. Click **"Create Web Service"**

## Step 3: Wait for Deployment

Render will:
1. Clone your repository
2. Install dependencies
3. Start your application
4. Provide you with a live URL (e.g., `https://call-center-compliance-api.onrender.com`)

## Step 4: Test Your Deployed API

### Health Check
```bash
curl https://your-app.onrender.com/health
```

Expected response:
```json
{"status": "healthy"}
```

### Test with Sample Audio

You'll need to:
1. Download the sample audio file locally
2. Convert to Base64
3. Make a POST request

**Using Python:**
```python
import requests
import base64

# Read your local audio file
with open('sample.mp3', 'rb') as f:
    audio_base64 = base64.b64encode(f.read()).decode('utf-8')

# Make request
response = requests.post(
    'https://your-app.onrender.com/api/call-analytics',
    headers={
        'Content-Type': 'application/json',
        'x-api-key': 'sk_track3_987654321'
    },
    json={
        'language': 'Tamil',
        'audioFormat': 'mp3',
        'audioBase64': audio_base64
    }
)

print(response.json())
```

**Using cURL:**
```bash
# First, encode your audio file
BASE64_AUDIO=$(base64 -w 0 sample.mp3)

# Make request
curl -X POST https://your-app.onrender.com/api/call-analytics \
  -H "Content-Type: application/json" \
  -H "x-api-key: sk_track3_987654321" \
  -d "{
    \"language\": \"Tamil\",
    \"audioFormat\": \"mp3\",
    \"audioBase64\": \"$BASE64_AUDIO\"
  }"
```

## Important Notes

### Free Tier Limitations
- Render's free tier spins down after 15 minutes of inactivity
- First request after spin-down may take 30-60 seconds
- For hackathon judging, consider pinging your endpoint every 10 minutes

### Keep Your API Alive (Optional)
Use a service like **UptimeRobot** or **Cron-job.org** to ping your `/health` endpoint every 10 minutes:
```
https://your-app.onrender.com/health
```

### Monitoring Logs
View real-time logs in Render dashboard:
1. Go to your service
2. Click **"Logs"** tab
3. Monitor for any errors

## Troubleshooting

### 502 Bad Gateway
- Application crashed or failed to start
- Check logs for Python errors
- Verify all environment variables are set

### 401 Unauthorized
- API key mismatch
- Verify `x-api-key` header is correct

### Slow Response
- Groq/Gemini API calls take time
- Normal response time: 10-30 seconds
- Increase timeout if needed

### Out of Memory
- Free tier has limited RAM
- Consider upgrading to paid tier if needed
- Optimize code to reduce memory usage

## Testing for Hackathon Submission

When submitting your API URL to GUVI:
1. Ensure your service is running (not spun down)
2. Test with the sample audio first
3. Verify all required fields in response
4. Submit URL: `https://your-app.onrender.com/api/call-analytics`

## API Endpoint for Submission
```
POST https://your-app.onrender.com/api/call-analytics
Header: x-api-key: sk_track3_987654321
```

Good luck with your hackathon! 🚀
