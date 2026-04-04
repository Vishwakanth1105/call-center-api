# Local Testing Guide

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables
Create a `.env` file (or use the existing one):
```
API_KEY=sk_track3_987654321
GROQ_API_KEY=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
GEMINI_API_KEY=AIzaSyA6nmuCv43jMkSWSb1qngc4yrnMtmY4Mu0
```

### 3. Run the Application
```bash
python app.py
```

The server will start on `http://localhost:5000`

### 4. Test the Health Endpoint
In another terminal:
```bash
curl http://localhost:5000/health
```

Expected response:
```json
{"status": "healthy"}
```

## Testing with Sample Audio

### Method 1: Download Sample Audio Locally

1. **Download the sample audio:**
   - URL: https://recordings.exotel.com/exotelrecordings/guvi64/5780094ea05a75c867120809da9a199f.mp3
   - Save as `sample.mp3` in your project directory

2. **Run the test script:**
```bash
python test_api.py
```

### Method 2: Manual Testing with Python

```python
import requests
import base64

# Read your local audio file
with open('sample.mp3', 'rb') as f:
    audio_base64 = base64.b64encode(f.read()).decode('utf-8')

# Make request
response = requests.post(
    'http://localhost:5000/api/call-analytics',
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

import json
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

### Method 3: Using cURL

```bash
# Encode your audio file
BASE64_AUDIO=$(base64 -w 0 sample.mp3)

# Make request
curl -X POST http://localhost:5000/api/call-analytics \
  -H "Content-Type: application/json" \
  -H "x-api-key: sk_track3_987654321" \
  -d "{
    \"language\": \"Tamil\",
    \"audioFormat\": \"mp3\",
    \"audioBase64\": \"$BASE64_AUDIO\"
  }"
```

## Expected Response Structure

```json
{
  "status": "success",
  "language": "Tamil",
  "transcript": "Agent: Hello? Customer: Yeah, hello...",
  "summary": "An agent from Guvi Institution followed up...",
  "sop_validation": {
    "greeting": true,
    "identification": false,
    "problemStatement": true,
    "solutionOffering": true,
    "closing": true,
    "complianceScore": 0.8,
    "adherenceStatus": "NOT_FOLLOWED",
    "explanation": "The agent did not identify the customer..."
  },
  "analytics": {
    "paymentPreference": "EMI",
    "rejectionReason": "NONE",
    "sentiment": "Positive"
  },
  "keywords": [
    "Guvi Institution",
    "Data Science",
    "Career Change",
    ...
  ]
}
```

## Troubleshooting

### Port Already in Use
```bash
# Kill process on port 5000
lsof -ti:5000 | xargs kill -9

# Or use a different port
PORT=8000 python app.py
```

### API Key Errors
- Verify `.env` file exists
- Check `x-api-key` header is exactly: `sk_track3_987654321`

### Groq/Gemini API Errors
- Verify your API keys are valid
- Check internet connection
- Groq has rate limits (free tier)

### Slow Response
- Audio transcription takes time (5-10 seconds)
- Gemini analysis adds 5-15 seconds
- Total expected time: 15-30 seconds per request

## Testing Without Internet Access

If you can't download the sample audio:
1. Use any MP3 file you have locally
2. The API will process it the same way
3. Change language parameter if needed ("Tamil" or "Hindi")

## Production Testing

Before deploying, verify:
- ✅ Health endpoint responds
- ✅ 401 error for missing API key
- ✅ Valid response structure
- ✅ All required fields present
- ✅ SOP validation logic works
- ✅ Payment/rejection classification accurate
- ✅ Keywords extraction functional
