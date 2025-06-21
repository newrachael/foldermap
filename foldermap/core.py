"""Core functionality for the foldermap package."""

import os
import datetime
from pathspec import PathSpec


def collect_files(folder_path, extensions=None, exclude_folders=None, include_hidden=False):
    """Collect files from within a folder with improved .gitignore handling.

    Args:
        folder_path (str): Path to search for files
        extensions (list, optional): List of file extensions to include
        exclude_folders (list, optional): List of folder names or paths to exclude
        include_hidden (bool, optional): Whether to include hidden folders (starting with .)
        
    Returns:
        list: List of collected file paths (relative to folder_path)
    """
    # Note: Default exclusions are now handled by CLI
    # This allows for more explicit control
    
    # ─────────────────────────────────────────────────────────────────────────────
    # 1) Load .gitignore patterns
    gitignore_path = os.path.join(folder_path, '.gitignore')
    gitignore_spec = None
    if os.path.isfile(gitignore_path):
        with open(gitignore_path, 'r') as f:
            patterns = []
            for line in f:
                line = line.strip()
                # Skip comments and empty lines
                if line and not line.startswith('#'):
                    patterns.append(line)
        
        if patterns:
            gitignore_spec = PathSpec.from_lines('gitwildmatch', patterns)
    # ─────────────────────────────────────────────────────────────────────────────

    collected_files = []

    for root, dirs, files in os.walk(folder_path, topdown=True):
        # Get relative path from folder_path
        rel_root = os.path.relpath(root, folder_path)
        if rel_root == '.':
            rel_root = ''

        # ─────────────────────────────────────────────────────────────────────────
        # 2) Filter directories BEFORE os.walk descends into them
        # ─────────────────────────────────────────────────────────────────────────
        filtered_dirs = []
        
        for d in dirs:
            # Build the full relative path for this directory
            if rel_root:
                dir_path = os.path.join(rel_root, d)
            else:
                dir_path = d
            
            # Normalize path for gitignore matching
            dir_path_posix = dir_path.replace(os.sep, '/')
            
            # Check if should exclude
            should_exclude = False
            
            # Check user-specified exclusions
            if exclude_folders:
                # Check both directory name and full path
                if d in exclude_folders or dir_path in exclude_folders:
                    should_exclude = True
            
            # Check hidden/dunder folders
            if not include_hidden:
                if d.startswith('.') or (d.startswith('__') and d.endswith('__')):
                    should_exclude = True
            
            # Check .gitignore patterns
            if gitignore_spec and not should_exclude:
                # For directories, check multiple variations
                # PathSpec expects directories to have trailing slashes for proper matching
                paths_to_check = [
                    d,                          # Just the directory name
                    d + '/',                    # Directory name with trailing slash
                    dir_path_posix,            # Full relative path
                    dir_path_posix + '/',      # With trailing slash
                ]
                
                for check_path in paths_to_check:
                    if gitignore_spec.match_file(check_path):
                        should_exclude = True
                        break
            
            if not should_exclude:
                filtered_dirs.append(d)
        
        # Update dirs in-place to control which subdirectories os.walk will visit
        dirs[:] = filtered_dirs

        # ─────────────────────────────────────────────────────────────────────────
        # 3) Process files in current directory
        # ─────────────────────────────────────────────────────────────────────────
        for filename in files:
            # Build relative file path
            if rel_root:
                rel_file = os.path.join(rel_root, filename)
            else:
                rel_file = filename
            
            # Normalize for gitignore matching
            rel_file_posix = rel_file.replace(os.sep, '/')
            
            # Check .gitignore
            if gitignore_spec and gitignore_spec.match_file(rel_file_posix):
                continue
            
            # Check extensions
            if extensions:
                ext = os.path.splitext(filename)[1].lower()
                if ext not in extensions:
                    continue
            
            # Check hidden files
            if not include_hidden and filename.startswith('.'):
                continue
            
            collected_files.append(rel_file)

    return collected_files


