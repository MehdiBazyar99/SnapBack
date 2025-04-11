"""
config.py

Handles saving/loading the SnapBack configuration (paths, dropdowns, etc.),
but does NOT store input_path or input_type. Only background_path, output
and sizing settings, and window geometry are saved.
"""

import os
import json

CONFIG_FILE = os.path.join(os.path.expanduser("~"), ".snapback_config.json")

# Default config
# Removed 'input_path' and 'input_type'
DEFAULT_CONFIG = {
    'background_path': "",
    'custom_output_path': "",
    'output_folder_option': "Same as input",
    'filename_postfix': "_composited",
    'output_format': "PNG",
    'size_preset': "Same as background",
    'custom_width': "",
    'custom_height': "",
    'position_option': "Center",
    'resize_scale': "90",
    'window_geometry': "900x700",
}

def load_config():
    if not os.path.exists(CONFIG_FILE):
        return DEFAULT_CONFIG.copy()
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            config = DEFAULT_CONFIG.copy()
            config.update(data)
            return config
    except Exception:
        return DEFAULT_CONFIG.copy()

def save_config(state, geometry):
    """
    Save only the keys in DEFAULT_CONFIG (excludes input_path/input_type).
    """
    data = {}
    for key in DEFAULT_CONFIG.keys():
        if key == 'window_geometry':
            data['window_geometry'] = geometry
        else:
            data[key] = state[key].get()
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"⚠️ Could not save config: {e}")
