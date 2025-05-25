Architecture: GUI File Organizer in Python

Overview

This application is a GUI-based file organizer written in Python using Tkinter. The user selects a folder, optionally edits file extension-to-folder mappings, and clicks a button to organize files accordingly. The UI is clean and intuitive, designed for non-technical users.

Modules

1. gui.py

Contains the Tkinter-based GUI.

Handles user interaction.

Collects user input (target folder, mappings, options).

2. organizer.py

Core logic to sort files based on the user-defined mappings.

Includes conflict resolution, folder creation, summary generation.

3. config.py

Default mappings.

Load/save configuration logic.

4. undo.py

Logs move actions to allow undoing.

Applies reverse of log to move files back.

Core Functional Components

GUI Elements

Folder picker (uses tkinter.filedialog.askdirectory())

Editable mapping area (text field or table with file extension → folder)

Buttons: Run, Dry Run checkbox, Recursive toggle

Status Log output (scrollable text box)

File Sorting Logic

Loads mapping from GUI or config

Walks the target folder (optionally recursively)

Applies move logic

Skips system/hidden files

Avoids overwriting (adds suffix if needed)

Creates folders if missing

Logs all actions

Undo Mechanism

Each run writes to undo_log.txt with original → new path pairs

Undo reads log and reverses each move

Configuration Persistence

Saves current mapping to .json or .yaml

Loads mapping from saved config on launch or by user request

Dependencies

Python 3.x

Tkinter (standard library)

os, shutil, json, yaml, re, tkinter.filedialog

Optional Enhancements (Modular)

Add command-line interface fallback

Add dark mode toggle

Add logging to file for audits

