"""
main.py

Entry point for SnapBack – A tool primarily used to place screenshots on top of a default background.
Saves user config between sessions, is resizable, and supports drag-and-drop.
"""

import tkinter as tk
from tkinter import ttk
from tkinterdnd2 import TkinterDnD
from PIL import ImageTk
from ui_components import build_ui
from dragdrop import configure_drag_and_drop
from logic import preview_sample, process_images
from config import load_config, save_config

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

    img.thumbnail((1000, 800))
    img_tk = ImageTk.PhotoImage(img)
    lbl = tk.Label(win, image=img_tk)
    lbl.image = img_tk  # Keep a reference
    lbl.pack(expand=True, fill=tk.BOTH)

if __name__ == "__main__":
    main()
