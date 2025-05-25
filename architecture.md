file_sorter_gui/
├── main.py                          # App entry point
├── requirements.txt                # Dependencies
├── README.md                       # Project documentation
├── sorter/
│   ├── __init__.py
│   ├── controller.py               # Links GUI and sorting logic
│   ├── sorter_engine.py           # Core logic: scan, classify, sort
│   ├── file_rules.py              # File extension → folder mapping
│   └── utils.py                   # Helpers: move file, logging, etc.
├── gui/
│   ├── __init__.py
│   ├── app.py                     # Bootstraps GUI app
│   ├── layout.py                  # GUI layout (folder picker, sort button)
│   └── events.py                  # Handles UI interaction logic
├── assets/
│   ├── icon.png                   # App icon
│   └── styles.qss                 # (Optional) UI styling
├── tests/
│   ├── test_sorter_engine.py
│   ├── test_file_rules.py
│   └── test_utils.py
└── logs/
    └── sorter.log                 # Runtime logs (moved files, errors)

📄 File & Folder Roles
main.py
Purpose: App entry point.

Responsibilities:

Initializes GUI

Sets up logging

Loads config/defaults

requirements.txt
Lists all Python dependencies (e.g., PyQt5, watchdog, pytest, etc.)

README.md
Documentation for setup, usage, and architecture overview.

📦 sorter/ — Core Sorting Logic
controller.py
Role: Orchestrates GUI ↔ logic interaction.

Handles:

Input from GUI (e.g., folder selection)

Triggering sort operations

Managing app state

sorter_engine.py
Role: Core sorting engine.

Handles:

Reading file metadata

Moving files to target folders

Undo functionality (move history, rollback)

Safe overwrite handling

file_rules.py
Role: Rule definitions for file sorting.

Examples:

Group .jpg, .png, .gif into Images/

Group .pdf, .docx into Documents/

Custom user-defined rules

utils.py
Role: Helper functions.

Includes:

File extension extractor

Size/date filters

Logging helpers

🖼️ gui/ — GUI Components
app.py
Role: GUI App starter (e.g., using PyQt5 or Tkinter)

Initializes:

Main window

Layout

Event loop

layout.py
Role: Contains visual layout of the app.

Elements:

Folder chooser

Sorting settings panel

File preview

Logs/output area

events.py
Role: Event management.

Handles:

Button clicks

Rule selection changes

Error modals

File sorting triggers

🎨 assets/ — UI Assets
icon.png: App icon

styles.qss: Theme/stylesheet for PyQt UI (or CSS-equivalent)

🧪 tests/ — Unit & Integration Tests
test_sorter_engine.py: Tests for file moving and rollback logic

test_file_rules.py: Tests rule logic + extension handling

test_utils.py: Tests date/size/format helpers

🗃️ logs/ — Output & Debugging
sorter.log: Runtime logs (errors, file moves, etc.)

✅ Optional Features (Scalable Additions)
✅ Undo/Redo stack using JSON move history

✅ Drag-and-drop folder selection

✅ Save/Load user-defined rule sets

✅ Background folder monitoring (with watchdog)

✅ Profile performance (file count, speed)

💡 Technologies to Use
Language: Python 3.11+

GUI Library: PyQt5 or Tkinter

File Ops: os, shutil, pathlib

Watcher (optional): watchdog

Testing: pytest

🛠️ Sample Rule Format (YAML or JSON)
json
Copy
Edit
{
  "Images": [".jpg", ".jpeg", ".png", ".gif", ".svg"],
  "Documents": [".pdf", ".docx", ".txt", ".odt"],
  "Audio": [".mp3", ".wav", ".flac"],
  "Video": [".mp4", ".mov", ".avi"],
  "Adobe Files": [".psd", ".ai", ".indd"]
}
