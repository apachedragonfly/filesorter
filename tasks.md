Task List: GUI File Organizer in Python

Phase 1: Setup and Skeleton

Initialize project structure

Create folders: /src, /tests, /assets

Create files: gui.py, organizer.py, config.py, undo.py, main.py

Setup basic GUI window

Use Tkinter to create a root window

Set a clean and minimal layout

Add folder picker

Add button to open folder selection dialog

Display selected folder path

Phase 2: Core GUI

Add file extension mapping input area

Use multiline Text widget or editable Table

Preload with default mappings

Add control buttons

"Run" button to trigger sorting

"Dry Run" checkbox

"Recursive Mode" toggle

Add status log panel

Scrollable Text box to display move actions and summaries

Phase 3: Sorting Logic (organizer.py)

Implement file scanning logic

List all files in the selected directory

If recursive, walk through all subfolders

Implement extension mapping and sorting logic

Match file extension to folder

Create folder if not exists

Move file to folder

Handle name conflicts

If file exists, add (1), (2), etc., until a free name is found

Update status log

Append result of each move to the log

Display final summary (e.g., "Moved 10 Images")

Phase 4: Undo System (undo.py)

Log all file moves

Write original and new path to undo_log.txt

Implement undo function

Read undo_log.txt

Reverse each move (if file exists)

Phase 5: Config System (config.py)

Add save config feature

Write mapping to .json or .yaml file

Add load config feature

Allow loading from a previously saved config file

Preload default mappings

On first run, populate input area with default mapping dictionary

Phase 6: Finalization

Polish GUI layout

Align elements, ensure resize behavior is clean

Test all features

Manual test each feature

Validate undo, recursive, dry run

Add optional enhancements (if time)

Logging to file

Dark mode

Command-line mode fallback