import customtkinter as ctk
import sqlite3
from tkinter import messagebox, Listbox, END


class ModifyApp(ctk.CTk):
    def __init__(self, username):
        super().__init__()

        self.title("Modify Existing List")
        self.geometry("1200x600+150+100")

        self.username = username

        # List selection
        self.list_label = ctk.CTkLabel(self, text="Select List:")
        self.list_label.pack(pady=(20, 5))
        self.listbox = Listbox(self, width=50, height=5)
        self.listbox.pack(pady=5)
        self.load_lists()
        self.listbox.bind('<<ListboxSelect>>', self.on_list_select)

        # Task selection
        self.task_label = ctk.CTkLabel(self, text="Tasks in Selected List:")
        self.task_label.pack(pady=5)
        self.task_listbox = Listbox(self, width=50, height=10)
        self.task_listbox.pack(pady=5)

        # Modify task status
        self.status_label = ctk.CTkLabel(self, text="Modify Task Status:")
        self.status_label.pack(pady=5)
        self.status_entry = ctk.CTkEntry(self)
        self.status_entry.pack(pady=5)

        self.modify_status_button = ctk.CTkButton(self, text="Modify Status", command=self.modify_status)
        self.modify_status_button.pack(pady=10)

        # Delete task
        self.delete_task_button = ctk.CTkButton(self, text="Delete Task", command=self.delete_task)
        self.delete_task_button.pack(pady=10)

        # Add new task
        self.new_task_label = ctk.CTkLabel(self, text="New Task:")
        self.new_task_label.pack(pady=5)
        self.new_task_entry = ctk.CTkEntry(self)
        self.new_task_entry.pack(pady=5)

        self.add_task_button = ctk.CTkButton(self, text="Add Task", command=self.add_task)
        self.add_task_button.pack(pady=10)

        # Delete list
        self.delete_list_button = ctk.CTkButton(self, text="Delete List", command=self.delete_list)
        self.delete_list_button.pack(pady=10)

        # Back button
        self.back_button = ctk.CTkButton(self, text="Back", command=self.back)
        self.back_button.pack(pady=20)

    def load_lists(self):
        self.listbox.delete(0, END)
        conn = sqlite3.connect('todo.db')
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT list_name FROM tasks WHERE username=?", (self.username,))
        lists = cursor.fetchall()
        conn.close()

        for lst in lists:
            self.listbox.insert(END, lst[0])

    def on_list_select(self, event):
        selected_list = self.listbox.get(self.listbox.curselection())
        self.load_tasks(selected_list)

    def load_tasks(self, list_name):
        self.task_listbox.delete(0, END)
        conn = sqlite3.connect('todo.db')
        cursor = conn.cursor()
        cursor.execute("SELECT task, status FROM tasks WHERE username=? AND list_name=?", (self.username, list_name))
        tasks = cursor.fetchall()
        conn.close()

        for task, status in tasks:
            self.task_listbox.insert(END, f"{task} ({status})")

    def modify_status(self):
        selected_task_index = self.task_listbox.curselection()
        if not selected_task_index:
            messagebox.showwarning("Input Error", "Please select a task to modify")
            return

        selected_task = self.task_listbox.get(selected_task_index).split(" (")[0]
        new_status = self.status_entry.get().strip()
        list_name = self.listbox.get(self.listbox.curselection())

        if selected_task and new_status:
            conn = sqlite3.connect('todo.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE tasks SET status=? WHERE username=? AND list_name=? AND task=?",
                           (new_status, self.username, list_name, selected_task))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Task status updated successfully")
            self.load_tasks(list_name)
        else:
            messagebox.showwarning("Input Error", "Please select a task and enter a new status")

    def delete_task(self):
        selected_task_index = self.task_listbox.curselection()
        if not selected_task_index:
            messagebox.showwarning("Input Error", "Please select a task to delete")
            return

        selected_task = self.task_listbox.get(selected_task_index).split(" (")[0]
        list_name = self.listbox.get(self.listbox.curselection())

        if selected_task:
            conn = sqlite3.connect('todo.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tasks WHERE username=? AND list_name=? AND task=?",
                           (self.username, list_name, selected_task))
            conn.commit()
            conn.close()
            self.load_tasks(list_name)
            messagebox.showinfo("Success", "Task deleted successfully")
        else:
            messagebox.showwarning("Input Error", "Please select a task to delete")

    def add_task(self):
        list_name = self.listbox.get(self.listbox.curselection())
        new_task = self.new_task_entry.get().strip()

        if list_name and new_task:
            conn = sqlite3.connect('todo.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tasks (username, list_name, task, status) VALUES (?, ?, ?, 'ongoing')",
                           (self.username, list_name, new_task))
            conn.commit()
            conn.close()
            self.task_listbox.insert(END, f"{new_task} (ongoing)")
            self.new_task_entry.delete(0, END)
            messagebox.showinfo("Success", "Task added successfully")
        else:
            messagebox.showwarning("Input Error", "Please select a list and enter a new task")

    def delete_list(self):
        list_name = self.listbox.get(self.listbox.curselection())

        if list_name:
            conn = sqlite3.connect('todo.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tasks WHERE username=? AND list_name=?", (self.username, list_name))
            conn.commit()
            conn.close()
            self.load_lists()
            self.task_listbox.delete(0, END)
            messagebox.showinfo("Success", "List deleted successfully")
        else:
            messagebox.showwarning("Input Error", "Please select a list to delete")

    def back(self):
        self.destroy()
        from Dashboard import DashboardApp
        DashboardApp().mainloop()


if __name__ == "__main__":
    username = "current_user"  # This should be dynamically set based on the logged-in user
    app = ModifyApp(username)
    app.mainloop()