def get_folder_structure(folder_path, files):
    """
    Create a tree representation of the folder structure.
    
    Args:
        folder_path (str): Base folder path
        files (list): List of files (relative paths)
        
    Returns:
        list: Formatted strings representing the folder structure
    """
    # Build a tree structure
    tree = {}
    
    # Add all files to tree
    for file_path in sorted(files):
        parts = file_path.split(os.sep)
        current = tree
        
        # Navigate/create folders
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
        
        # Add file (using a special prefix to distinguish from folders)
        filename = parts[-1]
        current[f"_file_{filename}"] = None

    # Convert tree to formatted strings
    def tree_to_strings(tree_dict, prefix=""):
        lines = []
        items = sorted(tree_dict.items())
        
        # Separate files and folders
        files = [(name, val) for name, val in items if name.startswith("_file_")]
        folders = [(name, val) for name, val in items if not name.startswith("_file_")]
        
        # Process files first
        for name, _ in files:
            actual_name = name[6:]  # Remove "_file_" prefix
            lines.append(f"{prefix}📄 {actual_name}")
        
        # Then process folders
        for name, subtree in folders:
            lines.append(f"{prefix}📁 {name}")
            # Recurse into subfolder
            new_prefix = prefix + "  "
            lines.extend(tree_to_strings(subtree, new_prefix))
        
        return lines

    # Generate final structure
    return tree_to_strings(tree)


def read_file_content(file_path):
    """Read content from a file.
    
    Args:
        file_path (str): Path to the file
        
    Returns:
        str: Content of the file
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        try:
            # Try another encoding if UTF-8 fails
            with open(file_path, 'r', encoding='cp949') as f:
                return f.read()
        except:
            return "[Binary file or unsupported encoding]"
    except Exception as e:
        return f"[Error reading file: {str(e)}]"


def generate_markdown(folder_path, files, folder_structure, output_file):
    """Generate a markdown report from the collected data.
    
    Args:
        folder_path (str): Base folder path
        files (list): List of files (relative paths)
        folder_structure (list): Formatted folder structure
        output_file (str): Path to output markdown file
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# File Collection Report\n\n")
        f.write(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"Base folder: `{os.path.abspath(folder_path)}`\n\n")
        
        # Write folder structure
        f.write("## Folder Structure\n\n```\n")
        for line in folder_structure:
            f.write(f"{line}\n")
        f.write("```\n\n")
        
        # Write file contents
        f.write("## File Contents\n\n")
        
        for i, file_path in enumerate(files, 1):
            full_path = os.path.join(folder_path, file_path)
            content = read_file_content(full_path)
            
            f.write(f"### {i}. {file_path}\n\n")
            f.write("```\n")
            f.write(content)
            f.write("\n```\n\n")
            
            f.write("---\n\n")


def generate_structure_only(folder_path, folder_structure, output_file):
    """Generate a markdown report with only the folder structure.
    
    Args:
        folder_path (str): Base folder path
        folder_structure (list): Formatted folder structure
        output_file (str): Path to output markdown file
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Folder Structure Report\n\n")
        f.write(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"Base folder: `{os.path.abspath(folder_path)}`\n\n")
        
        # Write folder structure
        f.write("## Folder Structure\n\n```\n")
        for line in folder_structure:
            f.write(f"{line}\n")
        f.write("```\n")


# Debug function to help diagnose .gitignore issues
def debug_gitignore(folder_path):
    """Debug function to show what .gitignore patterns are being loaded."""
    gitignore_path = os.path.join(folder_path, '.gitignore')
    
    if not os.path.isfile(gitignore_path):
        print(f"No .gitignore file found at: {gitignore_path}")
        return
    
    print(f"Loading .gitignore from: {gitignore_path}")
    print("Patterns found:")
    
    with open(gitignore_path, 'r') as f:
        for i, line in enumerate(f, 1):
            original = line.rstrip('\n')
            stripped = line.strip()
            if stripped and not stripped.startswith('#'):
                print(f"  Line {i}: '{original}' -> Pattern: '{stripped}'")
            elif stripped.startswith('#'):
                print(f"  Line {i}: '{original}' (comment, ignored)")
            else:
                print(f"  Line {i}: '{original}' (empty, ignored)")
    
    # Test specific paths
    print("\nTesting common paths:")
    test_paths = ['venv', 'venv/', 'venv/bin', 'venv/lib/python3.9/site-packages/test.py']
    
    patterns = []
    with open(gitignore_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                patterns.append(line)
    
    if patterns:
        spec = PathSpec.from_lines('gitwildmatch', patterns)
        for path in test_paths:
            matched = spec.match_file(path)
            print(f"  '{path}': {'MATCHED (will be ignored)' if matched else 'NOT MATCHED'}")