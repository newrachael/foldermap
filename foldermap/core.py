"""Core functionality for the foldermap package."""

import os
import datetime


def collect_files(folder_path, extensions=None, exclude_folders=None, include_hidden=False):
    """Collect files from within a folder.
    
    Args:
        folder_path (str): Path to search for files
        extensions (list, optional): List of file extensions to include
        exclude_folders (list, optional): List of folder names or paths to exclude
        include_hidden (bool, optional): Whether to include hidden folders (starting with .)
        
    Returns:
        list: List of collected file paths (relative to folder_path)
    """
    collected_files = []
    
    for root, dirs, files in os.walk(folder_path):
        # Remove excluded folders from dirs to prevent walking into them
        if exclude_folders:
            # Get the relative path from the root folder
            rel_path = os.path.relpath(root, folder_path)
            
            # Remove directories to be excluded (modifying dirs in-place affects os.walk)
            dirs[:] = [d for d in dirs if d not in exclude_folders and 
                      os.path.join(rel_path, d) not in exclude_folders]
        
        # Remove hidden folders if include_hidden is False
        if not include_hidden:
            dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in files:
            file_path = os.path.join(root, file)
            
            # Filter by specific extensions
            if extensions:
                file_ext = os.path.splitext(file)[1].lower()
                if file_ext not in extensions:
                    continue
            
            # Calculate relative path
            rel_path = os.path.relpath(file_path, folder_path)
            collected_files.append(rel_path)
    
    return collected_files


def get_folder_structure(folder_path, files):
    """Create a tree representation of the folder structure.
    
    Args:
        folder_path (str): Base folder path
        files (list): List of files (relative paths)
        
    Returns:
        list: Formatted strings representing the folder structure
    """
    # Extract folder paths from files
    folders = set()
    for file_path in files:
        dir_path = os.path.dirname(file_path)
        if dir_path:
            folders.add(dir_path)
    
    # Create folder structure
    structure = []
    root_folders = set()
    
    # Find root folders
    for folder in folders:
        parts = folder.split(os.sep)
        root_folders.add(parts[0])
    
    # Sort folder and file lists
    sorted_folders = sorted(list(folders))
    sorted_files = sorted(files)
    
    # Create folder structure representation
    prev_level = 0
    for folder in sorted_folders:
        level = folder.count(os.sep) + 1
        indent = "  " * level
        folder_name = os.path.basename(folder)
        structure.append(f"{indent}📁 {folder_name}")
    
    # Add files to structure
    file_structure = []
    for file_path in sorted_files:
        dir_path = os.path.dirname(file_path)
        file_name = os.path.basename(file_path)
        level = file_path.count(os.sep) + 1
        indent = "  " * level
        
        # Check if the folder containing the file is included in the structure
        if dir_path in folders or dir_path == "":
            file_structure.append((file_path, f"{indent}📄 {file_name}"))
    
    # Create final structure with proper ordering
    final_structure = []
    current_dir = ""
    
    # Handle root files
    root_files = [f for f in sorted_files if os.sep not in f]
    if root_files:
        for file in root_files:
            final_structure.append(f"📄 {file}")
    
    # Process folders
    for folder in sorted_folders:
        parts = folder.split(os.sep)
        depth = len(parts)
        indent = "  " * (depth - 1)
        final_structure.append(f"{indent}📁 {parts[-1]}")
        
        # Add direct child files of this folder
        for file_path, file_str in file_structure:
            if os.path.dirname(file_path) == folder:
                final_structure.append(file_str)
    
    return final_structure


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