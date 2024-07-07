import wave
import os
from pydub import AudioSegment
from datetime import datetime

class FileHandler:

    @staticmethod
    def create_folder(path):
        os.makedirs(path, exist_ok=True)

    @staticmethod
    def write_to_file(path, text):
        with open(path, 'w') as file: file.write(text)

    @staticmethod
    def create_wav_file(output_path, channels, sample_width, sample_rate):
        try:
            wf = wave.open(output_path, 'wb')
            wf.setnchannels(channels)
            wf.setsampwidth(sample_width)
            wf.setframerate(sample_rate)
            return wf
        except Exception as e:
            print(f"Failed to create wav file: {e}")

    @staticmethod
    def get_wav_length(file_path):
        try:
            audio = AudioSegment.from_wav(file_path)
            duration = len(audio) / 1000.0  # Convert milliseconds to seconds
            return duration
        except Exception as e:
            print(e)
            return 0

    @staticmethod
    def snip_audio(input_path, output_path, snippet_length):
        if os.path.exists(input_path):
            try:
                audio = AudioSegment.from_file(input_path)
                start_time = max(0, len(audio) - snippet_length * 1000)
                audio_segment = audio[start_time:]
                audio_segment.export(output_path, format="wav")
            except FileNotFoundError as e:
                print(e)
    
    @staticmethod
    def get_snippet_path():
        return "cache/snippet.wav"

    @staticmethod
    def get_recording_output_path():
        return "recordings/recording-" + datetime.now().strftime("%m-%H-%M-%d-%Y") + '.wav'
    
    @staticmethod
    def get_transcription_output_path():
        return "transcriptions/transcription-" + datetime.now().strftime("%m-%H-%M-%d-%Y") + '.txt'
