import tkinter as tk
from gui import App

def main():
    """Main function to run the application."""
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main() 