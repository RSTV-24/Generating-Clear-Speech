import os
import threading
import wave
from time import sleep
import keyboard
import pyaudio
import soundfile as sf
import torch
from transformers import WhisperForConditionalGeneration, WhisperProcessor

class Transcriber:
    def __init__(self, model="openai/whisper-base.en"):
        '''
        Initializes the transcription model and processor.

        Parameters:
        model (str): The model name or path. Default is "openai/whisper-base".
        '''
        self.model = WhisperForConditionalGeneration.from_pretrained(model)
        self.processor = WhisperProcessor.from_pretrained(model)

    def transcribe(self, file_path):
        '''
        Transcribes the given audio file and returns the transcription.

        Parameters:
        file_path (str): The path to the audio file.

        Returns:
        str: The transcription of the audio file.
        '''
        audio_input, sample_rate = sf.read(file_path)
        inputs = self.processor.feature_extractor(audio_input, sampling_rate=sample_rate, return_tensors="pt")

        with torch.no_grad():
            predicted_ids = self.model.generate(inputs["input_features"])

        transcription = self.processor.tokenizer.batch_decode(predicted_ids, skip_special_tokens=True)[0]
        print("Transcription: ", transcription)
        return transcription

class FileManager:
    def __init__(self, recordings_folder="recordings", transcription_file="transcriptions.txt"):
        '''
        Initializes the file manager with the specified recordings folder and transcription file.

        Parameters:
        recordings_folder (str): The folder where recordings will be saved. Default is "recordings".
        transcription_file (str): The file where transcriptions will be saved. Default is "transcriptions.txt".
        '''
        self.recordings_folder = recordings_folder
        self.transcription_file = transcription_file
        os.makedirs(self.recordings_folder, exist_ok=True)

    def save_transcription(self, file_path, transcription):
        '''
        Saves the transcription to the transcription file.

        Parameters:
        file_path (str): The path to the audio file.
        transcription (str): The transcription of the audio file.
        '''
        with open(self.transcription_file, "a") as f:
            f.write(f"{file_path},{transcription}\n")

    def get_new_recording_filename(self, counter):
        '''
        Gets a new filename for the recording based on the counter.

        Parameters:
        counter (int): The counter used for generating the filename.

        Returns:
        str: The new recording filename.
        '''
        return os.path.join(self.recordings_folder, f"recording_{counter}.wav")
    
    def get_latest_counter(self):
        '''
        Gets the latest counter from the transcription file.

        Returns:
        int: The latest counter value.
        '''
        if not os.path.exists(self.transcription_file):
            return 1
        max_counter = 1
        with open(self.transcription_file, "r") as f:
            for line in f:
                try:
                    filename = line.split(",")[0]
                    counter = int(filename.split("_")[-1].split(".")[0])
                    if counter > max_counter:
                        max_counter = counter
                except (IndexError, ValueError):
                    continue
        return max_counter + 1

class AudioRecorder:
    def __init__(self, file_manager, transcriber):
        '''
        Initializes the audio recorder with the file manager and transcriber.

        Parameters:
        file_manager (FileManager): The file manager instance.
        transcriber (Transcriber): The transcriber instance.
        '''
        self.file_manager = file_manager
        self.transcriber = transcriber
        self.counter = self.file_manager.get_latest_counter()
        self.is_recording = False

    def start_recording(self):
        '''
        Starts recording audio in a separate thread.
        '''
        self.is_recording = True
        threading.Thread(target=self.record_audio_continuously, daemon=True).start()

    def stop_recording(self):
        '''
        Stops recording audio.
        '''
        self.is_recording = False

    def record_audio_continuously(self):
        '''
        Continuously records audio while is_recording is True.
        '''
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 16000
        CHUNK = 1024

        audio = pyaudio.PyAudio()
        stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
        frames = []
        print("Recording...")

        try:
            while self.is_recording:
                data = stream.read(CHUNK)
                frames.append(data)
        finally:
            stream.stop_stream()
            stream.close()
            audio.terminate()
            print("Recording stopped.")

            wav_filename = self.file_manager.get_new_recording_filename(self.counter)
            with wave.open(wav_filename, 'wb') as wf:
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(audio.get_sample_size(FORMAT))
                wf.setframerate(RATE)
                wf.writeframes(b''.join(frames))

            transcription = self.transcriber.transcribe(wav_filename)
            self.file_manager.save_transcription(wav_filename, transcription)

            self.counter += 1

class HotkeyListener:
    def __init__(self, audio_recorder):
        '''
        Initializes the hotkey listener with the audio recorder.

        Parameters:
        audio_recorder (AudioRecorder): The audio recorder instance.
        '''
        self.audio_recorder = audio_recorder

    def listen_for_hotkey(self):
        '''
        Listens for the hotkey (Ctrl+Q) to start and stop recording.
        '''
        print("Started listening for hotkeys...")
        while True:
            keyboard.wait('ctrl+q')
            if not self.audio_recorder.is_recording:
                self.audio_recorder.start_recording()
            else:
                self.audio_recorder.stop_recording()

if __name__ == "__main__":
    '''
    Main execution starts here.
    Initializes instances of FileManager, Transcriber, AudioRecorder, and HotkeyListener.
    Starts the hotkey listener in a separate thread.
    Keeps the main thread alive to allow the hotkey listener to function.
    '''
    file_manager = FileManager()
    transcriber = Transcriber()
    audio_recorder = AudioRecorder(file_manager, transcriber)
    hotkey_listener = HotkeyListener(audio_recorder)

    # Start the hotkey listener in a separate thread
    listener_thread = threading.Thread(target=hotkey_listener.listen_for_hotkey, daemon=True)
    listener_thread.start()

    # Keep the main thread alive
    while True:
        sleep(0.5)
