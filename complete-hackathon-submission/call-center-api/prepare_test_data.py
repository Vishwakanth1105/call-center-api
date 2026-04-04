import requests
import base64
import json

# Download sample audio and convert to base64
audio_url = "https://recordings.exotel.com/exotelrecordings/guvi64/5780094ea05a75c867120809da9a199f.mp3"

print(f"Downloading audio from: {audio_url}")
response = requests.get(audio_url)

if response.status_code == 200:
    audio_base64 = base64.b64encode(response.content).decode('utf-8')
    print(f"✓ Audio downloaded and encoded")
    print(f"  Size: {len(response.content)} bytes")
    print(f"  Base64 length: {len(audio_base64)} characters")
    print(f"  First 100 chars: {audio_base64[:100]}...")
    
    # Save to file for later use
    with open('sample_audio_base64.txt', 'w') as f:
        f.write(audio_base64)
    print(f"✓ Saved to sample_audio_base64.txt")
    
    # Create sample request payload
    payload = {
        "language": "Tamil",
        "audioFormat": "mp3",
        "audioBase64": audio_base64
    }
    
    with open('sample_request.json', 'w') as f:
        json.dump(payload, f, indent=2)
    print(f"✓ Sample request saved to sample_request.json")
    
else:
    print(f"✗ Failed to download: {response.status_code}")
