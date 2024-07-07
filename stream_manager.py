import pyaudio
import threading
import api
from file_handler import FileHandler
from obswebsocket import obsws, requests

class StreamManager:

    def __init__(self, device_index):

        OBS_SERVER_PORT = input("Enter server port: ")
        OBS_SERVER_PASSWORD = input("Enter server password: ")

        self.source_name = input("Enter source name: ")

        self.ws = obsws(host='localhost', port=OBS_SERVER_PORT, password=OBS_SERVER_PASSWORD)

        self.port_audio = pyaudio.PyAudio()

        self.recording_output_path = None
        self.snippet_path = None
        self.wav_file = None
        
        self.is_streaming = False
        self.snippet_length = 5
        self.DEVICE_INDEX = device_index
        self.FORMAT = pyaudio.paInt16
        self.DEVICE_INFO = self.port_audio.get_device_info_by_index(self.DEVICE_INDEX)
        self.SAMPLE_RATE = int(self.DEVICE_INFO['defaultSampleRate'])
        self.IS_INPUT = self.DEVICE_INFO['maxInputChannels'] > 0
        self.CHANNELS = int(self.DEVICE_INFO['maxInputChannels']) if self.IS_INPUT else int(self.DEVICE_INFO['maxOutputChannels'])
        self.SAMPLE_WIDTH = self.port_audio.get_sample_size(self.FORMAT)
        self.CAPTURE_DURATION = 1
        self.MIN_BUFFER_SIZE = int(self.SAMPLE_RATE * self.CAPTURE_DURATION)
        self.FRAMES_PER_BUFFER = self.SAMPLE_RATE * self.CHANNELS * self.CAPTURE_DURATION

        self.stream = self.port_audio.open(
                format=self.FORMAT,
                channels=self.CHANNELS,
                rate=self.SAMPLE_RATE,
                input=self.IS_INPUT,
                input_device_index=self.DEVICE_INDEX,
                frames_per_buffer=self.FRAMES_PER_BUFFER,
                start=False
            )

        FileHandler.create_folder('recordings')
        FileHandler.create_folder('transcriptions')
        FileHandler.create_folder('cache')

        self.stream_thread = threading.Thread(target=self.thread_target, daemon=True)

        self.ws.connect()    
    
    def thread_target(self):

        print('Thread target')
        
        self.recording_output_path = FileHandler.get_recording_output_path()
        self.snippet_path = FileHandler.get_snippet_path()

        self.wav_file = FileHandler.create_wav_file(
            output_path=self.recording_output_path,
            channels=self.CHANNELS,
            sample_rate=self.SAMPLE_RATE,
            sample_width=self.SAMPLE_WIDTH,
        )

        try:
            self.stream.start_stream()
            self.is_streaming = True
            print("Started stream")

            while self.is_streaming:
                self.update()
            
        except Exception as e:
            print(e)
    
    def start_streaming(self):
        print("Starting stream...")
        try:
            self.stream_thread.start()
        except RuntimeError:
            print('Thread already started')
    
    def stop_streaming(self):
        print("Stopping stream...")
        self.is_streaming = False

        if self.stream_thread is not None:
            self.stream_thread.join()

        if self.stream is not None:
            self.stream.stop_stream()

        if self.recording_output_path is not None:
            with open(self.recording_output_path, 'rb') as audio_file:
                transcription = api.transcribe_audio(audio_file)
                if transcription is not None:
                    FileHandler.write_to_file(FileHandler.get_transcription_output_path(), transcription)

        self.recording_output_path = None
        self.snippet_path = None

        print("Stopped stream")       

    def on_exit(self):
        print("Exiting...")
        self.stop_streaming()
        if self.stream is not None:
            self.stream.close()
        if self.port_audio is not None:
            self.port_audio.terminate()
        if self.wav_file is not None:
            self.wav_file.close()
           
    def update(self):
        print('Updating...')
        try:
            if self.stream is not None:
                data = self.stream.read(self.FRAMES_PER_BUFFER, exception_on_overflow=False)
                if data:
                    print('Has data')
                    self.wav_file.writeframes(data)
                    print('Updated')
                else:
                    print('No data')
            else:
                print('Stream is None')
        except IOError as e:
            print(f"IOError: {e}")

    def streaming_status(self):
        return self.is_streaming
    
    def request_snippet(self):
        wav_length = FileHandler.get_wav_length(self.recording_output_path)
        if wav_length > 1:
            print("Snippet request")
            FileHandler.snip_audio(self.recording_output_path, self.snippet_path, self.snippet_length)
    
    def send_to_obs(self, transcription):
        self.ws.call(requests.SetInputSettings(
            inputName=self.source_name,
            inputSettings={
                "text": transcription,
            }
        ))
    
    def request_transcription(self):
        wav_length = FileHandler.get_wav_length(self.recording_output_path)
        if wav_length > 1:
            print("Transcription request")
            try:
                with open(self.snippet_path, 'rb') as audio_file:
                    transcription = api.transcribe_audio(audio_file)
                    print(f"Transcription: {transcription}")
                    self.send_to_obs(transcription)
                    return transcription
            except Exception as e:
                print(e)
                return None
