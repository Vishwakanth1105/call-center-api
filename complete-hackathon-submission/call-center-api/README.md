# Call Center Compliance API

## Description
AI-powered API for analyzing call center recordings to ensure SOP compliance, extract business intelligence, and generate actionable insights. Built for GUVI Hackathon 2026 - Track 3: Call Center Compliance.

## Features
- **Speech-to-Text Transcription**: Converts Tamil/Hindi audio to text using Groq Whisper API
- **SOP Validation**: Analyzes adherence to standard call scripts (Greeting → Identification → Problem Statement → Solution → Closing)
- **Payment Classification**: Categorizes payment preferences (EMI, FULL_PAYMENT, PARTIAL_PAYMENT, DOWN_PAYMENT)
- **Rejection Analysis**: Identifies reasons for incomplete transactions
- **Sentiment Analysis**: Detects customer sentiment (Positive, Neutral, Negative)
- **Keyword Extraction**: Extracts relevant keywords for business intelligence
- **API Key Authentication**: Secure endpoint with mandatory API key validation

## Tech Stack
- **Framework**: Flask (Python 3.10+)
- **Speech-to-Text**: Groq Whisper API (whisper-large-v3)
- **NLP Analysis**: Google Gemini 1.5 Flash
- **Deployment**: Render (Production-ready with Gunicorn)

## Architecture
```
Audio (Base64) → Groq Whisper → Transcript → Gemini AI → Analysis → JSON Response
```

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd call-center-api
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Environment Variables
Copy `.env.example` to `.env` and fill in your API keys:
```bash
cp .env.example .env
```

Edit `.env`:
```
API_KEY=sk_track3_987654321
GROQ_API_KEY=your_groq_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
PORT=5000
```

### 4. Run the Application

**Development Mode:**
```bash
python app.py
```

**Production Mode (with Gunicorn):**
```bash
gunicorn app:app --bind 0.0.0.0:5000
```

### 5. Test the API
```bash
python test_api.py
```

## API Documentation

### Endpoint
```
POST /api/call-analytics
```

### Authentication
Include API key in request header:
```
x-api-key: sk_track3_987654321
```

### Request Body
```json
{
  "language": "Tamil",
  "audioFormat": "mp3",
  "audioBase64": "SUQzBAAAAAAAI1RTU0UAAAAPAAADTGF2ZjU2LjM2LjEwMAAAAAAA..."
}
```

### Response Structure
```json
{
  "status": "success",
  "language": "Tamil",
  "transcript": "Full transcription...",
  "summary": "Concise summary of conversation",
  "sop_validation": {
    "greeting": true,
    "identification": false,
    "problemStatement": true,
    "solutionOffering": true,
    "closing": true,
    "complianceScore": 0.8,
    "adherenceStatus": "NOT_FOLLOWED",
    "explanation": "Agent did not identify the customer"
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
    "EMI options",
    "Portfolio"
  ]
}
```

### Error Responses

**401 Unauthorized** (Missing or invalid API key):
```json
{
  "error": "Unauthorized"
}
```

**400 Bad Request** (Missing required fields):
```json
{
  "error": "Missing audioBase64 field"
}
```

**500 Internal Server Error**:
```json
{
  "status": "error",
  "error": "Detailed error message"
}
```

## cURL Example
```bash
curl -X POST https://your-domain.com/api/call-analytics \
  -H "Content-Type: application/json" \
  -H "x-api-key: sk_track3_987654321" \
  -d '{
    "language": "Tamil",
    "audioFormat": "mp3",
    "audioBase64": "SUQzBAAAAAAAI1RTU0U..."
  }'
```

## Approach

### 1. **Audio Transcription Pipeline**
- Receive Base64-encoded MP3 audio
- Decode and save to temporary file
- Process using Groq Whisper API with language detection
- Return accurate Tamil/Hindi transcription

### 2. **AI-Powered Analysis**
- Use Google Gemini 1.5 Flash for structured analysis
- Prompt engineering ensures consistent JSON output
- Multi-stage validation for SOP compliance
- Contextual extraction of payment preferences and rejection reasons

### 3. **SOP Compliance Scoring**
- Binary validation for 5 key stages: greeting, identification, problemStatement, solutionOffering, closing
- Compliance score = (true_count / 5)
- Adherence status: "FOLLOWED" (all 5 true) or "NOT_FOLLOWED"

### 4. **Business Analytics Extraction**
- Payment preference classification using enum validation
- Rejection reason analysis with contextual understanding
- Sentiment analysis for customer experience tracking

### 5. **Keyword Intelligence**
- Extract 10-15 relevant keywords from conversation
- Focus on products, services, concerns, and key discussion points

## Deployment on Render

### 1. Create `render.yaml` (optional, for automatic deployment)
```yaml
services:
  - type: web
    name: call-center-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app
    envVars:
      - key: API_KEY
        value: sk_track3_987654321
      - key: GROQ_API_KEY
        sync: false
      - key: GEMINI_API_KEY
        sync: false
```

### 2. Manual Deployment Steps
1. Create new Web Service on Render
2. Connect your GitHub repository
3. Configure:
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
4. Add environment variables in Render dashboard:
   - `API_KEY`
   - `GROQ_API_KEY`
   - `GEMINI_API_KEY`
5. Deploy!

## Evaluation Criteria

### API Functionality (90 points)
- **Response Structure** (20 pts): All required fields present
- **Transcript & Summary** (30 pts): Accurate transcription and concise summary
- **SOP Validation** (30 pts): Correct boolean values and compliance scoring
- **Analytics** (10 pts): Accurate payment/rejection classification
- **Keywords** (10 pts): Relevant keywords from transcript

### Code Quality (10 points)
- Clean code structure
- Proper error handling
- Well-documented functions
- Production-ready deployment

## Sample Test Audio
```
https://recordings.exotel.com/exotelrecordings/guvi64/5780094ea05a75c867120809da9a199f.mp3
```

## Project Structure
```
call-center-api/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .env                  # Actual environment variables (gitignored)
├── test_api.py           # Testing script
├── README.md             # This file
└── render.yaml           # Render deployment config (optional)
```

## License
MIT License - GUVI Hackathon 2026

## Author
Vishwa - Final Year B.Tech CSE Student
R.M.K. Engineering College, Chennai

## Acknowledgments
- GUVI & HCL for organizing the hackathon
- Groq for Whisper API access
- Google for Gemini AI API
