import pygame
import pyaudio
from gui import Button, Text, screen, WHITE, GREEN, RED
from stream_manager import StreamManager

SOURCE_NAME = 'python-transcription'

def listDevices():
    p = pyaudio.PyAudio()
    for i in range(p.get_device_count()):
        device_info = p.get_device_info_by_index(i)
        if (int(device_info['maxInputChannels'] > 0) and int(device_info['maxOutputChannels'] == 0)):
            print(f"Index {i}: {device_info['name']}")
            print(f"  Default Sample Rate: {device_info['defaultSampleRate']}")
            print(f"  Input Channels: {device_info['maxInputChannels']}")
            #print(f"  Output Channels: {device_info['maxOutputChannels']}")
            #print(f"  Host API: {device_info['hostApi']}")
            print("-" * 40)

def main():

    running = False
    transcription = "Press Start"
    last_snippet_time = 0
    last_transcription_time = 0

    # Input device selection
    listDevices()
    device_index = int(input('Select device index: '))
    stream_manager = StreamManager(device_index)

    # Pygame GUI
    pygame.init()

    start_button = Button(50, 50, 100, 40, "Start", GREEN, stream_manager.start_streaming)
    stop_button = Button(150, 50, 100, 40, "Stop", RED, stream_manager.stop_streaming)
    transcription_text = Text(50, 100, 200, 200, transcription)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stream_manager.on_exit()
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.is_pressed(event.pos):
                    start_button.action()
                elif stop_button.is_pressed(event.pos):
                    stop_button.action()
        
        # Periodic snippet
        if stream_manager.streaming_status() and (pygame.time.get_ticks() - last_snippet_time) >= 1000:
            stream_manager.request_snippet()
            last_snippet_time = pygame.time.get_ticks()
        
        # Periodic transcription request
        if stream_manager.streaming_status() and ((pygame.time.get_ticks() - last_transcription_time) >= 500):
            transcription = stream_manager.request_transcription()
            if transcription is not None:
                transcription_text.set_text(transcription)
            last_transcription_time = pygame.time.get_ticks()
        
        # Update screen
        screen.fill(WHITE)
        start_button.draw(screen)
        stop_button.draw(screen)
        transcription_text.draw(screen)
        pygame.display.flip()

    # Clean up
    stream_manager.on_exit()
    pygame.quit()
    

if __name__ == '__main__':
    main()