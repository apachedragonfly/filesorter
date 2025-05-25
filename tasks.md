🧩 Granular Tasks
🚀 Phase 1: Setup
✅ Task 1: Scaffold project structure

Create file_sorter_gui/ and subdirectories.

Include: README.md, .gitignore, and requirements.txt.

✅ Task 2: Set up virtual environment

Initialize Python venv.

Install PyQt5 and pytest.

Test: pip install -r requirements.txt

⚙️ Phase 2: Sorting Logic (Headless)
✅ Task 3: Build file_rules.py

Create a DEFAULT_RULES dictionary:

python
Copy
Edit
DEFAULT_RULES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".odt"],
    "Audio": [".mp3", ".wav", ".flac", ".aac"],
    "Video": [".mp4", ".mov", ".avi", ".mkv"],
    "Archives": [".zip", ".rar", ".7z"],
    "Adobe Files": [".psd", ".ai", ".indd"],
    "Executables": [".exe", ".msi", ".bat"],
    "Code": [".py", ".js", ".html", ".css", ".cpp", ".java"]
}
✅ Task 4: Implement sort_files_by_extension(src_dir) in sorter_engine.py

Walk the directory.

For each loose file, determine its extension.

Move file to a subfolder based on the rules.

Create the subfolder if it doesn’t exist.

Do not enter subfolders—only sort files directly inside src_dir.

✅ Task 5: Add move_file_safely(src_path, dest_path) to utils.py

Handles:

Creating folders if needed.

Avoiding overwrites (e.g., file (1).jpg)

Test with multiple files having same name.

✅ Task 6: Link file rules to sorter engine

Import DEFAULT_RULES in sorter_engine.py.

Use it in sorting logic to determine destination.

✅ Task 7: Add logging to sorter_engine.py

Create logs/sorter.log.

Log every move: "Moved example.jpg → Images/"

✅ Task 8: Add unit test: test_sorter_engine.py

Mock a temp folder.

Place mixed loose files in it.

Assert files are correctly moved into matching folders.

🧠 Phase 3: GUI Interface
✅ Task 9: Build static UI layout in layout.py

Add:

Folder picker (directory browser)

“Sort Files” button

Output log area

✅ Task 10: Hook up folder picker to variable

Store selected folder path in app state.

✅ Task 11: Trigger sort_files_by_extension() from UI

When button clicked:

Call sort_files_by_extension() with selected path

Update log box with results

✅ Task 12: Add error handling in events.py

Show message if:

Folder is invalid

No files found

Exceptions raised during move

🎨 Phase 4: Polish (Optional for MVP)
✅ Task 13: Apply minimal style via styles.qss

Clean spacing, readable fonts, padding

✅ Task 14: Package executable using pyinstaller

Generate .exe or .app for easy use