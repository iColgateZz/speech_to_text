# SpeechToTextModel.py
import sounddevice as sd
import queue
import json
from vosk import Model, KaldiRecognizer
from svc import Svc

class SpeechToTextModel:
    def __init__(self, model_path: str, sample_rate: int, blocksize: int, svc: Svc):
        self.model = Model(model_path)
        self.recognizer = KaldiRecognizer(self.model, sample_rate)
        self.sample_rate = sample_rate
        self.blocksize = blocksize
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
