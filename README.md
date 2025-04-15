# Foldermap

Foldermap is a utility that collects files from a directory, creates a visual tree structure, and generates a comprehensive markdown report with all the file contents.

## Features
* Collect files from directories and subdirectories
* Filter files by extension
* Exclude specific folders
* Generate folder structure visualization
* Create markdown reports with file contents
* Generate structure-only reports (without file contents)
* Simple command-line interface
* Option to include/exclude hidden folders (starting with .)

## Installation

```bash
pip install foldermap
```

## Usage

### Command Line

```bash
# Basic usage
foldermap /path/to/folder

# Specify output file
foldermap /path/to/folder -o report.md

# Filter files by extension
foldermap /path/to/folder -e py,txt,md

# Exclude specific folders
foldermap /path/to/folder -x node_modules,.git,venv

# Generate structure-only report (without file contents)
foldermap /path/to/folder -s

# Include hidden folders (starting with .)
foldermap /path/to/folder --include-hidden

# Combine options
foldermap /path/to/folder -o report.md -e py,txt -x node_modules,venv -s --include-hidden
```

### Python API

```python
from foldermap import collect_files, get_folder_structure, generate_markdown, generate_structure_only

# Collect files from a directory
files = collect_files(
    folder_path="your/folder/path", 
    extensions=[".py", ".txt"],  # Optional
    exclude_folders=["venv", ".git"],  # Optional
    include_hidden=False  # Optional, default is False
)

# Generate folder structure
structure = get_folder_structure("your/folder/path", files)

# Generate complete markdown report with file contents
generate_markdown("your/folder/path", files, structure, "output.md")

# Generate structure-only report (without file contents)
generate_structure_only("your/folder/path", structure, "structure.md")
```

## Example Output
The generated markdown file includes:
1. A timestamp of when the report was generated
2. The absolute path of the base folder
3. A visual tree structure of all folders and files
4. The content of each file, formatted as code blocks (for complete reports)

Example folder structure:

```
📄 README.md
📁 foldermap
  📄 __init__.py
  📄 core.py
  📄 cli.py
📁 tests
  📄 test_foldermap.py
```

## License
MIT License