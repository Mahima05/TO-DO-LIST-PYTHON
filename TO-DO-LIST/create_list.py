import customtkinter as ctk
from tkinter import messagebox
from tkcalendar import DateEntry
import sqlite3
import random

# Database setup
conn = sqlite3.connect('todo_list.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS lists (
                list_id INTEGER PRIMARY KEY,
                list_name TEXT NOT NULL)''')

c.execute('''CREATE TABLE IF NOT EXISTS tasks (
                task_id INTEGER PRIMARY KEY AUTOINCREMENT,
                list_id INTEGER,
                task TEXT NOT NULL,
                priority TEXT NOT NULL,
                FOREIGN KEY(list_id) REFERENCES lists(list_id))''')
conn.commit()

class CreateListWindow(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Create a New List")
        self.geometry('600x400+300+200')
        self.list_id = random.randint(10000, 99999)
        self.tasks = []
        self.create_widgets()

    def create_widgets(self):
        label_title = ctk.CTkLabel(self, text=f"List ID: {self.list_id}", font=("Arial", 16))
        label_title.place(x=50, y=20)

        label_name = ctk.CTkLabel(self, text="List Name:", font=("Arial", 16))
        label_name.place(x=50, y=60)
        self.entry_name = ctk.CTkEntry(self, width=200)
        self.entry_name.place(x=150, y=60)

        label_task = ctk.CTkLabel(self, text="Task:", font=("Arial", 16))
        label_task.place(x=50, y=100)
        self.entry_task = ctk.CTkEntry(self, width=200)
        self.entry_task.place(x=150, y=100)

        label_priority = ctk.CTkLabel(self, text="Priority:", font=("Arial", 16))
        label_priority.place(x=50, y=140)

        self.priority_var = ctk.StringVar(value="low")

        self.high_priority = ctk.CTkRadioButton(self, text="", variable=self.priority_var, value="high")
        self.high_priority.place(x=150, y=140)
        high_priority_label = ctk.CTkLabel(self, text="High", fg_color="red", width=15, height=15, corner_radius=10)
        high_priority_label.place(x=170, y=140)

        self.medium_priority = ctk.CTkRadioButton(self, text="", variable=self.priority_var, value="medium")
        self.medium_priority.place(x=220, y=140)
        medium_priority_label = ctk.CTkLabel(self, text="Medium", fg_color="yellow", width=15, height=15, corner_radius=10)
        medium_priority_label.place(x=240, y=140)

        self.low_priority = ctk.CTkRadioButton(self, text="", variable=self.priority_var, value="low")
        self.low_priority.place(x=290, y=140)
        low_priority_label = ctk.CTkLabel(self, text="Low", fg_color="green", width=15, height=15, corner_radius=10)
        low_priority_label.place(x=310, y=140)

        add_task_button = ctk.CTkButton(self, text="Add Task", command=self.add_task)
        add_task_button.place(x=150, y=180)

        self.task_listbox = ctk.CTkListbox(self, width=400, height=150)
        self.task_listbox.place(x=50, y=220)

        save_list_button = ctk.CTkButton(self, text="Save List", command=self.save_list)
        save_list_button.place(x=250, y=380)

    def add_task(self):
        task = self.entry_task.get()
        priority = self.priority_var.get()
        if task:
            self.tasks.append((task, priority))
            c.execute("INSERT INTO tasks (list_id, task, priority) VALUES (?, ?, ?)",
                      (self.list_id, task, priority))
            conn.commit()
            self.update_task_list()
            self.entry_task.delete(0, 'end')  # Clear the task entry after adding
        else:
            messagebox.showerror("Error", "Task cannot be empty")

    def update_task_list(self):
        self.task_listbox.delete(0, 'end')
        sorted_tasks = sorted(self.tasks, key=lambda x: {'high': 0, 'medium': 1, 'low': 2}[x[1]])
        for task, priority in sorted_tasks:
            self.task_listbox.insert('end', f"{task} ({priority})")

    def save_list(self):
        list_name = self.entry_name.get()
        if not list_name:
            messagebox.showerror("Error", "List name cannot be empty")
            return

        c.execute("INSERT INTO lists (list_id, list_name) VALUES (?, ?)",
                  (self.list_id, list_name))
        conn.commit()

        messagebox.showinfo("List Saved", f"List '{list_name}' with ID {self.list_id} has been saved successfully!")
        self.destroy()

# Example main app code to show how to open the CreateListWindow
if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("300x200")

    def open_create_list():
        CreateListWindow(root)

    create_list_button = ctk.CTkButton(root, text="Create a New List", command=open_create_list)
    create_list_button.pack(pady=20)

    root.mainloop()
