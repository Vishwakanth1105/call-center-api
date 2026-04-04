import requests
import base64
import json

# Download sample audio and convert to base64
def download_and_encode_audio(url):
    """Download audio from URL and encode to base64"""
    print(f"Downloading audio from: {url}")
    response = requests.get(url)
    if response.status_code == 200:
        audio_base64 = base64.b64encode(response.content).decode('utf-8')
        print(f"Audio downloaded and encoded. Size: {len(audio_base64)} characters")
        return audio_base64
    else:
        raise Exception(f"Failed to download audio: {response.status_code}")

# Test the API
def test_api(base_url="http://localhost:5000"):
    """Test the call analytics API"""
    
    # Sample audio URL
    audio_url = "https://recordings.exotel.com/exotelrecordings/guvi64/5780094ea05a75c867120809da9a199f.mp3"
    
    # Download and encode
    audio_base64 = download_and_encode_audio(audio_url)
    
    # Prepare request
    endpoint = f"{base_url}/api/call-analytics"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": "sk_track3_987654321"
    }
    
    payload = {
        "language": "Tamil",
        "audioFormat": "mp3",
        "audioBase64": audio_base64
    }
    
    print(f"\nSending request to: {endpoint}")
    print("Headers:", json.dumps({k: v for k, v in headers.items()}, indent=2))
    print("Payload keys:", list(payload.keys()))
    
    # Make request
    response = requests.post(endpoint, headers=headers, json=payload)
    
    print(f"\nResponse Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("\n" + "="*80)
        print("API RESPONSE:")
        print("="*80)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        print("="*80)
        
        # Validation
        print("\n" + "="*80)
        print("VALIDATION:")
        print("="*80)
        
        required_fields = ["status", "language", "transcript", "summary", 
                          "sop_validation", "analytics", "keywords"]
        
        for field in required_fields:
            if field in result:
                print(f"✓ {field}: Present")
            else:
                print(f"✗ {field}: MISSING")
        
        # Validate SOP structure
        if "sop_validation" in result:
            sop = result["sop_validation"]
            sop_fields = ["greeting", "identification", "problemStatement", 
                         "solutionOffering", "closing", "complianceScore", 
                         "adherenceStatus", "explanation"]
            print("\nSOP Validation Fields:")
            for field in sop_fields:
                if field in sop:
                    print(f"  ✓ {field}: {sop[field]}")
                else:
                    print(f"  ✗ {field}: MISSING")
        
        # Validate Analytics
        if "analytics" in result:
            analytics = result["analytics"]
            analytics_fields = ["paymentPreference", "rejectionReason", "sentiment"]
            print("\nAnalytics Fields:")
            for field in analytics_fields:
                if field in analytics:
                    print(f"  ✓ {field}: {analytics[field]}")
                else:
                    print(f"  ✗ {field}: MISSING")
        
        print("="*80)
        
    else:
        print(f"Error Response: {response.text}")

def test_unauthorized():
    """Test unauthorized access"""
    print("\n" + "="*80)
    print("Testing Unauthorized Access (no API key)")
    print("="*80)
    
    endpoint = "http://localhost:5000/api/call-analytics"
    headers = {
        "Content-Type": "application/json"
        # No x-api-key header
    }
    
    payload = {
        "language": "Tamil",
        "audioFormat": "mp3",
        "audioBase64": "test"
    }
    
    response = requests.post(endpoint, headers=headers, json=payload)
    print(f"Response Status: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 401:
        print("✓ Unauthorized access properly rejected")
    else:
        print("✗ Expected 401 status code")

if __name__ == "__main__":
    print("="*80)
    print("CALL CENTER COMPLIANCE API - TEST SUITE")
    print("="*80)
    
    # Test health endpoint
    print("\nTesting health endpoint...")
    try:
        health_response = requests.get("http://localhost:5000/health")
        print(f"Health Check: {health_response.json()}")
    except Exception as e:
        print(f"Server not running. Please start the server first: python app.py")
        print(f"Error: {e}")
        exit(1)
    
    # Test unauthorized
    test_unauthorized()
    
    # Test main API
    print("\n" + "="*80)
    print("Testing Main API with Sample Audio")
    print("="*80)
    test_api()
