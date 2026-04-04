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
        response = model.generate_content(prompt)  # ✅ CHANGED FROM gemini_model to model
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
