import requests
import os

WHISPER_API_URL = 'https://api.openai.com/v1/audio/transcriptions'
WHISPER_API_KEY = os.getenv('OPENAI_API_KEY')
if not WHISPER_API_KEY:
    raise ValueError("API key is not set in the environment variable 'OPENAI_API_KEY'")

@staticmethod
def transcribe_audio(audio_data):
    headers = {'Authorization': f'Bearer {WHISPER_API_KEY}',}
    files = {'file': ('audio.wav', audio_data, 'audio/wav')}
    data = {'model': 'whisper-1'}
    response = requests.post(WHISPER_API_URL, headers=headers, files=files, data=data)
    if response.status_code == 200:
        response_json = response.json()
        return response_json.get('text', 'No text received')
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None
