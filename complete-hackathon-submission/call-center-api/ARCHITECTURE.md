# System Architecture

## High-Level Flow

```
┌─────────────────┐
│   User/Client   │
│  (GUVI System)  │
└────────┬────────┘
         │
         │ POST /api/call-analytics
         │ Headers: x-api-key
         │ Body: { audioBase64, language }
         │
         ▼
┌─────────────────────────────────────────┐
│         Flask API (Render)              │
│  ┌───────────────────────────────────┐  │
│  │  1. API Key Authentication        │  │
│  │     ✓ Verify x-api-key header     │  │
│  │     ✗ Return 401 if invalid       │  │
│  └───────────────────────────────────┘  │
│                  │                       │
│                  ▼                       │
│  ┌───────────────────────────────────┐  │
│  │  2. Audio Processing              │  │
│  │     • Decode Base64 → Binary      │  │
│  │     • Save to temp file           │  │
│  └───────────────────────────────────┘  │
│                  │                       │
│                  ▼                       │
│  ┌───────────────────────────────────┐  │
│  │  3. Groq Whisper API Call         │  │
│  │     • Upload MP3 file             │  │
│  │     • Model: whisper-large-v3     │  │
│  │     • Language: Tamil/Hindi       │  │
│  │     • Get: Full Transcript        │  │
│  └───────────────────────────────────┘  │
│                  │                       │
│                  ▼                       │
│  ┌───────────────────────────────────┐  │
│  │  4. Gemini AI Analysis            │  │
│  │     • Model: gemini-1.5-flash     │  │
│  │     • Input: Transcript           │  │
│  │     • Analyze:                    │  │
│  │       - Summary                   │  │
│  │       - SOP Validation            │  │
│  │       - Payment Classification    │  │
│  │       - Rejection Reasoning       │  │
│  │       - Sentiment Analysis        │  │
│  │       - Keyword Extraction        │  │
│  └───────────────────────────────────┘  │
│                  │                       │
│                  ▼                       │
│  ┌───────────────────────────────────┐  │
│  │  5. Response Construction         │  │
│  │     • Build JSON response         │  │
│  │     • Validate structure          │  │
│  │     • Return to client            │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
                  │
                  ▼
         ┌────────────────┐
         │ JSON Response  │
         │   200 OK       │
         └────────────────┘
```

## Component Details

### 1. API Key Authentication
```python
def verify_api_key():
    api_key = request.headers.get('x-api-key')
    if not api_key or api_key != API_KEY:
        return False  # 401 Unauthorized
    return True
```

**Security:**
- All requests must include `x-api-key` header
- Invalid/missing key → 401 Unauthorized
- Protects against unauthorized access

### 2. Audio Processing Pipeline
```python
# Decode Base64 → Binary
audio_data = base64.b64decode(audio_base64)

# Save to temp file (required by Groq)
with tempfile.NamedTemporaryFile(suffix='.mp3') as temp:
    temp.write(audio_data)
```

**Why temporary files?**
- Groq Whisper API requires file upload (not raw bytes)
- Files automatically cleaned up after processing
- Prevents disk space issues

### 3. Groq Whisper Integration
```python
groq_client.audio.transcriptions.create(
    file=audio_file,
    model="whisper-large-v3",
    language="ta" if Tamil else "hi"
)
```

**Model:** whisper-large-v3
- Best accuracy for Tamil/Hindi
- Handles Tanglish/Hinglish well
- Response time: 5-10 seconds

### 4. Gemini AI Analysis

**Prompt Engineering Strategy:**
- Clear, structured instructions
- Request JSON-only output (no markdown)
- Specify exact field names and types
- Define validation rules for SOP compliance
- Enumerate allowed values for classifications

**Analysis Components:**

#### a) Summary Generation
- Concise 2-3 sentence overview
- Key points: participants, topic, outcome

#### b) SOP Validation (5 stages)
```
greeting         → Did agent greet customer?
identification   → Did agent identify self/customer?
problemStatement → Was issue discussed?
solutionOffering → Was solution presented?
closing          → Proper call closure?

complianceScore = (true_count / 5)
adherenceStatus = "FOLLOWED" if all 5 true else "NOT_FOLLOWED"
```

