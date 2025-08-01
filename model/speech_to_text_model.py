# SpeechToTextModel.py
import sounddevice as sd
import queue
import json
from vosk import Model, KaldiRecognizer
from svc.svc import Svc
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "vosk-model-small-ru-0.22")
SAMPLE_RATE = 16_000
BLOCKSIZE = 4_000

class SpeechToTextModel:
    def __init__(self, svc: Svc):
        self.model = Model(MODEL_PATH)
        self.recognizer = KaldiRecognizer(self.model, SAMPLE_RATE)
        self.sample_rate = SAMPLE_RATE
        self.blocksize = BLOCKSIZE
        self.svc = svc
        self.q = queue.Queue()
        self.running = False

    def _callback(self, indata, frames, time, status):
        self.q.put(bytes(indata))

    def run(self):
        self.running = True
        try:
            with sd.RawInputStream(
                samplerate=self.sample_rate,
                blocksize=self.blocksize,
                dtype='int16',
                channels=1,
                callback=self._callback
            ):
                print("Говорите")
                while self.running:
                    data = self.q.get()
                    if self.recognizer.AcceptWaveform(data):
                        result = self.recognizer.Result()
                        text = json.loads(result).get('text', '')
                        if text:
                            self.svc.write(text)
                            print(text)
                    else:
                        partial = self.recognizer.PartialResult()
        except KeyboardInterrupt:
            print("Завершение работы")
            
    def stop(self):
        self.running = False
