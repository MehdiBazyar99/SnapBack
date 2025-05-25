"""
main.py

Entry point for SnapBack – A tool primarily used to place screenshots on top of a default background.
Saves user config between sessions, is resizable, and supports drag-and-drop.
"""

import tkinter as tk
from tkinter import ttk
from tkinterdnd2 import TkinterDnD
import shutil # Added import
import os # Added import
from PIL import ImageTk, Image # Ensure Image is imported for Image.Resampling
from ui_components import build_ui
from dragdrop import configure_drag_and_drop
from logic import preview_sample, process_images
from config import load_config, save_config

# Define APP_DATA_DIR (consistent with dragdrop.py)
APP_DATA_DIR = os.path.join(os.path.expanduser("~"), ".snapback")

def main():
    # Load last-saved user configuration
    user_config = load_config()

    # CHANGED: Renamed window title to "SnapBack"
    root = TkinterDnD.Tk()
    root.title("SnapBack")
    # Apply last window geometry from config (or default)
    root.geometry(user_config.get('window_geometry', "900x700"))
    root.resizable(True, True)

    # Configure style
    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure("TNotebook.Tab", padding=(12, 8))
    style.configure("TButton", font=('Segoe UI', 10))
    style.configure("TLabel", font=('Segoe UI', 10))
    style.configure("Header.TLabel", font=('Segoe UI', 12, 'bold'))

    # Build UI
    state = build_ui(root, user_config)

    # Connect buttons
    state['preview_button'].config(command=lambda: show_preview(preview_sample(state)))
    state['process_button'].config(command=lambda: process_images(state))

    # Enable drag and drop
    configure_drag_and_drop(root, state)

    # On close, save config
    def on_closing():
        geometry = root.winfo_geometry().split('+')[0]  # e.g. '900x700'
        save_config(state, geometry)
        # Cleanup "Dropped Inputs" folder
        drop_folder_path = os.path.join(APP_DATA_DIR, "Dropped Inputs")
        if os.path.exists(drop_folder_path):
            shutil.rmtree(drop_folder_path)
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

def show_preview(img):
    """
    Create a top-level window to display a composited preview image.
    """
    if img is None:
        return
    win = tk.Toplevel()
    win.title("Preview")
    win.resizable(True, True)

    # Store the original image on the label for access in the resize handler
    lbl = tk.Label(win) # Create label first
    lbl.original_image = img # Store original PIL image
    lbl.pack(expand=True, fill=tk.BOTH)

    # Bind the resize event
    win.bind('<Configure>', lambda event: resize_preview_image(event, lbl))

    # Perform initial sizing after window is drawn
    win.update_idletasks() 
    # Call resize_preview_image once to set the initial image correctly
    # We pass a dummy event-like object for the first call if needed, or rely on lbl dimensions
    class DummyEvent:
        def __init__(self, width, height):
            self.width = width
            self.height = height
    
    resize_preview_image(DummyEvent(lbl.winfo_width(), lbl.winfo_height()), lbl)


def resize_preview_image(event, lbl):
    """
    Resize the preview image when the window is resized.
    """
    if not hasattr(lbl, 'original_image') or lbl.original_image is None:
        return

    original_img = lbl.original_image
    
    # Get label's current size
    # Use event.width and event.height if they are reliably > 0, otherwise fallback
    # to lbl.winfo_width/height, but these can also be 0 or 1 initially on some platforms.
    # A small delay or update_idletasks() before first call helps.
    widget_width = lbl.winfo_width()
    widget_height = lbl.winfo_height()

    if widget_width <= 1 or widget_height <= 1: # Avoid issues with zero or minimal dimensions
        return

    # Create a copy of the original image to resize
    img_copy = original_img.copy()

    # Resize the copy using thumbnail to maintain aspect ratio
    # Use Image.Resampling.LANCZOS for high-quality downscaling
    img_copy.thumbnail((widget_width, widget_height), Image.Resampling.LANCZOS)

    # Create a new PhotoImage
    img_tk = ImageTk.PhotoImage(img_copy)

    # Update the label
    lbl.config(image=img_tk)
    lbl.image = img_tk # Keep a reference


if __name__ == "__main__":
    main()
