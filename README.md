# Text File Collector

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![PyQt5](https://img.shields.io/badge/PyQt5-5.15+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)

## Description

**Text File Collector** is a convenient application for combining multiple text files into a single document. The program supports drag-and-drop, folder processing, language selection, and features a modern dark/light interface.

### Key Features

- Drag & Drop — drag files and folders directly into the application window
- Batch loading — add entire folders with recursive traversal
- Bilingual interface — Russian and English languages
- Dark/Light theme — switch with one click
- Statistics — file count, line count, and total size
- Copy — copy result to clipboard
- Save — save result to text file
- Auto-rename — automatic renaming when duplicates are detected
- Management — delete individual files or all at once
- Path display — shows only the last folder for compactness

## Installation

### Requirements

- Python 3.7 or higher
- pip (Python package manager)

### Step 1: Clone the repository

git clone https://github.com/your-username/text-glitcher.git
cd text-glitcher

### Step 2: Install dependencies

pip install -r requirements.txt

Or manually:

pip install PyQt5 pyinstaller

### Step 3: Run

python main.py

## Building EXE

### Windows

# Install PyInstaller
pip install pyinstaller

# Build with icon
pyinstaller --onefile --windowed --icon=icon.ico --name="TextGlitcher" main.py

# Or without icon
pyinstaller --onefile --windowed --name="TextGlitcher" main.py

The ready EXE file will appear in the dist/ folder.

### Linux/macOS

pyinstaller --onefile --windowed --name="TextGlitcher" main.py

## Usage

### Quick Start

1. Launch the application
2. Add files in one of the following ways:
   - Drag files into the folder zone
   - Click "Add Files" and select files
   - Click "Add Folder" and select a folder
3. The result will automatically appear in the right panel
4. Copy the result to clipboard or save to file

### Supported Formats

- .txt — Text files
- .log — Log files
- .csv — Tabular data
- .json — JSON data
- .xml — XML documents
- .md — Markdown files
- .py — Python scripts
- .js — JavaScript files
- .html — HTML pages
- .css — CSS styles
- .ini, .cfg, .conf — Configuration files

### Keyboard Shortcuts

- Ctrl+O — Open files
- Ctrl+Shift+O — Open folder
- Ctrl+C — Copy result
- Ctrl+S — Save result
- Ctrl+Shift+C — Clear all files
- Ctrl+Shift+R — Clear result

## Technologies

- Python 3.7+ — programming language
- PyQt5 — graphical interface
- PyInstaller — EXE building

## Project Structure

text-glitcher/
├── main.py              # Main application file
├── requirements.txt     # Dependencies
├── icon.ico            # Application icon (optional)
├── README.md           # This file
├── LICENSE             # License
└── build/              # Build folder (auto-generated)
    └── dist/           # Ready EXE file

## Contributing

We welcome any contributions to the project!

1. Report a bug — create an Issue describing the problem
2. Suggest an idea — tell us what can be improved
3. Submit a Pull Request — fix a bug or add a new feature

### Development

# Clone the repository
git clone https://github.com/your-username/text-glitcher.git

# Create a branch for the new feature
git checkout -b feature/amazing-feature

# Make changes and commit
git commit -m 'Add some amazing feature'

# Push changes
git push origin feature/amazing-feature

## License

This project is distributed under the MIT license.

## Acknowledgments

- PyQt5 — for the excellent GUI framework
- PyInstaller — for convenient application building

## Contact

- Author: Your Name
- Email: Your Email
- GitHub: Your GitHub

---

⭐ If you like the application, give it a star on GitHub!

---

## Known Issues and Solutions

### Issue: Files with Russian characters in the path don't open

Solution: Make sure the file is saved in UTF-8 encoding. The application automatically tries to read files in UTF-8 and CP1251 encodings.

### Issue: EXE doesn't compile with icon

Solution:
1. Make sure the icon.ico file exists in the project folder
2. Use the absolute path to the icon: --icon="C:\full\path\to\icon.ico"
3. Try building without icon: pyinstaller --onefile --windowed --name="TextGlitcher" main.py

### Issue: Application doesn't run on Windows 7

Solution: Install Microsoft Visual C++ Redistributable for Visual Studio 2015-2022.

## Version History

### Version 1.0.0 (2024)

- First release
- Russian and English language support
- Dark and light themes
- Drag & Drop
- Support for 13+ file formats
- EXE building

---

Made with ❤️ using Python and PyQt5

---

**How to save:**

1. Select ALL the text above (from the first line to the last)
2. Press Ctrl+C (copy)
3. Open Notepad
4. Press Ctrl+V (paste)
5. Click File → Save As...
6. In the "File name" field, type: README.md
7. In the "Save as type" field, select "All files (*.*)"
8. Click "Save"

Done! Now you have a README.md file.
