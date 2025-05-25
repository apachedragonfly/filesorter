import sys
import logging # For custom handler and logger access
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLineEdit, QTextEdit, QLabel, QSizePolicy,
    QFileDialog, QMessageBox # Added QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal, QObject # Added pyqtSignal, QObject

# Adjust path to import from sorter module
import os
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
from sorter.sorter_engine import sort_files_by_extension, logger as sorter_logger # Import the specific logger

# Custom Log Handler for QTextEdit
class QTextEditLogHandler(logging.Handler, QObject):
    messageWritten = pyqtSignal(str)

    def __init__(self, parent):
        super().__init__()
        QObject.__init__(self)
        self.formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        self.setFormatter(self.formatter)

    def emit(self, record):
        msg = self.format(record)
        self.messageWritten.emit(msg)

class MainAppLayout(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("File Sorter GUI")
        self.setMinimumSize(600, 450) # Slightly increased height for log messages
        self.selected_folder_path = None
        self._init_ui()
        self._setup_gui_logging() # Initialize GUI logging

    def _setup_gui_logging(self):
        """Sets up logging to the GUI's QTextEdit."""
        self.log_handler = QTextEditLogHandler(self)
        # Add handler to the specific sorter_logger from sorter_engine
        # This avoids capturing all root logger messages if not desired.
        sorter_logger.addHandler(self.log_handler)
        # Optionally, set the level for this handler if you want GUI to show different verbosity
        # self.log_handler.setLevel(logging.INFO) 
        self.log_handler.messageWritten.connect(self._update_log_area)

    def _update_log_area(self, message):
        """Appends a message to the log_output_area QTextEdit."""
        self.log_output_area.append(message)

    def _init_ui(self):
        main_layout = QVBoxLayout(self)

        folder_section_layout = QHBoxLayout()
        self.folder_path_label = QLabel("Selected Folder:")
        self.folder_path_display = QLineEdit()
        self.folder_path_display.setPlaceholderText("No folder selected...")
        self.folder_path_display.setReadOnly(True)
        self.browse_folder_button = QPushButton("Browse...")
        self.browse_folder_button.clicked.connect(self._browse_folder)
        folder_section_layout.addWidget(self.folder_path_label)
        folder_section_layout.addWidget(self.folder_path_display, 1)
        folder_section_layout.addWidget(self.browse_folder_button)
        main_layout.addLayout(folder_section_layout)

        self.sort_files_button = QPushButton("Sort Files in Selected Folder")
        self.sort_files_button.setStyleSheet("padding: 10px; font-size: 16px;")
        self.sort_files_button.clicked.connect(self._trigger_sort) # Connect sort button
        main_layout.addWidget(self.sort_files_button, alignment=Qt.AlignCenter)

        log_area_label = QLabel("Log Output:")
        self.log_output_area = QTextEdit()
        self.log_output_area.setReadOnly(True)
        self.log_output_area.setPlaceholderText("Events will be logged here...")
        self.log_output_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        main_layout.addWidget(log_area_label)
        main_layout.addWidget(self.log_output_area)

        self.setLayout(main_layout)

    def _browse_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder to Sort", self.selected_folder_path or os.getcwd())
        if folder_path:
            self.selected_folder_path = folder_path
            self.folder_path_display.setText(self.selected_folder_path)
            # Log to GUI instead of print
            self.log_output_area.append(f"INFO: Selected folder: {self.selected_folder_path}") 
        else:
            self.log_output_area.append("INFO: Folder selection cancelled or no folder chosen.")

    def _trigger_sort(self):
        """Handles the click of the 'Sort Files' button."""
        self.log_output_area.clear() # Clear log area for new sort operation
        
        if self.selected_folder_path and os.path.isdir(self.selected_folder_path):
            self.log_output_area.append(f"Starting sort for: {self.selected_folder_path}")
            try:
                # This will now log to both file (if sorter_engine still has its file handler)
                # and to our GUI log area via the QTextEditLogHandler.
                moved_count, skipped_count = sort_files_by_extension(self.selected_folder_path)
                
                # The summary is already logged by sorter_engine, so we mainly focus on overall status here.
                if moved_count == 0 and skipped_count > 0:
                    self.log_output_area.append(f"INFO: Sorting process completed. No files were moved, but {skipped_count} items were processed/skipped.")
                    QMessageBox.information(self, "Sort Complete", f"Sorting process finished for \n{self.selected_folder_path}.\nNo files were moved. Check logs for details.")
                elif moved_count == 0 and skipped_count == 0:
                    self.log_output_area.append(f"INFO: Sorting process completed. No files found to move or skip in {self.selected_folder_path}.")
                    QMessageBox.information(self, "Sort Complete", f"No files found to sort in \n{self.selected_folder_path}.")
                else: # moved_count > 0
                    self.log_output_area.append(f"SUCCESS: Sorting process completed. {moved_count} file(s) moved.")
                    QMessageBox.information(self, "Sort Complete", f"Successfully sorted {moved_count} file(s) in \n{self.selected_folder_path}")
            except Exception as e:
                error_msg = f"ERROR: An unexpected error occurred during sorting: {e}"
                self.log_output_area.append(error_msg)
                QMessageBox.critical(self, "Sort Error", f"An error occurred: \n{e}")
        else:
            msg = "No folder selected or folder is invalid. Please select a valid folder first."
            self.log_output_area.append(f"WARNING: {msg}")
            QMessageBox.warning(self, "No Folder Selected", msg)

# To allow testing this layout independently
if __name__ == '__main__':
    # Setup a basic console logger for __main__ execution for debugging this file itself.
    # The sorter_engine's logger will still use its own handlers (file + GUI if MainAppLayout is up).
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    app = QApplication(sys.argv)
    layout_widget = MainAppLayout()
    layout_widget.show()
    sys.exit(app.exec_()) 