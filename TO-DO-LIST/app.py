import customtkinter as ctk
from tkcalendar import DateEntry
import sqlite3
from tkinter import messagebox
from create_list import CreateListWindow

# Database setup
conn = sqlite3.connect('todo_list.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                password TEXT NOT NULL,
                employment_status TEXT,
                dob TEXT)''')
conn.commit()


# Main Application
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry('1200x600+150+100')
        self.title('TODO List Application')
        ctk.set_appearance_mode('dark')
        ctk.set_default_color_theme('blue')

        self.login_frame = LoginFrame(self)
        self.register_frame = RegisterFrame(self)
        self.dashboard_frame = Dashboard(self)

        self.login_frame.pack(fill='both', expand=True)

    def show_login_frame(self):
        self.register_frame.pack_forget()
        self.dashboard_frame.pack_forget()
        self.login_frame.pack(fill='both', expand=True)

    def show_register_frame(self):
        self.login_frame.pack_forget()
        self.dashboard_frame.pack_forget()
        self.register_frame.pack(fill='both', expand=True)

    def show_dashboard(self):
        self.login_frame.pack_forget()
        self.register_frame.pack_forget()
        self.dashboard_frame.pack(fill='both', expand=True)


class LoginFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        label_title = ctk.CTkLabel(self, text="TODO List Login", font=("Arial", 24))
        label_title.place(x=550, y=50)

        label_name = ctk.CTkLabel(self, text="Name:", font=("Arial", 16))
        label_name.place(x=400, y=200)
        self.entry_name = ctk.CTkEntry(self, width=200)
        self.entry_name.place(x=500, y=200)

        label_password = ctk.CTkLabel(self, text="Password:", font=("Arial", 16))
        label_password.place(x=400, y=250)
        self.entry_password = ctk.CTkEntry(self, width=200, show='*')
        self.entry_password.place(x=500, y=250)

        login_button = ctk.CTkButton(self, text="Login", command=self.login)
        login_button.place(x=500, y=300)

        register_button = ctk.CTkButton(self, text="Register", command=self.master.show_register_frame)
        register_button.place(x=580, y=300)

        self.show_password_var = ctk.StringVar()
        show_password_checkbox = ctk.CTkCheckBox(self, text="Show Password", variable=self.show_password_var,
                                                 command=self.toggle_password_visibility)
        show_password_checkbox.place(x=500, y=280)

    def toggle_password_visibility(self):
        if self.show_password_var.get() == '1':
            self.entry_password.configure(show='')
        else:
            self.entry_password.configure(show='*')

    def login(self):
        username = self.entry_name.get()
        password = self.entry_password.get()

        c.execute("SELECT * FROM users WHERE name=? AND password=?", (username, password))
        result = c.fetchone()

        if result:
            self.master.show_dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")


class RegisterFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        label_title = ctk.CTkLabel(self, text="TODO List Registration", font=("Arial", 24))
        label_title.place(x=500, y=50)

        label_name = ctk.CTkLabel(self, text="Name:", font=("Arial", 16))
        label_name.place(x=400, y=150)
        self.entry_name = ctk.CTkEntry(self, width=200)
        self.entry_name.place(x=600, y=150)

        label_password = ctk.CTkLabel(self, text="Password:", font=("Arial", 16))
        label_password.place(x=400, y=200)
        self.entry_password = ctk.CTkEntry(self, width=200, show='*')
        self.entry_password.place(x=600, y=200)

        label_employment = ctk.CTkLabel(self, text="Employment Status:", font=("Arial", 16))
        label_employment.place(x=400, y=250)
        self.entry_employment = ctk.CTkEntry(self, width=200)
        self.entry_employment.place(x=600, y=250)

        label_dob = ctk.CTkLabel(self, text="Date of Birth:", font=("Arial", 16))
        label_dob.place(x=400, y=300)
        self.entry_dob = DateEntry(self, width=19, background='darkblue', foreground='white', borderwidth=2)
        self.entry_dob.place(x=600, y=300)

        register_button = ctk.CTkButton(self, text="Register", command=self.register)
        register_button.place(x=600, y=350)

        self.show_password_var = ctk.StringVar()
        show_password_checkbox = ctk.CTkCheckBox(self, text="Show Password", variable=self.show_password_var,
                                                 command=self.toggle_password_visibility)
        show_password_checkbox.place(x=600, y=230)

    def toggle_password_visibility(self):
        if self.show_password_var.get() == '1':
            self.entry_password.configure(show='')
        else:
            self.entry_password.configure(show='*')

    def register(self):
        name = self.entry_name.get()
        password = self.entry_password.get()
        employment_status = self.entry_employment.get()
        dob = self.entry_dob.get()

        if name and password and employment_status and dob:
            c.execute("INSERT INTO users (name, password, employment_status, dob) VALUES (?, ?, ?, ?)",
                      (name, password, employment_status, dob))
            conn.commit()
            messagebox.showinfo("Registration Success", "You have been registered successfully!")
            self.master.show_login_frame()
        else:
            messagebox.showerror("Error", "All fields are required!")

class Dashboard(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        label_title = ctk.CTkLabel(self, text="Dashboard", font=("Arial", 24))
        label_title.place(x=550, y=50)

        # You can add more widgets to the dashboard here
        welcome_label = ctk.CTkLabel(self, text="Welcome to the Dashboard!", font=("Arial", 20))
        welcome_label.place(x=500, y=150)

        # Create buttons
        create_list_button = ctk.CTkButton(self, text="Create a New List", command=self.create_new_list)
        create_list_button.place(x=500, y=250)

        modify_list_button = ctk.CTkButton(self, text="Modify an Existing List", command=self.modify_existing_list)
        modify_list_button.place(x=500, y=300)

        track_list_button = ctk.CTkButton(self, text="Track a List", command=self.track_list)
        track_list_button.place(x=500, y=350)

        # Example of a logout button
        logout_button = ctk.CTkButton(self, text="Logout", command=self.logout)
        logout_button.place(x=600, y=400)

    def create_new_list(self):
        CreateListWindow(self.master)

    def modify_existing_list(self):
        # Placeholder function for modifying an existing list
        messagebox.showinfo("Modify an Existing List", "Functionality to modify an existing list goes here.")

    def track_list(self):
        # Placeholder function for tracking a list
        messagebox.showinfo("Track a List", "Functionality to track a list goes here.")

    def logout(self):
        self.master.show_login_frame()



if __name__ == "__main__":
    app = App()
    app.mainloop()
