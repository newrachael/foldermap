"""Tests for the foldermap package."""

import os
import tempfile
import unittest
from foldermap import collect_files, get_folder_structure


class TestFoldermapunittest.TestCase):
    """Test cases for foldermap package."""

    def setUp(self):
        """Set up temporary files for testing."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_dir = self.temp_dir.name
        
        # Create test directory structure
        os.makedirs(os.path.join(self.test_dir, "folder1"))
        os.makedirs(os.path.join(self.test_dir, "folder2"))
        os.makedirs(os.path.join(self.test_dir, "excluded"))
        
        # Create test files
        with open(os.path.join(self.test_dir, "root.txt"), "w") as f:
            f.write("Root file")
        
        with open(os.path.join(self.test_dir, "root.py"), "w") as f:
            f.write("print('Hello')")
        
        with open(os.path.join(self.test_dir, "folder1", "file1.txt"), "w") as f:
            f.write("File 1")
        
        with open(os.path.join(self.test_dir, "folder2", "file2.py"), "w") as f:
            f.write("print('File 2')")
        
        with open(os.path.join(self.test_dir, "excluded", "excluded.txt"), "w") as f:
            f.write("Excluded")

    def tearDown(self):
        """Clean up temporary files."""
        self.temp_dir.cleanup()

    def test_collect_files(self):
        """Test collecting files."""
        # Test collecting all files
        files = collect_files(self.test_dir)
        self.assertEqual(len(files), 5)
        
        # Test with extension filter
        files = collect_files(self.test_dir, extensions=[".txt"])
        self.assertEqual(len(files), 3)
        
        # Test with folder exclusion
        files = collect_files(self.test_dir, exclude_folders=["excluded"])
        self.assertEqual(len(files), 4)
        
        # Test with both filters
        files = collect_files(
            self.test_dir, 
            extensions=[".py"], 
            exclude_folders=["excluded"]
        )
        self.assertEqual(len(files), 2)

    def test_folder_structure(self):
        """Test generating folder structure."""
        files = collect_files(self.test_dir)
        structure = get_folder_structure(self.test_dir, files)
        
        # Check structure length (should contain all files and folders)
        # 5 files + 3 folders
        self.assertTrue(len(structure) >= 5)
        
        # Check that structure contains folder markers
        folder_lines = [line for line in structure if "📁" in line]
        self.assertTrue(len(folder_lines) >= 3)
        
        # Check that structure contains file markers
        file_lines = [line for line in structure if "📄" in line]
        self.assertTrue(len(file_lines) >= 5)


if __name__ == '__main__':
    unittest.main()