# main.py
from svc.google_doc.google_doc_svc import GoogleDocSvc
from model.speech_to_text_model import SpeechToTextModel
import customtkinter as ctk
import threading

def main():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    app = ctk.CTk()
    app.title("Звук -> Текст")
    app.geometry("600x600")
    
    label = ctk.CTkLabel(master=app, text="Введите название файла")
    label.pack(pady=20)
    
    entry = ctk.CTkEntry(master=app, placeholder_text="Название файла")
    entry.pack(pady=20)
    
    button = ctk.CTkButton(master=app, text="Начать", command=lambda: start_model(app, entry))
    button.pack(pady=20)
    
    button_stop = ctk.CTkButton(master=app, text="Остановить", command=lambda: stop_model(app))
    button_stop.pack(pady=20)
    
    app.mainloop()


def start_model(app: ctk.CTk, entry: ctk.CTkEntry):
    file_name = entry.get()
    svc = GoogleDocSvc(file_name)
    stt = SpeechToTextModel(svc)
    app.stt = stt
    threading.Thread(target=stt.run, daemon=True).start()
    
def stop_model(app: ctk.CTk):
    app.stt.stop()
    print("Остановлено")


if __name__ == "__main__":
    main()
