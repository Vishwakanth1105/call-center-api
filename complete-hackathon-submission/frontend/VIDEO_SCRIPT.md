# 🎥 Demo Video Script (2-5 minutes)

## Recording Setup

**Tools Needed:**
- Screen recorder (OBS Studio / Loom / QuickTime)
- Microphone (built-in is fine)
- Sample MP3 file

**Settings:**
- Resolution: 1920x1080 (1080p)
- Audio: Clear narration (no background music needed)
- Format: MP4 or upload to YouTube

---

## VIDEO SCRIPT

### [00:00 - 00:20] Introduction (20 seconds)

**[Show: Your face or just screen with title]**

**NARRATION:**
> "Hello! I'm Vishwakanth, and I'm presenting my Call Center Compliance Analyzer built for the GUVI Hackathon 2026. This AI-powered solution analyzes call recordings to validate SOP compliance and extract business intelligence using Groq Whisper and Google Gemini AI."

**[Show: Landing page of your app]**

---

### [00:20 - 00:40] Problem Statement (20 seconds)

**[Show: PDF or text overlay explaining the problem]**

**NARRATION:**
> "The problem: Call centers need to ensure agents follow standard operating procedures, but manual auditing is time-consuming and inconsistent. My solution automates this process using AI, providing instant compliance scores, sentiment analysis, and actionable insights."

---

### [00:40 - 01:20] Architecture Overview (40 seconds)

**[Show: Architecture diagram or draw on screen]**

**NARRATION:**
> "Here's how it works: The frontend is built with React and Tailwind CSS, deployed on Vercel. Users upload MP3 files which are converted to Base64 and sent to our Flask API on Render. The backend uses Groq's Whisper API for speech-to-text transcription, supporting both Tamil and Hindi. Then, Google Gemini AI analyzes the transcript for SOP compliance, payment preferences, rejection reasons, sentiment, and keywords. Results are returned as structured JSON and beautifully displayed on the frontend."

**[Show architecture diagram with arrows pointing to each component]**

---

### [01:20 - 02:30] Live Demo (70 seconds)

**[Show: Your live website]**

**NARRATION:**
> "Let me show you a live demonstration. Here's the web interface - clean, responsive, and user-friendly."

**[Action: Drag and drop MP3 file]**

> "I'll upload this sample call recording. You can drag and drop or click to select an MP3 file."

**[Action: Click "Analyze Call Recording"]**

> "Now I'll click Analyze. The system is processing the audio - this takes about 15 to 30 seconds as it transcribes and analyzes the call."

**[Show: Loading state]**

> "Notice the loading indicator keeps users informed."

**[Show: Results appear]**

> "And here are the results! At the top, we see a concise summary of the conversation."

**[Scroll to SOP Validation]**

> "The SOP compliance section shows a score of 80% - four out of five stages were completed. The agent greeted, discussed the problem, offered a solution, and closed properly, but didn't identify the customer. Each stage is clearly marked with visual indicators."

**[Scroll to Analytics]**

> "The analytics section shows the customer preferred EMI payment, there was no rejection, and the sentiment was positive."

**[Show: Keywords]**

> "Here are the extracted keywords - Guvi Institution, Data Science, Career Change - all relevant to the conversation."

**[Scroll to Transcript]**

> "And finally, the full transcript for detailed review."

---

### [02:30 - 03:00] Technical Highlights (30 seconds)

**[Show: Code editor or tech stack slide]**

**NARRATION:**
> "Technical highlights: The frontend uses React 18 with Vite for blazing-fast builds, Tailwind CSS for responsive design, and Lucide icons for beautiful UI. The backend is a Flask REST API with Gunicorn for production. I used Groq's Whisper-large-v3 model for 95%+ transcription accuracy, and Google Gemini 1.5 Flash for intelligent NLP analysis. The entire project is documented on GitHub with detailed setup instructions."

---

### [03:00 - 03:30] AI Tools Disclosure (30 seconds)

**[Show: README section or text overlay]**

**NARRATION:**
> "As required, I'm disclosing all AI tools used. Claude AI assisted with code generation and architecture planning, significantly reducing development time while maintaining best practices. Groq Whisper handles speech-to-text, and Google Gemini provides the NLP analysis. This combination allowed me to build a production-ready application in just a few hours."

---

### [03:30 - 03:50] Mobile Responsiveness (20 seconds)

**[Show: Open browser dev tools, switch to mobile view]**

**NARRATION:**
> "The application is fully responsive. Here it is on mobile - the interface adapts perfectly to smaller screens, maintaining usability and aesthetics across all devices."

**[Demo scrolling on mobile view]**

---

### [03:50 - 04:20] Deployment & URLs (30 seconds)

**[Show: Both URLs in browser tabs]**

**NARRATION:**
> "The frontend is deployed on Vercel at this URL, and the backend API is on Render. Both are publicly accessible, and I've tested them extensively. The code is open-source on GitHub with comprehensive documentation including setup instructions, architecture details, and the complete tech stack."

**[Show GitHub repo briefly]**

---

### [04:20 - 04:50] Conclusion (30 seconds)

**[Show: Your face or landing page]**

**NARRATION:**
> "In summary, this Call Center Compliance Analyzer solves a real business problem using modern AI technology. It provides instant SOP validation, business intelligence, and a great user experience. The project demonstrates full-stack development skills, AI integration, and production deployment. All code and documentation are available on GitHub. Thank you for watching, and I look forward to your feedback!"

**[Show: Contact info or GitHub link]**

---

## Recording Tips

### DO:
✅ **Speak clearly** and at moderate pace
✅ **Show actual functionality** - upload real file, get real results
✅ **Highlight unique features** - AI analysis, beautiful UI
✅ **Keep it concise** - 3-4 minutes is perfect
✅ **Test audio** before final recording
✅ **Use high quality** - 1080p minimum

### DON'T:
❌ Don't rush through sections
❌ Don't have long pauses
❌ Don't show errors without explaining them
❌ Don't make it too long (max 5 minutes)
❌ Don't forget to mention AI tools used

---

## After Recording

### Edit (Optional)
- Trim dead air at start/end
- Add simple title card (optional)
- Ensure audio is clear

### Upload to YouTube

1. Go to [youtube.com/upload](https://youtube.com/upload)
2. Upload your video
3. Settings:
   - **Title**: "Call Center Compliance Analyzer - GUVI Hackathon 2026"
   - **Description**: 
     ```
     AI-Powered Call Center Compliance Analyzer built for GUVI Hackathon 2026.
     
     Tech Stack:
     - Frontend: React + Tailwind CSS (Vercel)
     - Backend: Flask + Groq Whisper + Google Gemini (Render)
     
     GitHub: https://github.com/YOUR_USERNAME/call-center-compliance-api
     Live Demo: https://your-app.vercel.app
     ```
   - **Visibility**: Public or Unlisted (both work for submission)
   - **Category**: Science & Technology
   - **Tags**: GUVI, Hackathon, AI, Machine Learning, Call Center, SOP Compliance

4. Click **Publish**
5. Copy the YouTube URL

### Alternative: Google Drive

If YouTube doesn't work:

1. Go to [drive.google.com](https://drive.google.com)
2. Upload video
3. Right-click → Share
4. Change to "Anyone with the link"
5. Copy link

---

## Submit Video URL

Include in your GUVI submission:
```
Demo Video: https://youtu.be/YOUR_VIDEO_ID
```

---

**Total Time to Record**: 30-45 minutes including setup and retakes
**Final Video Length**: 3-4 minutes (perfect!)

**You got this! 🎬**
