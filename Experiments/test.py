from time import sleep
import keyboard
import threading
import pyaudio
import wave
import os
from transformers import WhisperForConditionalGeneration, WhisperProcessor
import torch
import soundfile as sf
from pynput.keyboard import Controller, Key

counter = 1

recordings_folder = "recordings"

os.makedirs(recordings_folder, exist_ok=True)

is_recording = False


def transcribe_audio(file_path):
    model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-base")
    processor = WhisperProcessor.from_pretrained("openai/whisper-base")
    audio_input, sample_rate = sf.read(file_path)
    
    inputs = processor.feature_extractor(audio_input, sampling_rate=sample_rate, return_tensors="pt")

    with torch.no_grad():
        predicted_ids = model.generate(inputs["input_features"])

    transcription = processor.tokenizer.batch_decode(predicted_ids, skip_special_tokens=True)[0]
    print("Transcription: ", transcription)
    return transcription

def save_transcription_to_file(file_path, transcription):
    with open("transcriptions.txt", "a") as f:
        f.write(f"{file_path}: {transcription}\n")

def record_audio_continuously():
    global is_recording
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    CHUNK = 1024

    audio = pyaudio.PyAudio()

    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    frames = []
    print("Recording...")

    try:
        while is_recording:
            data = stream.read(CHUNK)
            frames.append(data)

            if not is_recording:
                break

    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()
        print("Recording stopped.")

        output_filename = f"recording_{counter}.wav"
        wav_filename = os.path.join(recordings_folder, output_filename)
        with wave.open(wav_filename, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(audio.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
        
        transcription = transcribe_audio(wav_filename)

        save_transcription_to_file(wav_filename, transcription)

def show_popup():
    global is_recording

    def on_close(response):
        global is_recording
        is_recording = False if response else True
    
    keyboard.wait('ctrl+q')
    on_close(True)

def listen_for_hotkey():
    global is_recording
    global counter
    print("Started..")
    while True:
        keyboard.wait('ctrl+q')
        
        if not is_recording:
            is_recording = True
            threading.Thread(target=show_popup, daemon=True).start()
            record_audio_continuously()
            counter += 1

listener_thread = threading.Thread(target=listen_for_hotkey, daemon=True)
listener_thread.start()

while True:
    sleep(0.5)
    pass
