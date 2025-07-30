# ui.py
import customtkinter as ctk

def main() -> None:
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    app = ctk.CTk()
    app.title("App")
    app.geometry("600x600")
    
    app.mainloop()


if __name__ == '__main__':
    main()