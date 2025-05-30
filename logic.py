"""
logic.py

Implements compositing logic for SnapBack (preview + batch processing).
"""

import os
from PIL import Image
from helpers import (
    get_output_folder,
    get_output_size,
    calculate_position,
    resize_input_relative,
    safe_scale
)

def preview_sample(state):
    try:
        bg_path = state['background_path'].get()
        in_path = state['input_path'].get()
        if not (bg_path and in_path):
            raise ValueError("Select background and input first.")

        background = Image.open(bg_path).convert("RGBA")
        out_size = get_output_size(state, background.size)
        background = background.resize(out_size)

        input_type = state['input_type'].get()
        sample_file = in_path if input_type == "File" else get_first_image_in_folder(in_path)
        if not sample_file:
            raise FileNotFoundError("No valid input image found.")

        foreground = Image.open(sample_file).convert("RGBA")
        scale = safe_scale(state['resize_scale'].get()) / 100.0
        resized_fg = resize_input_relative(foreground, scale)

        pos = calculate_position(background.size, resized_fg.size, state['position_option'].get())
        background.paste(resized_fg, pos, resized_fg)

        return background
    except Exception as e:
        from tkinter import messagebox
        messagebox.showerror("Preview Error", str(e))
        return None

def process_images(state):
    from tkinter import messagebox

    bg_path = state['background_path'].get()
    in_path = state['input_path'].get()
    out_path = get_output_folder(state)
    postfix = state['filename_postfix'].get().strip() or "_composited"
    fmt = state['output_format'].get().lower()
    alignment = state['position_option'].get()
    scale = safe_scale(state['resize_scale'].get()) / 100.0

    if not (bg_path and in_path and out_path):
        messagebox.showerror("Error", "Please select background, input, and output paths.")
        return

    try:
        os.makedirs(out_path, exist_ok=True)
        background = Image.open(bg_path).convert("RGBA")
        out_size = get_output_size(state, background.size)
        background = background.resize(out_size)

        if state['input_type'].get() == "File":
            input_files = [in_path]
        else:
            input_files = get_all_images(in_path)

        if not input_files:
            messagebox.showwarning("No Images", "No valid input images found.")
            return

        state['progress_bar']['maximum'] = len(input_files)
        state['progress_bar']['value'] = 0

        for idx, file_path in enumerate(input_files):
            try:
                foreground = Image.open(file_path).convert("RGBA")
                fg_resized = resize_input_relative(foreground, scale)

                bg_copy = background.copy()
                pos = calculate_position(bg_copy.size, fg_resized.size, alignment)
                bg_copy.paste(fg_resized, pos, fg_resized)

                name = os.path.splitext(os.path.basename(file_path))[0]
                save_path = os.path.join(out_path, f"{name}{postfix}.{fmt}")

                save_kwargs = {"quality": 90} if fmt in ["jpg", "jpeg"] else {}
                final_mode = "RGB" if fmt in ["jpg", "jpeg"] else "RGBA"
                bg_copy.convert(final_mode).save(save_path, **save_kwargs)
            except Exception as e:
                print(f"⚠️ Error processing {file_path}: {e}")

            state['progress_bar']['value'] = idx + 1
            state['progress_bar'].update_idletasks()

        messagebox.showinfo("Done", f"✅ Processed {len(input_files)} image(s).")

    except Exception as e:
        messagebox.showerror("Processing Error", str(e))

def get_first_image_in_folder(folder):
    if not os.path.isdir(folder):
        return None
    for f in os.listdir(folder):
        if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            return os.path.join(folder, f)
    return None

def get_all_images(folder):
    if not os.path.isdir(folder):
        return []
    return [
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))
    ]
