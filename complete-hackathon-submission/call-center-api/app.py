from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import base64
import tempfile
from groq import Groq
import json
import re

app = Flask(__name__)
CORS(app)

# Configuration from environment variables (NEVER hardcode!)
API_KEY = os.environ.get('API_KEY')
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')

# Initialize Groq client
groq_client = Groq(api_key=GROQ_API_KEY)

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

def analyze_with_groq(transcript, language):
    """Analyze transcript using Groq LLaMA for SOP validation and analytics"""
    
    prompt = f"""You are a call center quality analyst. Analyze this transcript and return ONLY valid JSON (no markdown, no explanations):

Transcript: {transcript}

Return this exact structure:
{{
  "summary": "2-3 sentence summary of the call",
  "sop_validation": {{
    "greeting": true,
    "identification": false,
    "problemStatement": true,
    "solutionOffering": true,
    "closing": false,
    "complianceScore": 0.6,
    "adherenceStatus": "NOT_FOLLOWED",
    "explanation": "Missing identification and closing steps"
  }},
  "analytics": {{
    "paymentPreference": "EMI",
    "rejectionReason": "NONE",
    "sentiment": "Positive"
  }},
  "keywords": ["payment", "loan", "emi", "interest"]
}}

Return ONLY the JSON object, nothing else."""

    try:
        response = groq_client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            max_tokens=1500
        )
        
        response_text = response.choices[0].message.content.strip()
        
        # Remove markdown if present
        response_text = re.sub(r'^```json\s*', '', response_text)
        response_text = re.sub(r'^```\s*', '', response_text)
        response_text = re.sub(r'\s*```$', '', response_text)
        response_text = response_text.strip()
        
        analysis = json.loads(response_text)
        
        # Validate and calculate SOP metrics
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
    
    except Exception as e:
        raise Exception(f"Analysis error: {str(e)}")

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
        
        # Step 1: Transcribe audio
        transcript = transcribe_audio(audio_base64, language)
        
        if not transcript or not transcript.strip():
            return jsonify({"error": "Transcription failed or empty"}), 500
        
        # Step 2: Analyze with Groq
        analysis = analyze_with_groq(transcript, language)
        
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
