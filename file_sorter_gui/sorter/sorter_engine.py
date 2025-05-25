import os
import pathlib
import logging
import datetime

# Import DEFAULT_RULES and move_file_safely
from .file_rules import DEFAULT_RULES
from .utils import move_file_safely

# --- Logger Setup ---
def setup_logger():
    """Sets up the main logger for the sorter engine."""
    log_directory = "logs"  # Relative to project root (file_sorter_gui/)
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    log_file_path = os.path.join(log_directory, "sorter.log")

    logger = logging.getLogger("FileSorterEngine")
    logger.setLevel(logging.INFO) # Set default logging level

    # Prevent duplicate handlers if this setup is called multiple times (e.g., in tests)
    if logger.hasHandlers():
        logger.handlers.clear()

    # File Handler
    fh = logging.FileHandler(log_file_path)
    fh.setLevel(logging.INFO) # Or logging.DEBUG for more verbose logs

    # Console Handler (optional, for also seeing logs in console during -m execution)
    # ch = logging.StreamHandler()
    # ch.setLevel(logging.INFO)

    # Formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    fh.setFormatter(formatter)
    # ch.setFormatter(formatter)

    logger.addHandler(fh)
    # logger.addHandler(ch) # Uncomment to also log to console

    return logger

logger = setup_logger()
# --- End Logger Setup ---

def sort_files_by_extension(src_dir):
    """Sorts files in src_dir into subdirectories based on their extension.

    Args:
        src_dir (str): The source directory containing files to sort.
    """
    if not os.path.isdir(src_dir):
        logger.error(f"Source directory '{src_dir}' not found or is not a directory.")
        return 0, 0 # Return counts on error

    logger.info(f"Starting to sort files in: {src_dir}")
    files_moved_count = 0
    files_skipped_count = 0

    for item_name in os.listdir(src_dir):
        item_path = os.path.join(src_dir, item_name)

        if os.path.isfile(item_path):
            file_extension = pathlib.Path(item_name).suffix.lower()
            if not file_extension: # Skip files with no extension
                logger.info(f"Skipping '{item_name}': no file extension.")
                files_skipped_count += 1
                continue

            destination_category = "Uncategorized" # Default if no rule matches
            for category, extensions in DEFAULT_RULES.items():
                if file_extension in extensions:
                    destination_category = category
                    break

            destination_folder_path = os.path.join(src_dir, destination_category)
            destination_file_path = os.path.join(destination_folder_path, item_name)

            logger.debug(f"Identified file: '{item_name}', extension: '{file_extension}', category: '{destination_category}'")
            
            final_path = move_file_safely(item_path, destination_file_path) # move_file_safely prints its own info/errors
            if final_path:
                logger.info(f"Moved '{item_name}' -> '{destination_category}/'")
                files_moved_count += 1
            else:
                # move_file_safely would have printed an error, here we log the failure from sorter's perspective
                logger.warning(f"Failed to move '{item_name}' (destination: '{destination_file_path}'). Check previous logs for details from move_file_safely.")
                files_skipped_count += 1

        elif os.path.isdir(item_path):
            logger.info(f"Skipping directory: '{item_name}'")
            files_skipped_count += 1
        else:
            logger.warning(f"Skipping unknown item: '{item_name}' at path '{item_path}'")
            files_skipped_count += 1

    logger.info(f"Finished sorting files in: {src_dir}")
    logger.info(f"Summary: {files_moved_count} file(s) moved, {files_skipped_count} item(s) skipped.")
    return files_moved_count, files_skipped_count # Return the counts

if __name__ == '__main__':
    import shutil
    # Ensure logger is set to DEBUG for __main__ to see all messages if testing verbosely
    # logger.setLevel(logging.DEBUG) # Optional: for more verbose output during this test
    
    print("--- Main execution started. Logging to logs/sorter.log ---")
    logger.info("--- sorter_engine.py executed directly via __main__ ---")

    base_test_dir = "test_sorting_engine_integration_with_logging"
    if os.path.exists(base_test_dir):
        shutil.rmtree(base_test_dir)
    os.makedirs(base_test_dir)

    dummy_files_info = {
        "image.jpg": "", "image.jpeg": "", "photo.png": "", "animation.gif": "",
        "document.pdf": "", "report.docx": "", "notes.txt": "",
        "song.mp3": "", "podcast.wav": "",
        "movie.mp4": "", "clip.avi": "",
        "archive.zip": "", "backup.rar": "",
        "design.psd": "", "vector.ai": "",
        "installer.exe": "", "script.bat": "",
        "code.py": "", "webpage.html": "", "stylesheet.css": "",
        "unknown_ext.xyz": "", "file_without_extension": "",
        "another_image.jpg": "conflict_test" # To test renaming by move_file_safely
    }
    for f_name, content in dummy_files_info.items():
        with open(os.path.join(base_test_dir, f_name), "w") as f:
            f.write(content)
    
    # Create a duplicate for conflict testing in move_file_safely, which should be logged by utils if it prints
    with open(os.path.join(base_test_dir, "image.jpg"), "w") as f: # Overwrite to ensure its content is different if needed for a deeper test
        f.write("original image.jpg content")


    os.makedirs(os.path.join(base_test_dir, "ExistingSubfolder"))
    with open(os.path.join(base_test_dir, "ExistingSubfolder", "dont_touch_me.txt"), "w") as f:
        f.write("This file should not be moved.")

    print(f"--- Running test for sort_files_by_extension in '{base_test_dir}' ---")
    print(f"Directory contents before sorting (see console):")
    for item in os.listdir(base_test_dir):
        print(f"- {item}")
    print("-----------------------------------------------------")

    moved, skipped = sort_files_by_extension(base_test_dir) # Capture returned counts
    print(f"__main__ result: Moved: {moved}, Skipped: {skipped}") # Print returned counts

    print("-----------------------------------------------------")
    print(f"--- Test finished. Check logs/sorter.log and contents of '{base_test_dir}' ---")
    print(f"Directory contents after sorting (see console):")
    for item in os.listdir(base_test_dir):
        item_full_path = os.path.join(base_test_dir, item)
        if os.path.isdir(item_full_path):
            print(f"- {item}/ (Contains: {os.listdir(item_full_path)})")
        else:
            print(f"- {item}")
    print("-----------------------------------------------------")
    logger.info("--- sorter_engine.py __main__ execution finished ---")
    # print(f"Consider manually deleting '{base_test_dir}' after review.")
    # shutil.rmtree(base_test_dir) 