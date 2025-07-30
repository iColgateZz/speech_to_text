# main.py
from svc.google_doc.google_doc_svc import GoogleDocSvc
from model.speech_to_text_model import SpeechToTextModel


def main():
    file_name = input("Введите название файла: ")
    svc = GoogleDocSvc(file_name)
    stt = SpeechToTextModel(svc)
    stt.run()

if __name__ == "__main__":
    main()
