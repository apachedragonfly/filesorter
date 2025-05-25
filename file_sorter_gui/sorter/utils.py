import os
import shutil
import pathlib

def move_file_safely(src_path, dest_path):
    """Moves a file from src_path to dest_path, handling directory creation
    and avoiding overwrites by appending a number to the filename if needed.

    Args:
        src_path (str): The full path to the source file.
        dest_path (str): The full path to the desired destination, including filename.

    Returns:
        str: The final destination path of the moved file, or None if move failed.
    """
    if not os.path.isfile(src_path):
        print(f"Error: Source file '{src_path}' not found or is not a file.")
        return None

    dest_dir = os.path.dirname(dest_path)
    base_name = pathlib.Path(dest_path).stem
    extension = pathlib.Path(dest_path).suffix
    final_dest_path = dest_path

    # Create destination directory if it doesn't exist
    if not os.path.exists(dest_dir):
        try:
            os.makedirs(dest_dir)
            print(f"Created directory: '{dest_dir}'")
        except OSError as e:
            print(f"Error creating directory '{dest_dir}': {e}")
            return None

    # Handle potential overwrites
    counter = 1
    while os.path.exists(final_dest_path):
        final_dest_path = os.path.join(dest_dir, f"{base_name} ({counter}){extension}")
        counter += 1

    # Move the file
    try:
        shutil.move(src_path, final_dest_path)
        print(f"Moved '{os.path.basename(src_path)}' to '{final_dest_path}'")
        return final_dest_path
    except Exception as e:
        print(f"Error moving file '{src_path}' to '{final_dest_path}': {e}")
        return None

if __name__ == '__main__':
    # Setup a test environment
    test_src_dir = "test_utils_src"
    test_dest_dir = "test_utils_dest"

    # Clean up previous test runs if they exist
    if os.path.exists(test_src_dir):
        shutil.rmtree(test_src_dir)
    if os.path.exists(test_dest_dir):
        shutil.rmtree(test_dest_dir)

    os.makedirs(test_src_dir)
    # os.makedirs(test_dest_dir) # Let the function create this

    # Create some dummy source files
    test_files = ["file1.txt", "file2.jpg", "file_to_conflict.txt"]
    for f_name in test_files:
        with open(os.path.join(test_src_dir, f_name), "w") as f:
            f.write(f"This is {f_name}")

    print("--- Testing move_file_safely --- (New Destination Folder)")
    # Test 1: Move file1.txt to a new folder
    src1 = os.path.join(test_src_dir, "file1.txt")
    dest1_folder = os.path.join(test_dest_dir, "TextFiles")
    dest1 = os.path.join(dest1_folder, "file1.txt")
    result_path1 = move_file_safely(src1, dest1)
    if result_path1 and os.path.exists(result_path1):
        print(f"Test 1 SUCCESS: '{result_path1}' exists.")
    else:
        print(f"Test 1 FAILED for '{src1}' to '{dest1}'.")

    print("\n--- Testing move_file_safely --- (Existing File Conflict)")
    # Test 2: Create a conflicting file at destination first
    conflict_src = os.path.join(test_src_dir, "file_to_conflict.txt") # Source file
    dest_conflict_folder = os.path.join(test_dest_dir, "ConflictFolder")
    dest_conflict_target_name = "file_to_conflict.txt"
    # Manually create the destination folder and the conflicting file
    if not os.path.exists(dest_conflict_folder):
        os.makedirs(dest_conflict_folder)
    with open(os.path.join(dest_conflict_folder, dest_conflict_target_name), "w") as f:
        f.write("This is the ORIGINAL conflicting file.")
        print(f"Manually created '{os.path.join(dest_conflict_folder, dest_conflict_target_name)}' for conflict test.")

    # Now try to move the source file to the same name
    result_path2 = move_file_safely(conflict_src, os.path.join(dest_conflict_folder, dest_conflict_target_name))
    expected_new_name = os.path.join(dest_conflict_folder, "file_to_conflict (1).txt")
    if result_path2 and os.path.exists(result_path2) and result_path2 == expected_new_name:
        print(f"Test 2 SUCCESS: Conflicting file moved to '{result_path2}'.")
    else:
        print(f"Test 2 FAILED. Expected '{expected_new_name}', Got: '{result_path2}'")
        if result_path2 and not os.path.exists(result_path2):
            print(f"  File '{result_path2}' does not exist.")
        elif not result_path2:
             print(f"  Move operation returned None.")


    print("\n--- Testing move_file_safely --- (Multiple Conflicts)")
    # Test 3: Move multiple files that would conflict
    # Re-create the source file as it was moved in Test 2
    with open(os.path.join(test_src_dir, "file_to_conflict.txt"), "w") as f:
        f.write("This is a NEW file_to_conflict.txt for Test 3")

    src3 = os.path.join(test_src_dir, "file_to_conflict.txt")
    dest3_target = os.path.join(dest_conflict_folder, "file_to_conflict.txt") # Same target as before
    result_path3 = move_file_safely(src3, dest3_target)
    expected_new_name3 = os.path.join(dest_conflict_folder, "file_to_conflict (2).txt")

    if result_path3 and os.path.exists(result_path3) and result_path3 == expected_new_name3:
        print(f"Test 3 SUCCESS: Second conflicting file moved to '{result_path3}'.")
    else:
        print(f"Test 3 FAILED. Expected '{expected_new_name3}', Got: '{result_path3}'")

    # Test 4: Moving a non-existent file
    print("\n--- Testing move_file_safely --- (Source File Not Found)")
    src4 = os.path.join(test_src_dir, "non_existent_file.txt")
    dest4 = os.path.join(test_dest_dir, "NonExistent", "non_existent_file.txt")
    result_path4 = move_file_safely(src4, dest4)
    if result_path4 is None:
        print(f"Test 4 SUCCESS: Handled non-existent source file correctly.")
    else:
        print(f"Test 4 FAILED: Did not handle non-existent source file correctly.")


    print("\n--- Test completed. Check output and folders: '")
    print(f"Source files were in: '{os.path.abspath(test_src_dir)}'")
    print(f"Destination files are in: '{os.path.abspath(test_dest_dir)}'")
    # print("Consider manually deleting test_utils_src/ and test_utils_dest/ after review.") 