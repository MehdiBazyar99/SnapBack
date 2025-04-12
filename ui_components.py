"""
ui_components.py

Builds the UI for SnapBack, storing user state in a dictionary of tkinter variables.
We do NOT store input_path / input_type in config, so they reset each run.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox

def build_ui(root, user_config):
    """
    Build and return the main UI as a dictionary of references to the created elements (state).
    :param root: The root Tkinter window.
    :param user_config: The config loaded from config.py (which won't include input_path/input_type).
    :return: A dict of tkinter StringVars + references to certain widgets (for drag/drop).
    """
    # Set default window dimensions to 420x380
    root.geometry("420x380")
    # Main frame
    main_frame = ttk.Frame(root, padding=10)
    main_frame.grid(row=0, column=0, sticky='nsew')
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    main_frame.columnconfigure(0, weight=1)
    main_frame.rowconfigure(1, weight=1)

    # Menubar
    menubar = tk.Menu(root)
    _build_menus(menubar, root)
    root.config(menu=menubar)

    # Notebook
    notebook = ttk.Notebook(main_frame)
    notebook.grid(row=0, column=0, sticky='nsew')
    main_frame.rowconfigure(0, weight=1)

    # The State dictionary:
    #
    # Some keys read from user_config, others are always default:
    #   - input_type, input_path always revert to defaults (not in config).
    #   - background_path is loaded from config.
    #   - the rest (output, position, size) are loaded from config.
    state = {
        # Not saved in config:
        'input_type':    tk.StringVar(value="Folder"),
        'input_path':    tk.StringVar(value=""), 
        # Saved in config:
        'background_path':     tk.StringVar(value=user_config.get('background_path', "")),
        'custom_output_path':  tk.StringVar(value=user_config.get('custom_output_path', "")),
        'output_folder_option':tk.StringVar(value=user_config.get('output_folder_option', "Same as input")),
        'filename_postfix':    tk.StringVar(value=user_config.get('filename_postfix', "_composited")),
        'output_format':       tk.StringVar(value=user_config.get('output_format', "PNG")),
        'size_preset':         tk.StringVar(value=user_config.get('size_preset', "Same as background")),
        'custom_width':        tk.StringVar(value=user_config.get('custom_width', "")),
        'custom_height':       tk.StringVar(value=user_config.get('custom_height', "")),
        'position_option':     tk.StringVar(value=user_config.get('position_option', "Center")),
        'resize_scale':        tk.StringVar(value=user_config.get('resize_scale', "90")),
        'image_count':         tk.StringVar(value=''),  # for display in status bar
    }

    # Tabs
    tab_bg_input = ttk.Frame(notebook, padding=10)
    tab_output   = ttk.Frame(notebook, padding=10)
    tab_advanced = ttk.Frame(notebook, padding=10)

    notebook.add(tab_bg_input, text="Background & Input")
    notebook.add(tab_output,   text="Output Settings")
    notebook.add(tab_advanced, text="Position & Sizing")

    _build_tab_bg_input(tab_bg_input, state)
    _build_tab_output(tab_output, state)
    _build_tab_advanced(tab_advanced, state)

    # Status frame
    status_frame = ttk.Frame(main_frame)
    status_frame.grid(row=1, column=0, sticky='ew', pady=(5, 0))
    status_frame.columnconfigure(1, weight=1)

    lbl_count = ttk.Label(status_frame, textvariable=state['image_count'], foreground="blue")
    lbl_count.grid(row=0, column=0, padx=(5, 5))
    state['progress_bar'] = ttk.Progressbar(status_frame, mode='determinate')
    state['progress_bar'].grid(row=0, column=1, sticky='ew', padx=5, pady=2)

    return state

def _build_menus(menubar, root):
    filemenu = tk.Menu(menubar, tearoff=False)
    filemenu.add_command(label="Exit", command=root.destroy)
    menubar.add_cascade(label="File", menu=filemenu)

    helpmenu = tk.Menu(menubar, tearoff=False)
    helpmenu.add_command(label="About", command=_show_about_dialog)
    menubar.add_cascade(label="Help", menu=helpmenu)

def _show_about_dialog():
    messagebox.showinfo(
        title="About SnapBack",
        message=(
            "SnapBack\n\n"
            "A modern, resizable Tkinter application primarily used to place screenshots\n"
            "on top of a default background.\n\n"
            "Developed by Mehdi Bazyar\n"
            "GitHub: https://github.com/MehdiBazyar99/"
        )
    )

def _build_tab_bg_input(frame, state):
    frame.columnconfigure(1, weight=1)

    row = 0
    lbl_bg = ttk.Label(frame, text="🖼 Background Image", style="Header.TLabel")
    lbl_bg.grid(row=row, column=0, columnspan=3, sticky='w')

    row += 1
    ttk.Label(frame, text="Background:").grid(row=row, column=0, sticky='w', padx=5, pady=2)
    bg_entry = ttk.Entry(frame, textvariable=state['background_path'], width=50)
    bg_entry.grid(row=row, column=1, sticky='ew', padx=5, pady=2)
    state['bg_entry'] = bg_entry

    ttk.Button(frame, text="Browse", command=lambda: _select_background(state)).grid(
        row=row, column=2, padx=5, pady=2
    )

    row += 1
    lbl_input = ttk.Label(frame, text="📁 Input Images", style="Header.TLabel")
    lbl_input.grid(row=row, column=0, columnspan=3, sticky='w', pady=(8, 0))

    row += 1
    ttk.Label(frame, text="Input Type:").grid(row=row, column=0, sticky='w', padx=5, pady=2)
    om_input_type = ttk.OptionMenu(frame, state['input_type'], state['input_type'].get(), "Folder", "File")
    om_input_type.grid(row=row, column=1, sticky='w', padx=5, pady=2)

    row += 1
    ttk.Label(frame, text="Input:").grid(row=row, column=0, sticky='w', padx=5, pady=2)
    input_entry = ttk.Entry(frame, textvariable=state['input_path'], width=50)
    input_entry.grid(row=row, column=1, sticky='ew', padx=5, pady=2)
    state['input_entry'] = input_entry

    ttk.Button(frame, text="Browse", command=lambda: _select_input(state)).grid(
        row=row, column=2, padx=5, pady=2
    )

    row += 1
    btn_frame = ttk.Frame(frame)
    btn_frame.grid(row=row, column=0, columnspan=3, pady=(12, 0), sticky='ew')

    state['preview_button'] = ttk.Button(btn_frame, text="🔍 Preview Sample")
    state['preview_button'].pack(side='left', padx=10)

    state['process_button'] = ttk.Button(btn_frame, text="✅ Process Images")
    state['process_button'].pack(side='left')

def _build_tab_output(frame, state):
    frame.columnconfigure(1, weight=1)

    row = 0
    lbl_output = ttk.Label(frame, text="💾 Output Settings", style="Header.TLabel")
    lbl_output.grid(row=row, column=0, columnspan=3, sticky='w')

    row += 1
    ttk.Label(frame, text="Save to:").grid(row=row, column=0, sticky='w', padx=5, pady=2)
    om_output_folder = ttk.OptionMenu(
        frame,
        state['output_folder_option'],
        state['output_folder_option'].get(),
        "Same as input",
        "Desktop",
        "Custom"
    )
    om_output_folder.grid(row=row, column=1, sticky='w', padx=5, pady=2)

    row += 1
    ttk.Label(frame, text="Custom Folder:").grid(row=row, column=0, sticky='w', padx=5, pady=2)
    custom_out_entry = ttk.Entry(frame, textvariable=state['custom_output_path'], width=50)
    custom_out_entry.grid(row=row, column=1, sticky='ew', padx=5, pady=2)
    ttk.Button(frame, text="Browse", command=lambda: _select_output_folder(state)).grid(
        row=row, column=2, padx=5, pady=2
    )

    row += 1
    ttk.Label(frame, text="Filename Postfix:").grid(row=row, column=0, sticky='w', padx=5, pady=2)
    ttk.Entry(frame, textvariable=state['filename_postfix']).grid(row=row, column=1, sticky='w', padx=5, pady=2)

    row += 1
    ttk.Label(frame, text="Image Format:").grid(row=row, column=0, sticky='w', padx=5, pady=2)
    om_format = ttk.OptionMenu(
        frame,
        state['output_format'],
        state['output_format'].get(),
        "PNG",
        "JPG",
        "WEBP"
    )
    om_format.grid(row=row, column=1, sticky='w', padx=5, pady=2)

def _build_tab_advanced(frame, state):
    frame.columnconfigure(1, weight=1)

    row = 0
    lbl_size = ttk.Label(frame, text="📏 Output Size", style="Header.TLabel")
    lbl_size.grid(row=row, column=0, columnspan=3, sticky='w')

    row += 1
    ttk.Label(frame, text="Size Preset:").grid(row=row, column=0, sticky='w', padx=5, pady=2)
    om_size_preset = ttk.OptionMenu(
        frame,
        state['size_preset'],
        state['size_preset'].get(),
        "Same as background",
        "1920×1080",
        "1920×1280",
        "Custom"
    )
    om_size_preset.grid(row=row, column=1, sticky='w', padx=5, pady=2)

    row += 1
    ttk.Label(frame, text="Custom Size:").grid(row=row, column=0, sticky='w', padx=5, pady=2)
    size_frame = ttk.Frame(frame)
    size_frame.grid(row=row, column=1, sticky='w')
    tk.Entry(size_frame, textvariable=state['custom_width'], width=7).pack(side='left', padx=(0,2))
    ttk.Label(size_frame, text="×").pack(side='left', padx=2)
    tk.Entry(size_frame, textvariable=state['custom_height'], width=7).pack(side='left')

    row += 1
    ttk.Label(frame, text="Resize Overlay (%):").grid(row=row, column=0, sticky='w', padx=5, pady=2)
    tk.Entry(frame, textvariable=state['resize_scale'], width=10).grid(row=row, column=1, sticky='w', padx=5, pady=2)

    row += 1
    lbl_pos = ttk.Label(frame, text="📍 Position on Background", style="Header.TLabel")
    lbl_pos.grid(row=row, column=0, columnspan=3, sticky='w', pady=(10, 0))

    row += 1
    ttk.Label(frame, text="Alignment:").grid(row=row, column=0, sticky='w', padx=5, pady=2)
    om_position = ttk.OptionMenu(
        frame,
        state['position_option'],
        state['position_option'].get(),
        "Center",
        "Top-left",
        "Top-right",
        "Bottom-left",
        "Bottom-right"
    )
    om_position.grid(row=row, column=1, sticky='w', padx=5, pady=2)

def _select_background(state):
    path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.webp")])
    if path:
        state['background_path'].set(path)

def _select_input(state):
    if state['input_type'].get() == "Folder":
        path = filedialog.askdirectory()
    else:
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.webp")])
    if path:
        state['input_path'].set(path)

def _select_output_folder(state):
    path = filedialog.askdirectory()
    if path:
        state['custom_output_path'].set(path)
