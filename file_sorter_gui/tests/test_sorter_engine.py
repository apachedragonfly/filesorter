import os
import shutil
import pytest
from pathlib import Path

# Adjust the Python path to include the project root (file_sorter_gui)
# This allows pytest to find the sorter module correctly when run from the tests/ directory or project root.
import sys
PROJECT_ROOT = Path(__file__).resolve().parent.parent # Moves up two levels from tests/test_sorter_engine.py to file_sorter_gui/
sys.path.insert(0, str(PROJECT_ROOT))

from sorter.sorter_engine import sort_files_by_extension
from sorter.file_rules import DEFAULT_RULES # To help verify categories

@pytest.fixture
def temp_sorting_dir(tmp_path):
    """Create a temporary directory structure for sorting tests."""
    src_dir = tmp_path / "test_src"
    src_dir.mkdir()

    # Create dummy files with various extensions
    (src_dir / "image1.jpg").write_text("dummy jpg content")
    (src_dir / "document1.pdf").write_text("dummy pdf content")
    (src_dir / "archive1.zip").write_text("dummy zip content")
    (src_dir / "script1.py").write_text("dummy py content")
    (src_dir / "unknown.xyz").write_text("dummy unknown content")
    (src_dir / "file_no_ext").write_text("dummy no_ext content")

    # Create a subdirectory with a file (should be ignored)
    sub_dir = src_dir / "subfolder"
    sub_dir.mkdir()
    (sub_dir / "ignored_file.txt").write_text("this file should not be moved")
    
    return src_dir

def test_sort_files_basic(temp_sorting_dir, caplog):
    """Test basic file sorting into correct category folders."""
    src_dir = temp_sorting_dir
    
    # Capture logs for verification (optional, but good for checking behavior)
    import logging
    caplog.set_level(logging.INFO)

    sort_files_by_extension(str(src_dir))

    # Assertions
    # Check if files were moved to correct category folders based on DEFAULT_RULES
    assert (src_dir / "Images" / "image1.jpg").exists()
    assert not (src_dir / "image1.jpg").exists() # Original should be gone

    assert (src_dir / "Documents" / "document1.pdf").exists()
    assert not (src_dir / "document1.pdf").exists()

    assert (src_dir / "Archives" / "archive1.zip").exists()
    assert not (src_dir / "archive1.zip").exists()

    assert (src_dir / "Code" / "script1.py").exists()
    assert not (src_dir / "script1.py").exists()

    # Check for uncategorized files
    assert (src_dir / "Uncategorized" / "unknown.xyz").exists()
    assert not (src_dir / "unknown.xyz").exists()
    assert (src_dir / "file_no_ext").exists()
    assert not (src_dir / "Uncategorized" / "file_no_ext").exists()

    # Check that the subdirectory and its contents are untouched
    assert (src_dir / "subfolder").is_dir()
    assert (src_dir / "subfolder" / "ignored_file.txt").exists()

    # Verify log messages (example)
    assert f"Moved 'image1.jpg' -> 'Images/'" in caplog.text
    assert f"Moved 'document1.pdf' -> 'Documents/'" in caplog.text
    assert f"Skipping directory: 'subfolder'" in caplog.text
    assert f"Skipping 'file_no_ext': no file extension." in caplog.text # Check if this is logged as info or debug in engine
    assert f"Moved 'unknown.xyz' -> 'Uncategorized/'" in caplog.text

def test_sort_empty_directory(tmp_path, caplog):
    """Test sorting an empty directory."""
    empty_dir = tmp_path / "empty_test_src"
    empty_dir.mkdir()
    import logging
    caplog.set_level(logging.INFO)

    sort_files_by_extension(str(empty_dir))

    assert f"Starting to sort files in: {str(empty_dir)}" in caplog.text
    assert f"Finished sorting files in: {str(empty_dir)}" in caplog.text
    assert f"Summary: 0 file(s) moved, 0 item(s) skipped." in caplog.text
    # Check that no category folders were created
    items_in_dir = list(empty_dir.iterdir())
    assert len(items_in_dir) == 0

def test_sort_non_existent_directory(tmp_path, caplog):
    """Test sorting a non-existent directory."""
    non_existent_dir = tmp_path / "non_existent_dir"
    # Do not create this directory
    import logging
    caplog.set_level(logging.ERROR)

    sort_files_by_extension(str(non_existent_dir))

    assert f"Source directory '{str(non_existent_dir)}' not found or is not a directory." in caplog.text

# To run tests from the file_sorter_gui directory:
# Ensure pytest is installed in your venv.
# Activate venv: .\venv\Scripts\Activate.ps1
# Run: pytest
# Or specifically: pytest tests/test_sorter_engine.py 