#### c) Payment Classification
```
Allowed values:
- EMI
- FULL_PAYMENT
- PARTIAL_PAYMENT
- DOWN_PAYMENT
```

#### d) Rejection Reasoning
```
Allowed values:
- HIGH_INTEREST
- BUDGET_CONSTRAINTS
- ALREADY_PAID
- NOT_INTERESTED
- NONE (if no rejection)
```

#### e) Sentiment Analysis
```
- Positive: Satisfied, agreeable customer
- Neutral:  No strong emotion
- Negative: Frustrated, angry customer
```

#### f) Keyword Extraction
- 10-15 relevant keywords
- Products, services, concerns
- Traceable to transcript

### 5. Response Construction

**Validation Steps:**
1. Parse Gemini JSON response
2. Remove markdown artifacts (```json)
3. Validate all required fields
4. Calculate compliance score
5. Set adherence status
6. Return structured JSON

## Data Flow Example

**Input:**
```json
{
  "language": "Tamil",
  "audioFormat": "mp3",
  "audioBase64": "SUQzBAAAAAAAI..."
}
```

**Processing:**
1. **Groq Whisper** → Transcript
   ```
   "Agent: Hello? Customer: Yeah, hello..."
   ```

2. **Gemini Analysis** → Structured Data
   ```json
   {
     "summary": "Agent discussed course...",
     "sop_validation": { ... },
     "analytics": { ... },
     "keywords": [ ... ]
   }
   ```

**Output:**
```json
{
  "status": "success",
  "language": "Tamil",
  "transcript": "...",
  "summary": "...",
  "sop_validation": { ... },
  "analytics": { ... },
  "keywords": [ ... ]
}
```

## Error Handling

### Authentication Errors
```
401 Unauthorized
{ "error": "Unauthorized" }
```

### Validation Errors
```
400 Bad Request
{ "error": "Missing audioBase64 field" }
```

### Processing Errors
```
500 Internal Server Error
{
  "status": "error",
  "error": "Transcription error: ..."
}
```

## Performance Metrics

| Stage | Duration |
|-------|----------|
| Audio decoding | < 1 second |
| Groq Whisper API | 5-10 seconds |
| Gemini Analysis | 5-15 seconds |
| Response building | < 1 second |
| **Total** | **15-30 seconds** |

## Scalability Considerations

### Current Setup (Free Tier)
- Single worker process
- Sequential request processing
- Suitable for hackathon evaluation

### Production Improvements
- Multiple Gunicorn workers
- Request queuing (Celery + Redis)
- Caching for repeated audio
- Database for analytics storage
- Rate limiting per API key

## Technology Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **API Framework** | Flask 3.0 | HTTP request handling |
| **Production Server** | Gunicorn | WSGI server |
| **Speech-to-Text** | Groq Whisper | Audio transcription |
| **NLP Analysis** | Google Gemini | AI-powered analysis |
| **Deployment** | Render | Cloud hosting |
| **Language** | Python 3.12 | Core language |

## Security Features

1. **API Key Authentication**
   - Header-based authentication
   - Environment variable storage
   - No hardcoded secrets

2. **Input Validation**
   - Base64 format check
   - Required field validation
   - Error handling for malformed data

3. **Environment Isolation**
   - .env for sensitive data
   - .gitignore prevents key leakage
   - Separate dev/prod configs

## Deployment Architecture

```
GitHub Repository
      ↓
   Render Platform
      ↓
   Build Process
   (pip install)
      ↓
   Gunicorn Server
   (2 workers)
      ↓
   Flask Application
      ↓
   Public URL
```

**Auto-deployment:**
- Push to GitHub → Auto-redeploy on Render
- Zero-downtime deployments
- Automatic HTTPS/SSL

## Monitoring & Logging

### Available Logs
- Request/response logging
- Error tracking
- API call duration
- Groq/Gemini API errors

### Health Monitoring
- `/health` endpoint
- 200 OK = Service running
- Use for uptime monitoring
