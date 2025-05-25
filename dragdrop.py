"""
dragdrop.py

Configures drag-and-drop for background and input image entries in SnapBack.
"""

import os
import shutil # Added import
from tkinterdnd2 import DND_FILES
from helpers import update_image_count # Added import

# Define APP_DATA_DIR
APP_DATA_DIR = os.path.join(os.path.expanduser("~"), ".snapback")

def configure_drag_and_drop(root, state):
    """
    Register the drag-and-drop targets (entries), linking them to the handlers.
    """
    state['bg_entry'].drop_target_register(DND_FILES)
    state['bg_entry'].dnd_bind('<<Drop>>', lambda e: handle_background_drop(e, state))

    state['input_entry'].drop_target_register(DND_FILES)
    state['input_entry'].dnd_bind('<<Drop>>', lambda e: handle_input_drop(e, state))

def handle_background_drop(event, state):
    """
    Process a dropped file/folder for the background.
    Only the first valid image file is taken.
    """
    # CHANGED: parse paths using splitlist
    paths_list = event.widget.tk.splitlist(event.data)
    for raw_path in paths_list:
        clean_path = raw_path.strip('{}')  # remove any curly braces
        if os.path.isfile(clean_path) and clean_path.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            state['background_path'].set(clean_path)
            return

def handle_input_drop(event, state):
    """
    Process dropped file(s) or folder(s) for the input images.
    If multiple files are dropped, they are placed in 'Dropped Inputs' subfolder.
    """
    # CHANGED: parse paths using splitlist
    paths_list = event.widget.tk.splitlist(event.data)
    input_files = []

    for raw_path in paths_list:
        clean_path = raw_path.strip('{}')
        if os.path.isdir(clean_path):
            state['input_type'].set("Folder")
            state['input_path'].set(clean_path)
            update_image_count(state)
            return
        elif os.path.isfile(clean_path):
            input_files.append(clean_path)

    if input_files:
        if len(input_files) == 1:
            state['input_type'].set("File")
            state['input_path'].set(input_files[0])
            state['image_count'].set("1 image selected.")
        else:
            # Use APP_DATA_DIR for the drop_folder
            drop_folder = os.path.join(APP_DATA_DIR, "Dropped Inputs")
            os.makedirs(drop_folder, exist_ok=True) # Ensure directory exists
            for img in input_files:
                basename = os.path.basename(img)
                target = os.path.join(drop_folder, basename)
                # Always use shutil.copy2 and overwrite if exists
                shutil.copy2(img, target)
            state['input_type'].set("Folder")
            state['input_path'].set(drop_folder)
            update_image_count(state)
