# SpeechToTextModel.py
import sounddevice as sd
import queue
import json
from vosk import Model, KaldiRecognizer
from svc.svc import Svc

MODEL_PATH = "vosk-model-small-ru-0.22"
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

    def _callback(self, indata, frames, time, status):
        self.q.put(bytes(indata))

    def run(self):
        try:
            with sd.RawInputStream(
                samplerate=self.sample_rate,
                blocksize=self.blocksize,
                dtype='int16',
                channels=1,
                callback=self._callback
            ):
                print("Говорите")
                while True:
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
