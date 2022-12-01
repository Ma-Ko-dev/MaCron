# import subprocess
import tkinter as tk
from tkinter import ttk
import customtkinter

# Just something to test subprocess
# subprocess.run(["python", 'F:\\Users\\Gariot\\Documents\\Udemy\\100DaysOfCode\\Day 035\\tkinter_guitest.py'])

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # config window
        self.geometry("700x470")
        self.title("GarryCron")

        self.button_add = customtkinter.CTkButton(master=self, text="Add new Script", command=self.add_entry)
        self.button_add.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.seperator = ttk.Separator(master=self, orient="horizontal")
        self.seperator.grid(row=1, column=0, padx=10, pady=5, sticky="we")

        self.frame_scripts = customtkinter.CTkFrame(master=self, width=680, height=410, border_width=3, corner_radius=10)
        self.frame_scripts.grid_propagate(False)
        self.frame_scripts.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")

# ##############
        self.label1 = customtkinter.CTkLabel(master=self.frame_scripts, text="Hallo", bg_color="transparent", font=("Helvetica", 16))
        self.label1.grid(row=0, column=0, padx=10, pady=5, sticky="wens")

        self.seperator = ttk.Separator(master=self.frame_scripts, orient="horizontal")
        self.seperator.grid(row=1, column=0, padx=10, sticky="we")

        self.label1 = customtkinter.CTkLabel(master=self.frame_scripts, text="Hallo", bg_color="transparent", font=("Helvetica", 16))
        self.label1.grid(row=2, column=0, padx=10, pady=5, sticky="wens")


    def add_entry(self):
        print("Add function called")


if __name__ == "__main__":
    app = App()
    app.mainloop()
