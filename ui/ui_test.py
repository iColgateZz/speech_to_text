# ui.py
import customtkinter as ctk

def main() -> None:
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    app = ctk.CTk()
    app.title("Звук -> Текст")
    app.geometry("600x600")
    
    entry = ctk.CTkEntry(master=app, placeholder_text="Пиши сюда")
    entry.pack(pady=20)
    
    button = ctk.CTkButton(master=app, text="Кнопка", command=lambda: func(entry))
    button.pack(pady=20)

    segemented_button = ctk.CTkSegmentedButton(app, values=["Value 1", "Value 2", "Value 3"],
                                                     command=segmented_button_callback)
    segemented_button.set("Value 1")
    segemented_button.pack()
    
    tabview = ctk.CTkTabview(master=app)
    tabview.pack(padx=20, pady=20)

    tabview.add("tab 1")  # add tab at the end
    tabview.add("tab 2")  # add tab at the end
    tabview.set("tab 2")  # set currently visible tab

    button = ctk.CTkButton(master=tabview.tab("tab 1"))
    button.pack(padx=20, pady=20)

    app.mainloop()


def segmented_button_callback(value):
    print("segmented button clicked:", value)


def func(entry: ctk.CTkEntry) -> None:
    print(entry.get())

if __name__ == '__main__':
    main()