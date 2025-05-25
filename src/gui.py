import tkinter as tk
from tkinter import filedialog, ttk, messagebox

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("File Organizer")
        self.root.geometry("600x400") # Initial size

        # --- Main Frame ---
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Folder Selection ---
        folder_frame = ttk.Frame(main_frame, padding="5")
        folder_frame.pack(fill=tk.X, pady=5)

        self.select_folder_button = ttk.Button(
            folder_frame,
            text="Select Folder to Organize",
            command=self.select_folder
        )
        self.select_folder_button.pack(side=tk.LEFT, padx=(0, 10))

        self.selected_folder_var = tk.StringVar()
        self.selected_folder_var.set("No folder selected")
        self.selected_folder_label = ttk.Label(
            folder_frame,
            textvariable=self.selected_folder_var,
            wraplength=400 # Adjust as needed
        )
        self.selected_folder_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Placeholder for future elements
        self.setup_other_ui_elements(main_frame)

    def select_folder(self):
        """Opens a dialog to select a folder and updates the label."""
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.selected_folder_var.set(folder_selected)
            print(f"Selected folder: {folder_selected}") # Console log
        else:
            self.selected_folder_var.set("No folder selected")
            print("Folder selection cancelled.") # Console log

    def setup_other_ui_elements(self, parent_frame):
        """Placeholder for adding more UI elements in later tasks."""
        # This method will be expanded in Phase 2
        pass

if __name__ == '__main__':
    # This is for testing gui.py directly, main.py is the primary entry point
    root = tk.Tk()
    app = App(root)
    root.mainloop() 