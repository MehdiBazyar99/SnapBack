<details> <summary>README.md</summary>
css
Copy
Edit
# SnapBack

A modern, resizable Tkinter application primarily used to place screenshots on top of a default background.  
Allows you to specify a background image, one or many input images, alignment, resizing, and save the final composited result.

## Features

- Remembers your last background, output folder settings, and position/sizing settings (but **not** your last input image).
- Drag-and-drop support for quickly selecting background/input images/folders.
- Resizable UI with a Notebook interface for easy navigation of settings.
- Batch-processing for multiple images in a folder.

## Installation & Running

1. **Clone this repository**:
git clone https://github.com/<YourUsername>/Overlay-Composit.git cd Overlay-Composit

markdown
Copy
Edit
2. **Install dependencies**:
pip install -r requirements.txt

markdown
Copy
Edit
Dependencies typically include:
- `Pillow`
- `tkinterdnd2`

3. **Run the app**:
python main.py

less
Copy
Edit
On Windows, you may need `python -m pip install tkinterdnd2` if you don’t have it installed.

## Building a Windows .exe

We can use [PyInstaller](https://pyinstaller.org/) to create a standalone .exe:

1. Install PyInstaller if you haven’t:
pip install pyinstaller

arduino
Copy
Edit
2. In the project folder, run:
pyinstaller --onefile --windowed --icon=snapback_logo.ico --name=SnapBack main.py

markdown
Copy
Edit
Explanation:
- `--onefile`: Packs everything into a single exe.
- `--windowed`: No console window appears.
- `--icon=snapback_logo.ico`: Uses your custom icon for the exe.
- `--name=SnapBack`: Sets output exe name to `SnapBack.exe`.

3. After it finishes, check the `dist/` folder – you’ll find `SnapBack.exe`.  
You can share that `.exe` with others, and they won’t need Python installed (though some users may need the Visual C++ Redistributable libraries if not present).

## Usage

1. **Background**: Provide or drag-and-drop a background image.
2. **Input**: Choose “File” or “Folder” to overlay one image or many. Or drag-and-drop them.
3. **Output Settings**: Decide where to save, format, and filename postfix.
4. **Position & Sizing**: Customize exact output resolution, alignment, and scaling if the input is larger.
5. **Preview**: Click “Preview Sample” to see how one image looks before processing all.
6. **Process**: Click “Process Images” to batch-composite.

## License

(Choose a license and place it here – MIT, GPL, or whichever you prefer.)
</details>