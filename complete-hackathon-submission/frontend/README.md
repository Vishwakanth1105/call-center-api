# 🎯 Call Center Compliance Analyzer

AI-Powered solution for analyzing call center recordings to ensure SOP compliance, extract business intelligence, and generate actionable insights.

**Built for GUVI Hackathon 2026 - Track 3: Call Center Compliance**

[![Live Demo](https://img.shields.io/badge/Live-Demo-blue)](https://your-app.vercel.app)
[![API](https://img.shields.io/badge/API-Live-green)](https://your-api.onrender.com)

---

## 🌟 Features

### Core Functionality
- ✅ **Speech-to-Text Transcription** - Converts Tamil/Hindi audio to text using Groq Whisper API
- ✅ **SOP Validation** - Analyzes adherence to standard call scripts (5 stages)
- ✅ **Compliance Scoring** - Calculates compliance score (0.0-1.0)
- ✅ **Payment Classification** - Categorizes payment preferences (EMI, FULL, PARTIAL, DOWN)
- ✅ **Rejection Analysis** - Identifies reasons for incomplete transactions
- ✅ **Sentiment Analysis** - Detects customer sentiment (Positive, Neutral, Negative)
- ✅ **Keyword Extraction** - Extracts relevant keywords for business intelligence

### User Experience
- ✅ **Drag & Drop Upload** - Easy MP3 file upload interface
- ✅ **Real-time Processing** - Live analysis with progress indicators
- ✅ **Visual Results** - Beautiful charts and metrics display
- ✅ **Responsive Design** - Works seamlessly on mobile, tablet, and desktop
- ✅ **Professional UI** - Modern, clean interface with Tailwind CSS

---

## 🏗️ Architecture

```
┌─────────────────────────────────────┐
│     USER (Browser/Mobile)           │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│   FRONTEND (Vercel)                 │
│   - React 18 + Vite                 │
│   - Tailwind CSS                    │
│   - Drag & Drop Upload              │
│   - Results Visualization           │
└──────────────┬──────────────────────┘
               │
               │ POST /api/call-analytics
               │ Base64 Audio + API Key
               ▼
┌─────────────────────────────────────┐
│   BACKEND API (Render)              │
│   - Flask REST API                  │
│   - Groq Whisper (Transcription)    │
│   - Google Gemini (NLP Analysis)    │
│   - JSON Response                   │
└─────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

### Frontend
- **Framework**: React 18
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **Deployment**: Vercel

### Backend
- **Framework**: Flask (Python 3.10+)
- **Speech-to-Text**: Groq Whisper API (whisper-large-v3)
- **NLP Analysis**: Google Gemini 1.5 Flash
- **Server**: Gunicorn
- **Deployment**: Render

---

## 🚀 Setup Instructions

### Prerequisites
- Node.js 18+ (for frontend)
- Python 3.10+ (for backend)
- npm or yarn (for frontend)
- Git

### Frontend Setup

1. **Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/call-center-compliance-api.git
cd call-center-compliance-api/frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Update API URL**
Edit `src/App.jsx` and replace the API_URL:
```javascript
const API_URL = 'https://your-actual-api.onrender.com/api/call-analytics';
```

4. **Run development server**
```bash
npm run dev
```

Frontend will be available at `http://localhost:5173`

5. **Build for production**
```bash
npm run build
```

### Backend Setup

1. **Navigate to backend directory**
```bash
cd ../backend
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set environment variables**
Create `.env` file:
```
API_KEY=sk_track3_987654321
GROQ_API_KEY=your_groq_api_key
GEMINI_API_KEY=your_gemini_api_key
PORT=5000
```

4. **Run the server**
```bash
python app.py
```

API will be available at `http://localhost:5000`

---

## 🌐 Deployment

### Deploy Frontend to Vercel

1. **Install Vercel CLI**
```bash
npm i -g vercel
```

2. **Deploy**
```bash
cd frontend
vercel
```

Follow the prompts. Your app will be live at `https://your-app.vercel.app`

### Deploy Backend to Render

1. Go to [render.com](https://render.com)
2. Create new Web Service
3. Connect your GitHub repository
4. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120`
5. Add environment variables (API_KEY, GROQ_API_KEY, GEMINI_API_KEY)
6. Deploy!

Your API will be live at `https://your-app-name.onrender.com`

---

## 🤖 AI Tools Used

This project leverages multiple AI technologies:

### 1. **Claude AI (Anthropic)**
- **Usage**: Code generation, architecture planning, and development assistance
- **Purpose**: Accelerated development with best practices and clean code
- **Impact**: Reduced development time by ~70%, improved code quality

### 2. **Groq Whisper API**
- **Model**: whisper-large-v3
- **Usage**: Speech-to-text transcription for Tamil and Hindi audio
- **Purpose**: Convert MP3 call recordings to accurate text transcripts
- **Features**: 
  - 95%+ accuracy on clear audio
  - Multilingual support (Tamil, Hindi, Tanglish, Hinglish)
  - Fast processing (5-10 seconds per audio)

### 3. **Google Gemini 1.5 Flash**
- **Usage**: Natural Language Processing and analysis
- **Purpose**: 
  - Generate concise summaries
  - Validate SOP compliance (5 stages)
  - Classify payment preferences
  - Identify rejection reasons
  - Analyze customer sentiment
  - Extract relevant keywords
- **Features**:
  - Structured JSON output
  - Context-aware analysis
  - Multi-stage reasoning

### AI Tool Impact Summary

| Tool | Purpose | Benefit |
|------|---------|---------|
| Claude AI | Development assistance | Faster, cleaner code |
| Groq Whisper | Speech-to-Text | Accurate transcription |
| Google Gemini | NLP Analysis | Intelligent insights |

**Total Development Time**: ~3 hours (would have taken 15+ hours without AI assistance)

**Code Quality**: Production-ready with proper error handling, documentation, and best practices

---

## 📊 API Documentation

### Endpoint
```
POST https://your-api.onrender.com/api/call-analytics
```

### Headers
```
Content-Type: application/json
x-api-key: sk_track3_987654321
```

### Request Body
```json
{
  "language": "Tamil",
  "audioFormat": "mp3",
  "audioBase64": "SUQzBAAAAAAAI1RTU0UAAAA..."
}
```

### Response
```json
{
  "status": "success",
  "language": "Tamil",
  "transcript": "Full transcription...",
  "summary": "Concise summary...",
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

---

## 🎥 Demo Video

**YouTube Link**: [Watch Demo](https://youtube.com/your-video-link)

**Duration**: 3 minutes

**Content**:
1. Introduction and problem statement
2. Frontend UI walkthrough
3. Upload MP3 file demonstration
4. Real-time analysis process
5. Results visualization
6. Technical architecture overview

---

## 📁 Project Structure

```
call-center-compliance-api/
├── frontend/                    # React frontend
│   ├── src/
│   │   ├── App.jsx             # Main React component
│   │   ├── main.jsx            # Entry point
│   │   └── index.css           # Tailwind CSS
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
│
├── backend/                     # Flask backend
│   ├── app.py                  # Main Flask API
│   ├── requirements.txt        # Python dependencies
│   ├── .env.example           # Environment template
│   └── render.yaml            # Render config
│
├── README.md                   # This file
└── .gitignore
```

---

## 🧪 Testing

### Frontend Testing
```bash
cd frontend
npm run dev
# Open http://localhost:5173
# Upload sample MP3 file
# Verify results display correctly
```

### Backend Testing
```bash
cd backend
python test_api.py
```

### Integration Testing
1. Start backend server
2. Update API_URL in frontend
3. Start frontend dev server
4. Upload test MP3 file
5. Verify end-to-end flow

---

## ⚠️ Known Limitations

1. **Processing Time**: Analysis takes 15-30 seconds due to AI processing
2. **File Size**: Recommended MP3 size < 10MB for optimal performance
3. **Language Support**: Currently supports Tamil and Hindi only
4. **Free Tier Limitations**: 
   - Render: Server may sleep after 15 minutes of inactivity
   - Groq: Rate limits on free tier
5. **Audio Quality**: Best results with clear audio (minimal background noise)

---

## 🔮 Future Enhancements

- [ ] Real-time streaming transcription
- [ ] Support for more languages (English, Telugu, Kannada)
- [ ] Historical analytics dashboard
- [ ] Export reports as PDF
- [ ] Batch processing for multiple files
- [ ] Integration with CRM systems
- [ ] Voice activity detection
- [ ] Speaker diarization (identify multiple speakers)

---

## 🤝 Contributing

This is a hackathon project, but suggestions are welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is created for GUVI Hackathon 2026. All rights reserved.

---

## 👨‍💻 Author

**Vishwakanth P**
- Final Year B.Tech CSE Student
- R.M.K. Engineering College, Chennai
- GitHub: [@YOUR_USERNAME](https://github.com/YOUR_USERNAME)

---

## 🙏 Acknowledgments

- **GUVI** for organizing the hackathon
- **HCL** for the internship opportunity
- **Groq** for Whisper API access
- **Google** for Gemini AI API
- **Anthropic** for Claude AI assistance

---

## 📞 Support

For issues or questions:
- Open an issue on GitHub
- Email: your.email@example.com

---

**Built with ❤️ for GUVI Hackathon 2026**
