# 🚀 QUICK START GUIDE

## What You Have

A complete **Call Center Compliance API** built with:
- **Flask** (Python web framework)
- **Groq Whisper API** (Speech-to-Text transcription)
- **Google Gemini 1.5 Flash** (AI analysis for SOP validation & analytics)
- **Production-ready** with Gunicorn + Render deployment

## 📁 Project Structure

```
call-center-api/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (LOCAL ONLY - DO NOT COMMIT)
├── .env.example               # Template for environment variables
├── .gitignore                 # Git ignore file
├── render.yaml                # Render deployment configuration
├── README.md                  # Main documentation
├── DEPLOYMENT.md              # Deployment guide for Render
├── LOCAL_TESTING.md           # Local testing instructions
├── SUBMISSION_CHECKLIST.md    # Pre-submission checklist
├── test_api.py                # API testing script
└── prepare_test_data.py       # Helper to download sample audio
```

## ⚡ 3-Step Deployment

### Step 1: Push to GitHub (5 minutes)

```bash
cd call-center-api

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Call Center Compliance API for GUVI Hackathon"

# Create GitHub repo (do this on github.com first), then:
git remote add origin https://github.com/YOUR_USERNAME/call-center-compliance-api.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy to Render (10 minutes)

1. Go to **[render.com](https://render.com)** → Sign up/Login
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure:
   - **Name**: `call-center-compliance-api`
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120`
5. Add Environment Variables:
   - `API_KEY` = `sk_track3_987654321`
   - `GROQ_API_KEY` = `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`
   - `GEMINI_API_KEY` = `AIzaSyA6nmuCv43jMkSWSb1qngc4yrnMtmY4Mu0`
6. Click **"Create Web Service"**

Wait 3-5 minutes for deployment to complete.

### Step 3: Test Your API (5 minutes)

```bash
# Health check
curl https://your-app-name.onrender.com/health

# Response: {"status":"healthy"}
```

**Your API is now live! 🎉**

## 🧪 Testing with Sample Audio

### Download Sample Audio First
1. Download from: https://recordings.exotel.com/exotelrecordings/guvi64/5780094ea05a75c867120809da9a199f.mp3
2. Save as `sample.mp3`

### Test Using Python

```python
import requests
import base64

# Encode audio
with open('sample.mp3', 'rb') as f:
    audio_base64 = base64.b64encode(f.read()).decode('utf-8')

# Make request
response = requests.post(
    'https://your-app-name.onrender.com/api/call-analytics',
    headers={
        'Content-Type': 'application/json',
        'x-api-key': 'sk_track3_987654321'
    },
    json={
        'language': 'Tamil',
        'audioFormat': 'mp3',
        'audioBase64': audio_base64
    },
    timeout=60
)

print(response.json())
```

## 📊 Expected Response

```json
{
  "status": "success",
  "language": "Tamil",
  "transcript": "Full conversation transcript...",
  "summary": "Concise summary of the call...",
  "sop_validation": {
    "greeting": true,
    "identification": false,
    "problemStatement": true,
    "solutionOffering": true,
    "closing": true,
    "complianceScore": 0.8,
    "adherenceStatus": "NOT_FOLLOWED",
    "explanation": "Agent did not identify customer..."
  },
  "analytics": {
    "paymentPreference": "EMI",
    "rejectionReason": "NONE",
    "sentiment": "Positive"
  },
  "keywords": ["Guvi", "Data Science", "Career Change", ...]
}
```

## 🎯 For Hackathon Submission

**Submit These:**
1. **GitHub URL**: `https://github.com/YOUR_USERNAME/call-center-compliance-api`
2. **Live API Endpoint**: `https://your-app-name.onrender.com/api/call-analytics`
3. **API Key**: `sk_track3_987654321` (in header: `x-api-key`)

## ⚠️ Important Notes

### Free Tier Limitations
- Render free tier sleeps after 15 minutes of inactivity
- First request after sleep takes 30-60 seconds to wake up
- For hackathon evaluation, keep it alive by pinging every 10 minutes

### Keep API Alive
Use [UptimeRobot](https://uptimerobot.com/) or [Cron-job.org](https://cron-job.org/):
- Monitor URL: `https://your-app-name.onrender.com/health`
- Interval: Every 10 minutes

### Response Time
- Normal: 15-30 seconds (Groq transcription + Gemini analysis)
- If timeout occurs, increase timeout in your test script to 60-120 seconds

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| **502 Bad Gateway** | Check Render logs, verify env variables |
| **401 Unauthorized** | Verify `x-api-key` header is exactly `sk_track3_987654321` |
| **Empty transcript** | Check audio file is valid MP3, not corrupted |
| **Timeout** | Increase timeout to 60+ seconds |
| **API sleeping** | Set up UptimeRobot to ping every 10 minutes |

## 📚 Documentation Files

- **README.md** - Main project documentation
- **DEPLOYMENT.md** - Detailed Render deployment guide
- **LOCAL_TESTING.md** - How to test locally
- **SUBMISSION_CHECKLIST.md** - Pre-submission validation

## 🏆 Scoring Criteria

| Component | Points | What It Tests |
|-----------|--------|---------------|
| API Availability | 20/test | Endpoint responds with valid JSON |
| Transcript/Summary | 30/test | Accurate transcription & summary |
| SOP Validation | 30/test | Correct compliance detection |
| Analytics | 10/test | Payment/rejection classification |
| Keywords | 10/test | Relevant keyword extraction |
| **Code Quality** | **10** | Clean code, error handling, docs |

**Total: 100 points (10 test cases × 10 pts each = 90, + 10 code quality)**

## 🔑 Your API Keys (Already Set)

```
GROQ_API_KEY: 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
GEMINI_API_KEY: AIzaSyA6nmuCv43jMkSWSb1qngc4yrnMtmY4Mu0
API_KEY: sk_track3_987654321
```

## ✅ Final Checklist

Before submission, verify:
- [ ] GitHub repository is public
- [ ] API is deployed and accessible
- [ ] Health endpoint works
- [ ] Test with sample audio successful
- [ ] All response fields match requirements exactly
- [ ] README.md is comprehensive
- [ ] No API keys in committed code (they're in .gitignore)

---

**You're ready to deploy! Good luck with the hackathon! 🚀**

Need help? Check:
1. DEPLOYMENT.md for detailed deployment steps
2. LOCAL_TESTING.md for local testing
3. SUBMISSION_CHECKLIST.md for final validation
