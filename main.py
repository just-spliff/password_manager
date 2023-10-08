import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import json
import pyperclip
from pass_gen import password_generator
from settings import *

class Logo(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color=BG_COLOR)
        self.grid(row=0, column=0)
        
        # Load the image as a PIL.Image.Image instance
        logo_img = Image.open("logo.png")
        
        # Create a CTkImage with the loaded image
        self.logo = ctk.CTkImage(light_image=logo_img, 
                                 dark_image=logo_img,
                                 size=(200, 200))

        # Create a label as an intermediary and set the background to the image
        label = ctk.CTkLabel(self, image=self.logo, text='', bg_color=BG_COLOR)
        label.grid(row=0,column=0, sticky='nsew')  # Fill the entire frame

class Buttons(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color=BG_COLOR)
        self.grid(row=4,column=0,sticky='nsew',padx=50)
        
        self.rowconfigure(0,weight=1)
        self.columnconfigure((0,1,2),weight=1)
        
        font = ctk.CTkFont(family=FONT, size=BTN_FONT_SIZE,weight='bold')
        
        self.search_button = ctk.CTkButton(self, 
                                           text="Search", 
                                           font=font, 
                                           command=self.search_password,
                                           height=40,
                                           fg_color=MAIN_COLOR,
                                           text_color=BG_COLOR,
                                           corner_radius=BUTTON_CORNER_RADIUS)
        self.generate_button = ctk.CTkButton(self, 
                                             text="Generate", 
                                             font=font, 
                                             command=self.get_password,
                                             height=40,
                                             fg_color=MAIN_COLOR,
                                             text_color=BG_COLOR,
                                             corner_radius=BUTTON_CORNER_RADIUS)
        self.add_button = ctk.CTkButton(self, 
                                        text="+", 
                                        font=font, 
                                        command=self.save_password,
                                        width=50,
                                        height=50,
                                        fg_color=MAIN_COLOR,
                                        text_color=BG_COLOR,
                                        corner_radius=BUTTON_CORNER_RADIUS)
        
        self.search_button.grid(row=0, column=0, pady=10)
        self.generate_button.grid(row=0, column=2, pady=10)
        self.add_button.grid(row=0, column=1, pady=10)

    def get_password(self):
        password = password_generator()
        pyperclip.copy(password)
        password_entry.delete(0, "end")
        password_entry.insert(0, password)

    def save_password(self):
        website = website_entry.get()
        email = email_entry.get()
        password = password_entry.get()
        if len(website) == 0 or len(password) == 0:
            messagebox.showinfo(title="Oops", message="Please make sure you have not left any fields empty")
        else:
            is_ok = messagebox.askokcancel(title="Confirm entries", message=f"These are the details you entered\n"
                                                                             f"Email: {email}\n"
                                                                             f"Password: {password}\n"
                                                                             f"Is it okay to save ?")
            if is_ok:
                pyperclip.copy(password)
                new_entry_in_json = {
                    website: {
                        "Email": email,
                        "Password": password
                    }
                }
                self.database_manager(new_entry_in_json)

    def database_manager(self, new_user_entry):
        try:
            with open("data.json", mode="r") as old_password_file:
                password_data = json.load(old_password_file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            with open("data.json", mode="w") as new_password_file:
                json.dump(new_user_entry, new_password_file, indent=4)
        else:
            password_data.update(new_user_entry)
            with open("data.json", mode="w") as old_password_file:
                json.dump(password_data, old_password_file, indent=4)
        finally:
            website_entry.delete(0, "end")
            password_entry.delete(0, "end")

    def search_password(self):
        # Getting user website entry
        website = website_entry.get()
        # Get password data
        if len(website) == 0:
            messagebox.showinfo(title="Oops", message="Please enter a website to search")
        else:
            # Try to see if password files exit ,is in JSON, and not blank
            try:
                # seeing if there is any old passwords data file
                with open("data.json", mode="r") as old_password_file:
                    # reading old password data
                    password_data = json.load(old_password_file)
            # If there is no password file, or is in incorrect JSON format or is blank
            except (FileNotFoundError, json.decoder.JSONDecodeError):
                messagebox.showinfo(title="No passwords saved", message="Sorry, you have not saved any password before")
            else:
                # If the searched website is in password data
                if website in password_data:
                    email = password_data[website]["Email"]
                    password = password_data[website]["Password"]
                    # Save to clipboard message box
                    is_clipboard = messagebox.askokcancel(title=website, message=f"Email: {email}\nPassword: {password}"
                                                                                 f"\n\nSave to clipboard ?")
                    # Save to clipboard
                    if is_clipboard:
                        # saving password to clipboard
                        pyperclip.copy(password)
                        messagebox.showinfo(title="Saved to clipboard", message="Password has been saved to clipboard")
                # IF the searched website is not in the database
                else:
                    messagebox.showinfo(title="Password not saved for this website", message=f"The password for {website}\n"
                                                                                             f"has not been saved")

class PasswordManager(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color=BG_COLOR)
        
        self.title('Password Manager')
        self.geometry('700x600')
        self.resizable(False,False)
        
        self.logo = Logo(self)
        
        self.rowconfigure((0,1,2,3,4),weight=1)
        self.columnconfigure(0,weight=1)
        
        font = ctk.CTkFont(family=FONT, size= ENTRY_FONT_SIZE, weight='bold')
        
        global website_entry, email_entry, password_entry
        website_entry = ctk.CTkEntry(self, 
                                     width=400,
                                     height= 50, 
                                     bg_color=BG_COLOR, 
                                     fg_color=MAIN_COLOR, 
                                     font=font,
                                     text_color=BG_COLOR)
        email_entry = ctk.CTkEntry(self, 
                                   width=400,
                                   height=50, 
                                   bg_color=BG_COLOR, 
                                   fg_color=MAIN_COLOR, 
                                   font=font,
                                   text_color=BG_COLOR)
        password_entry = ctk.CTkEntry(self, 
                                      width=400,
                                      height=50, 
                                      bg_color=BG_COLOR, 
                                      fg_color=MAIN_COLOR, 
                                      font=font,
                                      text_color=BG_COLOR)
        
        website_entry.grid(row=1, column=0, pady=10)
        email_entry.grid(row=2, column=0, pady=10)
        password_entry.grid(row=3, column=0, pady=10)
        
        website_entry.focus()
        email_entry.insert(0, "example@email.com")
        password_entry.insert(0,"************")

        self.buttons = Buttons(self)
        
        self.mainloop()

if __name__ == "__main__":
    PasswordManager()
