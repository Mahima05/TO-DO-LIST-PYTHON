import customtkinter as ctk

class DashboardApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Dashboard")
        self.geometry("400x300")

        # Create New List button
        self.create_list_button = ctk.CTkButton(self, text="Create New List", command=self.open_create)
        self.create_list_button.pack(pady=(20, 10))

        # Modify Existing List button
        self.modify_list_button = ctk.CTkButton(self, text="Modify Existing List", command=self.open_modify)
        self.modify_list_button.pack(pady=10)

        # Track List button
        self.track_list_button = ctk.CTkButton(self, text="Track List", command=self.track_list)
        self.track_list_button.pack(pady=10)

        # Back button
        self.back_button = ctk.CTkButton(self, text="Back", command=self.back)
        self.back_button.pack(pady=(10, 20))

    def open_create(self):
        self.destroy()
        from Create import CreateApp
        CreateApp().mainloop()

    def open_modify(self):
        self.destroy()
        from Modify import ModifyApp
        ModifyApp(username="current_user").mainloop()

    def track_list(self):
        print("Track List clicked")
        # Add functionality to track a list

    def back(self):
        self.destroy()
        from Login import LoginApp
        LoginApp().mainloop()

if __name__ == "__main__":
    app = DashboardApp()
    app.mainloop()
