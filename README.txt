1. Install project requirements:
    pip install -r requirements.txt

2. Create an OpenAI key and set it as your System's PATH environment variables as 'OPENAI_API_KEY':
    https://platform.openai.com/api-keys

3. Install OBS WebSocket Plugin:
    https://github.com/obsproject/obs-websocket/releases

4. Open OBS create a 'Text (GDI+)' object in OBS

5. Go to 'Tools' and find your WebSocket server details

6. Run main.py

7. Select your preferred input device from the list

8. Enter your server port and password, and source name

8. Press 'Start' to start listening to the input device and generating the transcription

9. Press 'Stop' to finish listening

You can find the complete recordings of your streams in recordings, and the complete transcriptions in the transcriptions folder