import requests
import json
import sys

# Define the local Ollama API endpoint
OLLAMA_API_URL = "http://localhost:11434/api/generate"

# The data we want Qwen to analyze
prompt = """
You are an expert qualitative researcher. I have the following data from a recent survey of 60 teachers regarding their digital training habits:

- Awareness of digital training program: 23 out of 60 teachers (very low).
- Preferred time/location: 48 teachers prefer to do it at home, after school.
- Preferred duration: 18 teachers specifically requested a 2-hour maximum duration.
- Platform preference: 40 use DIKSHA, 30 use iGOT (there is fragmentation).
- Information source: Most get course links from WhatsApp groups.
- Preferred content: Animated videos, assessments, and quizzes.
- Barriers: Technical issues and time constraints.

Please write a short, 2-paragraph executive summary synthesizing this data. Recommend one major change to how we deliver digital training based on these insights.
"""

payload = {
    "model": "qwen3:4b",
    "prompt": prompt,
    "stream": False
}

print(f"Sending prompt to local model 'qwen3:4b' via Ollama...")

try:
    # Increased timeout to 5 minutes (300 seconds) to allow the model to load into memory
    response = requests.post(OLLAMA_API_URL, json=payload, timeout=300)
    response.raise_for_status()
    
    result = response.json()
    print("\n" + "="*50)
    print("QWEN 3 (4B) RESPONSE:")
    print("="*50)
    print(result.get("response", "No response text found."))
    print("="*50)
    
except requests.exceptions.RequestException as e:
    print(f"\nError communicating with Ollama API: {e}")
    print("Make sure the Ollama service is running in the background.")
