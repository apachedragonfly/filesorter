import os
import pathlib

# Placeholder for DEFAULT_RULES - will be imported in Task 6
# from .file_rules import DEFAULT_RULES

# Placeholder for move_file_safely - will be imported from utils.py in Task 5
# from .utils import move_file_safely

def sort_files_by_extension(src_dir):
    """Sorts files in src_dir into subdirectories based on their extension.

    Args:
        src_dir (str): The source directory containing files to sort.
    """
    if not os.path.isdir(src_dir):
        print(f"Error: Source directory '{src_dir}' not found.")
        return

    print(f"Starting to sort files in: {src_dir}")

    for item_name in os.listdir(src_dir):
        item_path = os.path.join(src_dir, item_name)

        if os.path.isfile(item_path):
            file_extension = pathlib.Path(item_name).suffix.lower()
            if not file_extension: # Skip files with no extension
                print(f"Skipping '{item_name}': no file extension.")
                continue

            # Placeholder: Determine destination category and path based on rules
            # This will be updated in Task 6 to use DEFAULT_RULES
            destination_category = "Uncategorized" # Default if no rule matches
            # Example: if file_extension in some_category_rules:
            #              destination_category = category_name

            destination_folder_path = os.path.join(src_dir, destination_category)
            destination_file_path = os.path.join(destination_folder_path, item_name)

            print(f"Identified file: '{item_name}', extension: '{file_extension}'")
            print(f"  -> Would move to: '{destination_file_path}' (Category: {destination_category})")

            # Placeholder: Actual file moving logic
            # This will be replaced by a call to move_file_safely in Task 5 & 6
            # if not os.path.exists(destination_folder_path):
            #     os.makedirs(destination_folder_path)
            #     print(f"Created directory: {destination_folder_path}")
            # shutil.move(item_path, destination_file_path) # Example, will use move_file_safely
            # print(f"Moved '{item_name}' to '{destination_category}/'")
        elif os.path.isdir(item_path):
            print(f"Skipping directory: '{item_name}'")
        else:
            print(f"Skipping unknown item: '{item_name}'")

    print(f"Finished sorting files in: {src_dir}")

if __name__ == '__main__':
    # Basic test (manual for now)
    test_dir = "test_sorting_dir"
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)
        # Create some dummy files for testing
        with open(os.path.join(test_dir, "image.jpg"), "w") as f: f.write("")
        with open(os.path.join(test_dir, "document.pdf"), "w") as f: f.write("")
        with open(os.path.join(test_dir, "script.py"), "w") as f: f.write("")
        with open(os.path.join(test_dir, "no_ext_file"), "w") as f: f.write("")
        os.makedirs(os.path.join(test_dir, "subfolder"))
        with open(os.path.join(test_dir, "subfolder", "another.txt"), "w") as f: f.write("")


    print(f"--- Running test for sort_files_by_extension in '{test_dir}' ---")
    sort_files_by_extension(test_dir)
    print(f"--- Test finished. Check '{test_dir}' for results. ---")
    # Manual cleanup: You might want to remove test_dir after checking
    # import shutil
    # shutil.rmtree(test_dir) # Careful with this! 