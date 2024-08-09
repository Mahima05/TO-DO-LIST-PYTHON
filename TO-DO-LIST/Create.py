import customtkinter as ctk
import sqlite3
from tkinter import messagebox

class CreateApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Create New List")
        self.geometry("400x500")

        # List name
        self.list_name_label = ctk.CTkLabel(self, text="List Name:")
        self.list_name_label.pack(pady=(20, 5))
        self.list_name_entry = ctk.CTkEntry(self)
        self.list_name_entry.pack(pady=5)

        # Task
        self.task_label = ctk.CTkLabel(self, text="Task:")
        self.task_label.pack(pady=5)
        self.task_entry = ctk.CTkEntry(self)
        self.task_entry.pack(pady=5)

        # Add Task button
        self.add_task_button = ctk.CTkButton(self, text="Add Task", command=self.add_task)
        self.add_task_button.pack(pady=10)

        # Task Textbox
        self.task_textbox = ctk.CTkTextbox(self, width=350, height=150)
        self.task_textbox.pack(pady=10)

        # Back button
        self.back_button = ctk.CTkButton(self, text="Back", command=self.back)
        self.back_button.pack(pady=20)

        self.tasks = []
        self.username = "current_user"  # This should be dynamically set based on the logged-in user

        self.create_table()

    def create_table(self):
        conn = sqlite3.connect('todo.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                username TEXT NOT NULL,
                list_name TEXT NOT NULL,
                task TEXT NOT NULL,
                status TEXT DEFAULT 'ongoing'
            )
        ''')
        conn.commit()
        conn.close()

    def add_task(self):
        list_name = self.list_name_entry.get()
        task = self.task_entry.get()

        if not list_name or not task:
            messagebox.showwarning("Input Error", "Please enter both list name and task")
            return

        self.tasks.append(task)
        self.task_textbox.insert(ctk.END, task + "\n")
        self.task_entry.delete(0, ctk.END)

        # Save to database
        conn = sqlite3.connect('todo.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (username, list_name, task, status) VALUES (?, ?, ?, ?)",
                       (self.username, list_name, task, 'ongoing'))
        conn.commit()
        conn.close()

    def back(self):
        self.destroy()
        from Dashboard import DashboardApp
        DashboardApp().mainloop()

if __name__ == "__main__":
    app = CreateApp()
    app.mainloop()
