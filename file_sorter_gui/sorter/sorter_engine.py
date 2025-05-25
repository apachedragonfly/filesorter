import os
import pathlib

# Import DEFAULT_RULES and move_file_safely
from .file_rules import DEFAULT_RULES
from .utils import move_file_safely

def sort_files_by_extension(src_dir):
    """Sorts files in src_dir into subdirectories based on their extension.

    Args:
        src_dir (str): The source directory containing files to sort.
    """
    if not os.path.isdir(src_dir):
        # Consider logging this error instead of just printing in a real app
        print(f"Error: Source directory '{src_dir}' not found or is not a directory.")
        return

    print(f"Starting to sort files in: {src_dir}")
    files_moved_count = 0
    files_skipped_count = 0

    for item_name in os.listdir(src_dir):
        item_path = os.path.join(src_dir, item_name)

        if os.path.isfile(item_path):
            file_extension = pathlib.Path(item_name).suffix.lower()
            if not file_extension: # Skip files with no extension
                print(f"Skipping '{item_name}': no file extension.")
                files_skipped_count += 1
                continue

            destination_category = "Uncategorized" # Default if no rule matches
            for category, extensions in DEFAULT_RULES.items():
                if file_extension in extensions:
                    destination_category = category
                    break

            destination_folder_path = os.path.join(src_dir, destination_category)
            # The move_file_safely function expects the full destination file path
            destination_file_path = os.path.join(destination_folder_path, item_name)

            print(f"Identified file: '{item_name}', extension: '{file_extension}', category: '{destination_category}'")
            
            # Use move_file_safely to move the file
            final_path = move_file_safely(item_path, destination_file_path)
            if final_path:
                files_moved_count += 1
                # print(f"Successfully moved '{item_name}' to '{final_path}'") # move_file_safely already prints
            else:
                files_skipped_count += 1
                print(f"Failed to move '{item_name}'. Check logs from move_file_safely.")

        elif os.path.isdir(item_path):
            # As per Task 4: Do not enter subfolders—only sort files directly inside src_dir.
            print(f"Skipping directory: '{item_name}'")
            files_skipped_count += 1 # Or handle as per specific requirements for subdirs
        else:
            print(f"Skipping unknown item: '{item_name}'")
            files_skipped_count += 1

    print(f"Finished sorting files in: {src_dir}")
    print(f"Summary: {files_moved_count} file(s) moved, {files_skipped_count} item(s) skipped.")

if __name__ == '__main__':
    import shutil # Added for cleanup in test
    # Basic test (manual for now)
    base_test_dir = "test_sorting_engine_integration"
    # Clean up previous test run directory if it exists
    if os.path.exists(base_test_dir):
        shutil.rmtree(base_test_dir)
    os.makedirs(base_test_dir) # Create a fresh base test directory

    # Create some dummy files directly in base_test_dir for testing
    dummy_files_info = {
        "image.jpg": "", "image.jpeg": "", "photo.png": "", "animation.gif": "",
        "document.pdf": "", "report.docx": "", "notes.txt": "",
        "song.mp3": "", "podcast.wav": "",
        "movie.mp4": "", "clip.avi": "",
        "archive.zip": "", "backup.rar": "",
        "design.psd": "", "vector.ai": "",
        "installer.exe": "", "script.bat": "",
        "code.py": "", "webpage.html": "", "stylesheet.css": "",
        "unknown_ext.xyz": "", "file_without_extension": ""
    }
    for f_name, content in dummy_files_info.items():
        with open(os.path.join(base_test_dir, f_name), "w") as f:
            f.write(content)
    
    # Create a dummy subfolder with a file in it (should be ignored by sorter)
    os.makedirs(os.path.join(base_test_dir, "ExistingSubfolder"))
    with open(os.path.join(base_test_dir, "ExistingSubfolder", "dont_touch_me.txt"), "w") as f:
        f.write("This file should not be moved.")

    print(f"--- Running test for sort_files_by_extension in '{base_test_dir}' ---")
    print(f"Directory contents before sorting:")
    for item in os.listdir(base_test_dir):
        print(f"- {item}")
    print("-----------------------------------------------------")

    sort_files_by_extension(base_test_dir)

    print("-----------------------------------------------------")
    print(f"--- Test finished. Check contents of '{base_test_dir}' for results. ---")
    print(f"Directory contents after sorting:")
    for item in os.listdir(base_test_dir):
        item_full_path = os.path.join(base_test_dir, item)
        if os.path.isdir(item_full_path):
            print(f"- {item}/ (Contains: {os.listdir(item_full_path)})")
        else:
            print(f"- {item}")
    print("-----------------------------------------------------")

    # Suggesting manual check, but cleanup can be uncommented for repeated tests
    # print(f"Consider manually deleting '{base_test_dir}' after review.")
    # shutil.rmtree(base_test_dir) # Careful with this! 