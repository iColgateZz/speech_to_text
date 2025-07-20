# main.py
from google_doc_svc import GoogleDocSvc
from speech_to_text_model import SpeechToTextModel

MODEL_PATH = "vosk-model-small-ru-0.22"
SAMPLE_RATE = 16_000
BLOCKSIZE = 4_000

def main():
    file_name = input("Введите название файла: ")
    svc = GoogleDocSvc(file_name)
    stt = SpeechToTextModel(MODEL_PATH, SAMPLE_RATE, BLOCKSIZE, svc)
    stt.run()

if __name__ == "__main__":
    main()
