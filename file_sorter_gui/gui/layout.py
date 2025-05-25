import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLineEdit, QTextEdit, QLabel, QSizePolicy,
    QFileDialog # Added for folder dialog
)
from PyQt5.QtCore import Qt

class MainAppLayout(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("File Sorter GUI")
        # Set a default size that's reasonable
        self.setMinimumSize(600, 400) 
        self.selected_folder_path = None # Variable to store the selected path
        self._init_ui()

    def _init_ui(self):
        # Main vertical layout
        main_layout = QVBoxLayout(self)

        # --- Folder Selection --- #
        folder_section_layout = QHBoxLayout()
        
        self.folder_path_label = QLabel("Selected Folder:")
        self.folder_path_display = QLineEdit()
        self.folder_path_display.setPlaceholderText("No folder selected...")
        self.folder_path_display.setReadOnly(True) # Display only, path set via picker
        
        self.browse_folder_button = QPushButton("Browse...")
        self.browse_folder_button.clicked.connect(self._browse_folder) # Connect button click

        folder_section_layout.addWidget(self.folder_path_label)
        folder_section_layout.addWidget(self.folder_path_display, 1) # Line edit takes available horizontal space
        folder_section_layout.addWidget(self.browse_folder_button)
        main_layout.addLayout(folder_section_layout)

        # --- Sort Button --- #
        self.sort_files_button = QPushButton("Sort Files in Selected Folder")
        self.sort_files_button.setStyleSheet("padding: 10px; font-size: 16px;") # Basic styling
        main_layout.addWidget(self.sort_files_button, alignment=Qt.AlignCenter)

        # --- Output Log Area --- #
        log_area_label = QLabel("Log Output:")
        self.log_output_area = QTextEdit()
        self.log_output_area.setReadOnly(True)
        self.log_output_area.setPlaceholderText("Events will be logged here...")
        # Allow log area to expand vertically
        self.log_output_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        main_layout.addWidget(log_area_label)
        main_layout.addWidget(self.log_output_area)

        self.setLayout(main_layout)

    def _browse_folder(self):
        """Opens a dialog to select a folder and updates the display and internal variable."""
        # The first argument is parent, second is caption, third is default dir.
        # os.getcwd() could be used for default dir if desired.
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder to Sort", "")
        
        if folder_path: # If a folder was selected (not cancelled)
            self.selected_folder_path = folder_path
            self.folder_path_display.setText(self.selected_folder_path)
            print(f"Selected folder: {self.selected_folder_path}") # For console feedback during testing
        else:
            # Optionally, handle case where dialog is cancelled (e.g., clear path or do nothing)
            # self.selected_folder_path = None
            # self.folder_path_display.setPlaceholderText("Folder selection cancelled...")
            print("Folder selection cancelled or no folder chosen.")

# To allow testing this layout independently
if __name__ == '__main__':
    app = QApplication(sys.argv)
    # In a real app, we'd instantiate from gui.app or main.py
    # For now, just show the layout
    layout_widget = MainAppLayout()
    layout_widget.show()
    sys.exit(app.exec_()) 