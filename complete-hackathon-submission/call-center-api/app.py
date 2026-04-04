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
CORS(app)  # Enable CORS for all routes

# Configuration
API_KEY = os.environ.get('API_KEY', 'sk_track3_987654321')
GROQ_API_KEY = os.environ.get('GROQ_API_KEY', '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')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', 'AIzaSyA6nmuCv43jMkSWSb1qngc4yrnMtmY4Mu0')

# Initialize clients
groq_client = Groq(api_key=GROQ_API_KEY)
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel('gemini-pro')

def verify_api_key():
    """Verify API key from request header"""
    api_key = request.headers.get('x-api-key')
    if not api_key or api_key != API_KEY:
        return False
    return True

def transcribe_audio(audio_base64, language):
    """Transcribe audio using Groq Whisper API"""
    try:
        # Decode base64 to binary
        audio_data = base64.b64decode(audio_base64)
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_audio:
            temp_audio.write(audio_data)
            temp_audio_path = temp_audio.name
        
        # Transcribe using Groq
        with open(temp_audio_path, 'rb') as audio_file:
            transcription = groq_client.audio.transcriptions.create(
                file=audio_file,
                model="whisper-large-v3",
                response_format="json",
                language="ta" if language.lower() == "tamil" else "hi"
            )
        
        # Clean up temp file
        os.unlink(temp_audio_path)
        
        return transcription.text
    
    except Exception as e:
        raise Exception(f"Transcription error: {str(e)}")

def analyze_with_gemini(transcript, language):
    """Analyze transcript using Gemini for SOP validation, analytics, and keywords"""
    
    prompt = f"""You are an expert call center quality analyst. Analyze the following call transcript and provide structured analysis.

Language: {language}
Transcript: {transcript}

Analyze and return ONLY a valid JSON object with this EXACT structure (no markdown, no code blocks, just raw JSON):

{{
  "summary": "Concise 2-3 sentence summary of the conversation",
  "sop_validation": {{
    "greeting": true or false (Did agent greet the customer?),
    "identification": true or false (Did agent identify themselves and/or verify customer identity?),
    "problemStatement": true or false (Was the issue/purpose discussed?),
    "solutionOffering": true or false (Was a solution/offer presented?),
    "closing": true or false (Did agent close the call properly?),
    "complianceScore": 0.0 to 1.0 (0.0 = none followed, 0.2 = 1 step, 0.4 = 2 steps, 0.6 = 3 steps, 0.8 = 4 steps, 1.0 = all 5 steps),
    "adherenceStatus": "FOLLOWED" if all 5 steps present, else "NOT_FOLLOWED",
    "explanation": "Brief explanation of what was missing or confirmed"
  }},
  "analytics": {{
    "paymentPreference": "EMI" or "FULL_PAYMENT" or "PARTIAL_PAYMENT" or "DOWN_PAYMENT" (based on customer's payment intent),
    "rejectionReason": "HIGH_INTEREST" or "BUDGET_CONSTRAINTS" or "ALREADY_PAID" or "NOT_INTERESTED" or "NONE" (NONE if payment was accepted or discussed positively),
    "sentiment": "Positive" or "Neutral" or "Negative" (overall customer sentiment)
  }},
  "keywords": ["keyword1", "keyword2", ...] (10-15 relevant keywords from the conversation about products, services, concerns, or key topics)
}}

Critical Rules:
1. Return ONLY the JSON object, no other text
2. Use double quotes for all strings
3. Boolean values must be lowercase: true/false
4. complianceScore calculation: count true values in greeting, identification, problemStatement, solutionOffering, closing, then divide by 5
5. adherenceStatus is "FOLLOWED" only if all 5 are true, else "NOT_FOLLOWED"
6. For paymentPreference: analyze what payment method customer preferred or discussed
7. For rejectionReason: if customer didn't complete payment or showed hesitation, identify why; otherwise use "NONE"
"""

    try:
        response = gemini_model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Remove markdown code blocks if present
        response_text = re.sub(r'^```json\s*', '', response_text)
        response_text = re.sub(r'^```\s*', '', response_text)
        response_text = re.sub(r'\s*```$', '', response_text)
        response_text = response_text.strip()
        
        # Parse JSON
        analysis = json.loads(response_text)
        
        # Validate and ensure correct structure
        if "sop_validation" in analysis:
            sop = analysis["sop_validation"]
            # Calculate compliance score correctly
            true_count = sum([
                sop.get("greeting", False),
                sop.get("identification", False),
                sop.get("problemStatement", False),
                sop.get("solutionOffering", False),
                sop.get("closing", False)
            ])
            sop["complianceScore"] = round(true_count / 5.0, 1)
            
            # Set adherence status
            if true_count == 5:
                sop["adherenceStatus"] = "FOLLOWED"
            else:
                sop["adherenceStatus"] = "NOT_FOLLOWED"
        
        return analysis
    
    except json.JSONDecodeError as e:
        raise Exception(f"Gemini returned invalid JSON: {str(e)}")
    except Exception as e:
        raise Exception(f"Gemini analysis error: {str(e)}")

@app.route('/api/call-analytics', methods=['POST'])
def call_analytics():
    """Main API endpoint for call analytics"""
    
    # Verify API key
    if not verify_api_key():
        return jsonify({"error": "Unauthorized"}), 401
    
    try:
        # Get request data
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Invalid request body"}), 400
        
        language = data.get('language', 'Tamil')
        audio_format = data.get('audioFormat', 'mp3')
        audio_base64 = data.get('audioBase64')
        
        if not audio_base64:
            return jsonify({"error": "Missing audioBase64 field"}), 400
        
        # Step 1: Transcribe audio
        transcript = transcribe_audio(audio_base64, language)
        
        if not transcript or len(transcript.strip()) == 0:
            return jsonify({"error": "Transcription failed or empty"}), 500
        
        # Step 2: Analyze with Gemini
        analysis = analyze_with_gemini(transcript, language)
        
        # Step 3: Build response
        response = {
            "status": "success",
            "language": language,
            "transcript": transcript,
            "summary": analysis.get("summary", ""),
            "sop_validation": analysis.get("sop_validation", {}),
            "analytics": analysis.get("analytics", {}),
            "keywords": analysis.get("keywords", [])
        }
        
        return jsonify(response), 200
    
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
