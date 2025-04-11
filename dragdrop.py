"""
dragdrop.py

Configures drag-and-drop for background and input image entries in SnapBack.
"""

import os
from tkinterdnd2 import DND_FILES

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
            drop_folder = os.path.join(os.path.dirname(input_files[0]), "Dropped Inputs")
            os.makedirs(drop_folder, exist_ok=True)
            for img in input_files:
                basename = os.path.basename(img)
                target = os.path.join(drop_folder, basename)
                if not os.path.exists(target):
                    try:
                        os.link(img, target)
                    except Exception:
                        import shutil
                        shutil.copy(img, target)
            state['input_type'].set("Folder")
            state['input_path'].set(drop_folder)
            update_image_count(state)

def update_image_count(state):
    folder = state['input_path'].get()
    if not os.path.isdir(folder):
        state['image_count'].set("No input folder selected.")
        return

    count = len([
        f for f in os.listdir(folder)
        if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))
    ])
    state['image_count'].set(f"{count} image(s) found.")
