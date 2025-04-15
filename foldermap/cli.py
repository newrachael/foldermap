"""Command-line interface for the foldermap package."""

import os
import argparse
import sys
from .core import (
    collect_files,
    get_folder_structure,
    generate_markdown,
    generate_structure_only
)


def main():
    """Main entry point for the command-line interface."""
    parser = argparse.ArgumentParser(
        description='Collect files from a folder and save their contents to a markdown file'
    )
    parser.add_argument('folder_path', help='Path to the folder to search')
    parser.add_argument(
        '-o', '--output', 
        default='collected_files.md', 
        help='Path to the output markdown file (default: collected_files.md)'
    )
    parser.add_argument(
        '-e', '--extensions', 
        help='File extensions to collect (comma-separated, e.g., .txt,.py,.md)'
    )
    parser.add_argument(
        '-x', '--exclude', 
        help='Folders to exclude (comma-separated, e.g., node_modules,venv,.git)'
    )
    parser.add_argument(
        '-s', '--structure-only',
        action='store_true',
        help='Output only the folder structure without file contents'
    )
    parser.add_argument(
        '--include-hidden',
        action='store_true',
        help='Include hidden folders (starting with .) in the output'
    )
    
    args = parser.parse_args()
    
    # Process extensions
    extensions = None
    if args.extensions:
        extensions = [ext.strip().lower() for ext in args.extensions.split(',')]
        # Add dot to extensions if not present
        extensions = [ext if ext.startswith('.') else f'.{ext}' for ext in extensions]
    
    # Process excluded folders
    exclude_folders = None
    if args.exclude:
        exclude_folders = [folder.strip() for folder in args.exclude.split(',')]
    
    print(f"Searching folder '{args.folder_path}'...")
    
    # Collect files (store relative paths)
    files = collect_files(args.folder_path, extensions, exclude_folders, args.include_hidden)
    print(f"Found {len(files)} files.")
    
    # Generate folder structure
    folder_structure = get_folder_structure(args.folder_path, files)
    
    # Generate output based on the structure-only flag
    if args.structure_only:
        generate_structure_only(args.folder_path, folder_structure, args.output)
        print(f"Done! Folder structure saved to '{args.output}'.")
    else:
        generate_markdown(args.folder_path, files, folder_structure, args.output)
        print(f"Done! Full report saved to '{args.output}'.")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())