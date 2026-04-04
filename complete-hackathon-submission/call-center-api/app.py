from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import base64
import tempfile
from groq import Groq
import google.generativeai as genai
import json
import re

app = Flask(__name__)
CORS(app)

# Configuration from environment variables
API_KEY = os.environ.get('API_KEY')
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

# Initialize clients
groq_client = Groq(api_key=GROQ_API_KEY)
genai.configure(api_key=GEMINI_API_KEY)

def verify_api_key():
    """Verify API key from request header"""
    api_key = request.headers.get('x-api-key')
    return api_key == API_KEY if api_key and API_KEY else False

def transcribe_audio(audio_base64, language):
    """Transcribe audio using Groq Whisper API"""
    try:
        audio_data = base64.b64decode(audio_base64)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_audio:
            temp_audio.write(audio_data)
            temp_audio_path = temp_audio.name
        
        with open(temp_audio_path, 'rb') as audio_file:
            transcription = groq_client.audio.transcriptions.create(
                file=audio_file,
                model="whisper-large-v3",
                response_format="json",
                language="ta" if language.lower() == "tamil" else "hi"
            )
        
        os.unlink(temp_audio_path)
        return transcription.text
    
    except Exception as e:
        raise Exception(f"Transcription error: {str(e)}")

def analyze_with_gemini(transcript, language):
    """Analyze transcript using Gemini for SOP validation, analytics, and keywords"""
    
    prompt = f"""You are an expert call center quality analyst. Analyze the following call transcript and provide structured analysis.

Language: {language}
Transcript: {transcript}

Return ONLY a valid JSON object (no markdown, no code blocks):

{{
  "summary": "Concise 2-3 sentence summary",
  "sop_validation": {{
    "greeting": true or false,
    "identification": true or false,
    "problemStatement": true or false,
    "solutionOffering": true or false,
    "closing": true or false,
    "complianceScore": 0.0 to 1.0,
    "adherenceStatus": "FOLLOWED" or "NOT_FOLLOWED",
    "explanation": "Brief explanation"
  }},
  "analytics": {{
    "paymentPreference": "EMI" or "FULL_PAYMENT" or "PARTIAL_PAYMENT" or "DOWN_PAYMENT",
    "rejectionReason": "HIGH_INTEREST" or "BUDGET_CONSTRAINTS" or "ALREADY_PAID" or "NOT_INTERESTED" or "NONE",
    "sentiment": "Positive" or "Neutral" or "Negative"
  }},
  "keywords": ["keyword1", "keyword2"]
}}

Rules:
1. Return ONLY JSON, no other text
2. Use lowercase booleans: true/false
3. complianceScore = (count of true values) / 5
4. adherenceStatus = "FOLLOWED" if all 5 true, else "NOT_FOLLOWED"
5. rejectionReason = "NONE" if no rejection"""

    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Remove markdown if present
        response_text = re.sub(r'^```json\s*', '', response_text)
        response_text = re.sub(r'^```\s*', '', response_text)
        response_text = re.sub(r'\s*```$', '', response_text)
        response_text = response_text.strip()
        
        analysis = json.loads(response_text)
        
        # Validate SOP structure
        if "sop_validation" in analysis:
            sop = analysis["sop_validation"]
            true_count = sum([
                sop.get("greeting", False),
                sop.get("identification", False),
                sop.get("problemStatement", False),
                sop.get("solutionOffering", False),
                sop.get("closing", False)
            ])
            sop["complianceScore"] = round(true_count / 5.0, 1)
            sop["adherenceStatus"] = "FOLLOWED" if true_count == 5 else "NOT_FOLLOWED"
        
        return analysis
    
    except json.JSONDecodeError as e:
        raise Exception(f"Gemini returned invalid JSON: {str(e)}")
    except Exception as e:
        raise Exception(f"Gemini analysis error: {str(e)}")

@app.route('/api/call-analytics', methods=['POST'])
def call_analytics():
    """Main API endpoint for call analytics"""
    
    if not verify_api_key():
        return jsonify({"error": "Unauthorized"}), 401
    
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Invalid request body"}), 400
        
        language = data.get('language', 'Tamil')
        audio_base64 = data.get('audioBase64')
        
        if not audio_base64:
            return jsonify({"error": "Missing audioBase64 field"}), 400
        
        # Step 1: Transcribe
        transcript = transcribe_audio(audio_base64, language)
        
        if not transcript or not transcript.strip():
            return jsonify({"error": "Transcription failed or empty"}), 500
        
        # Step 2: Analyze
        analysis = analyze_with_gemini(transcript, language)
        
        # Step 3: Build response
        return jsonify({
            "status": "success",
            "language": language,
            "transcript": transcript,
            "summary": analysis.get("summary", ""),
            "sop_validation": analysis.get("sop_validation", {}),
            "analytics": analysis.get("analytics", {}),
            "keywords": analysis.get("keywords", [])
        }), 200
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
