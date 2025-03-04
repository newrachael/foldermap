# Filemap

![PyPI version](https://img.shields.io/pypi/v/filemap.svg)
![Python versions](https://img.shields.io/pypi/pyversions/filemap.svg)
![License](https://img.shields.io/pypi/l/filemap.svg)

Filemap is a utility that collects files from a directory, creates a visual tree structure, and generates a comprehensive markdown report with all the file contents.

## Features

- Collect files from directories and subdirectories
- Filter files by extension
- Exclude specific folders
- Generate folder structure visualization
- Create markdown reports with file contents
- Simple command-line interface

## Installation

```bash
pip install filemap
```

## Usage

### Command Line

```bash
# Basic usage
filemap /path/to/folder

# Specify output file
filemap /path/to/folder -o report.md

# Filter files by extension
filemap /path/to/folder -e py,txt,md

# Exclude specific folders
filemap /path/to/folder -x node_modules,.git,venv

# Combine options
filemap /path/to/folder -o report.md -e py,txt -x node_modules,venv
```

### Python API

```python
from filemap import collect_files, get_folder_structure, generate_markdown

# Collect files from a directory
files = collect_files(
    folder_path="your/folder/path", 
    extensions=[".py", ".txt"],  # Optional
    exclude_folders=["venv", ".git"]  # Optional
)

# Generate folder structure
structure = get_folder_structure("your/folder/path", files)

# Generate markdown report
generate_markdown("your/folder/path", files, structure, "output.md")
```

## Example Output

The generated markdown file includes:

1. A timestamp of when the report was generated
2. The absolute path of the base folder
3. A visual tree structure of all folders and files
4. The content of each file, formatted as code blocks

Example folder structure:

```
📄 README.md
📁 filemap
  📄 __init__.py
  📄 core.py
  📄 cli.py
📁 tests
  📄 test_filemap.py
```

## License

MIT License