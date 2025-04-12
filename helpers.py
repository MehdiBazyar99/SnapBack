"""
helpers.py

Utility functions for SnapBack: handling paths, image sizes, and scaling.
"""

import os
from PIL import Image

def safe_scale(scale_str, default=100.0):
    try:
        val = float(scale_str)
        if val <= 0:
            raise ValueError
        return val
    except ValueError:
        return default

def get_output_folder(state):
    preset = state['output_folder_option'].get()
    if preset == "Same as input":
        in_path = state['input_path'].get()
        if state['input_type'].get() == "File":
            return os.path.dirname(in_path)
        return in_path
    elif preset == "Desktop":
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        return desktop_path
    elif preset == "Custom":
        return state['custom_output_path'].get()
    return ""

def get_output_size(state, original_size):
    preset = state['size_preset'].get()
    if preset == "Same as background":
        return original_size
    elif preset == "1920×1080":
        return (1920, 1080)
    elif preset == "1920×1280":
        return (1920, 1280)
    elif preset == "Custom":
        try:
            w = int(state['custom_width'].get())
            h = int(state['custom_height'].get())
            if w > 0 and h > 0:
                return (w, h)
            else:
                return original_size
        except ValueError:
            return original_size
    return original_size

def calculate_position(bg_size, fg_size, alignment):
    bg_w, bg_h = bg_size
    fg_w, fg_h = fg_size

    positions = {
        "Center":       ((bg_w - fg_w) // 2, (bg_h - fg_h) // 2),
        "Top-left":     (0, 0),
        "Top-right":    (bg_w - fg_w, 0),
        "Bottom-left":  (0, bg_h - fg_h),
        "Bottom-right": (bg_w - fg_w, bg_h - fg_h),
    }
    return positions.get(alignment, (0, 0))

def resize_input_relative(image, scale):
    """
    Resize the image by a given scale (e.g., 1.1 for 110%, 0.9 for 90%).
    """
    w, h = image.size
    new_w = int(w * scale)
    new_h = int(h * scale)
    return image.resize((new_w, new_h), Image.Resampling.LANCZOS)



