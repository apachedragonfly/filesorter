import sys
import os
import logging
from pathlib import Path
from PyQt5.QtWidgets import QApplication

# Ensure the current directory is in sys.path for PyInstaller compatibility if needed
# and for finding modules if main.py is in the root of file_sorter_gui.
if getattr(sys, 'frozen', False):
    # If the application is run as a bundle, the PyInstaller bootloader
    # extends the sys.path for imports from the temporary directory.
    # PROJECT_ROOT should point to where PyInstaller has unpacked files.
    PROJECT_ROOT = Path(sys._MEIPASS) # Base path for PyInstaller bundle
else:
    # If run as a normal script, calculate from __file__
    PROJECT_ROOT = Path(__file__).resolve().parent

# Add project root to sys.path to allow imports like from gui.layout
# This might be redundant if PyInstaller handles it or if main.py is in the root of the package already.
# However, being explicit can help avoid import issues.
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from gui.layout import MainAppLayout # Main window/layout class
# Future: from sorter.controller import AppController # If we refactor later

def main():
    """Main function to initialize and run the PyQt5 application."""
    # Setup basic logging for the main application part, if not handled elsewhere
    # The sorter_engine will have its own logger setup.
    # For the GUI part itself, we might want a general app logger.
    logging.basicConfig(level=logging.INFO, 
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    
    app_logger = logging.getLogger("FileSorterApp")
    app_logger.info("Application starting...")

    app = QApplication(sys.argv)

    # Load and apply stylesheet
    # When packaged with PyInstaller, assets might be in a different relative location.
    # We use PROJECT_ROOT which is adjusted for frozen (PyInstaller) state.
    style_sheet_path = PROJECT_ROOT / "assets" / "styles.qss"
    
    app_logger.info(f"Attempting to load stylesheet from: {style_sheet_path}")
    if style_sheet_path.exists():
        try:
            with open(style_sheet_path, "r") as f_style:
                app.setStyleSheet(f_style.read())
            app_logger.info("Stylesheet applied successfully.")
        except Exception as e:
            app_logger.error(f"Error loading stylesheet {style_sheet_path}: {e}")
    else:
        app_logger.warning(f"Stylesheet not found at {style_sheet_path}. Using default styles.")

    # Create and show the main window/layout
    main_window = MainAppLayout() 
    # In a more complex app, this might be: 
    # controller = AppController(main_window)
    # main_window.set_controller(controller) # If layout needs to call controller methods
    
    main_window.show()
    app_logger.info("Main window shown. Entering event loop.")
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main() 