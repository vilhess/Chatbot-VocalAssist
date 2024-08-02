import os
import warnings
import sounddevice as sd
from scipy.io.wavfile import write
from gtts import gTTS
import whisper
import ollama
import pyttsx4
from queue import Queue
from threading import Thread
# Suppress warnings
warnings.filterwarnings("ignore")

# Constants
AUDIO_DIR = 'audio'
OUTPUT_WAV = os.path.join(AUDIO_DIR, 'output.wav')
ANSWER_MP3 = os.path.join(AUDIO_DIR, 'answer.mp3')
FS = 44100    # Sample rate
DURATION = 3  # Duration of recording in seconds
LANGUAGE = 'fr'

# Ensure the audio directory exists
os.makedirs(AUDIO_DIR, exist_ok=True)

def get_my_question(duration=DURATION, filepath=OUTPUT_WAV):
    print("Recording...")
    audio_data = sd.rec(int(duration * FS), samplerate=FS, channels=1, dtype='int16')
    sd.wait()
    print("Recording complete")
    write(filepath, FS, audio_data)

def speech_to_text(model, filepath=OUTPUT_WAV):
    result = model.transcribe(filepath)
    return result["text"]

# Load Whisper model
model = whisper.load_model("base")

# Initial message for the assistant
messages = [{'role': 'system', 'content': "Tu es un client de boulangerie français, tu viens pour acheter ton pain dans la boulangerie de ta ville"}]

def say_loop():
    engine = pyttsx4.init()
    while True:
        engine.say(q.get())
        engine.runAndWait()
        q.task_done()


q = Queue()
t = Thread(target=say_loop)
t.daemon = True
t.start()

# Main loop for interaction
for _ in range(3):
    get_my_question()
    text = speech_to_text(model)
    messages.append({'role': 'user', 'content': text})
    answer = ollama.chat(
        model='llama3.1',
        messages=messages,
        stream=False
    )
    answer_content = answer['message']['content']
    myobj = gTTS(text=answer_content, lang="fr", slow=False)
    myobj.save("audio/answer.mp3")
    _ = os.system("afplay audio/answer.mp3")
    
    messages.append({'role': 'assistant', 'content': answer_content})

print('Interaction complete')
