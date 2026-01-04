import os
import time
import random
import sys
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox

import torch
import onnxruntime as ort
import numpy as np
from PIL import Image
import torchvision.transforms as transforms

# Set random seed
random.seed(random.randrange(sys.maxsize))

# Available ONNX models
styles = [
    "candy.onnx",
    "cubism.onnx",
    "futurism.onnx",
    "mosaic.onnx",
    "pop_art.onnx",
    "rain_princess.onnx",
    "starry_night.onnx",
]

onnx_models_dir = "models_onnx"

# ========================= IMAGE FUNCTIONS =========================
def capture_image():
    os.makedirs("images", exist_ok=True)
    filename = f"images/captured_{int(time.time())}.jpg"
    
    cmd = [
        "rpicam-still",
        "-o", filename,
        "-t", "1000",
        "--width", "1920",
        "--height", "1080",
        "--nopreview"
    ]
    
    print(f"Capturing image with command: {' '.join(cmd)}")
    try:
        subprocess.run(cmd, check=True)
        print(f"Image captured: {filename}")
        return filename
    except subprocess.CalledProcessError as e:
        print(f"❌ Error capturing image: {e}")
        sys.exit(1)

def apply_style(input_image_path, output_image_path, style_model):
    ort_session = ort.InferenceSession(os.path.join(onnx_models_dir, style_model))
    image = Image.open(input_image_path).convert("RGB")
    original_size = image.size

    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Lambda(lambda x: x.mul(255))
    ])
    input_tensor = transform(image).unsqueeze(0).numpy()

    ort_inputs = {"input_image": input_tensor}
    ort_output = ort_session.run(["output_image"], ort_inputs)[0]

    output_image = transforms.ToPILImage()(
        torch.tensor(ort_output).squeeze(0).div(255).clamp(0, 1)
    )
    output_image = output_image.resize(original_size, Image.LANCZOS)
    output_image.save(output_image_path)
    print(f"Styled image saved as: {output_image_path}")

def process_image(image_path, style_model):
    output_path = image_path.replace("captured", "styled")
    print(f"Processing {image_path} with model {style_model}")
    apply_style(image_path, output_path, style_model)
    return output_path

# ========================= UI FUNCTIONS =========================
def on_capture_button_click(style_combobox):
    selected_style = style_combobox.get()
    if not selected_style:
        messagebox.showerror("Error", "Please select a style.")
        return

    img_path = capture_image()
    styled_path = process_image(img_path, selected_style)

    os.system("pkill -f feh")
    os.system(f"DISPLAY=:0.0 feh --fullscreen {styled_path}")
    messagebox.showinfo("Success", f"Styled image saved as {styled_path}.")

def update_time(clock_label):
    current_time = time.strftime("%H:%M:%S")
    clock_label.config(text=current_time)
    clock_label.after(1000, update_time, clock_label)

# ========================= MAIN UI =========================
def create_ui():
    root = tk.Tk()
    root.title("AI Artistic Style Transfer")
    root.attributes("-fullscreen", True)  # Fullscreen mode

    # Colors and Fonts
    bg_color = "#1e1e1e"
    text_color = "#ffffff"
    accent_color = "#4CAF50"
    font_large = ("Helvetica", 32, "bold")
    font_medium = ("Helvetica", 20)
    font_small = ("Helvetica", 14)

    root.configure(bg=bg_color)

    # Header
    header_frame = tk.Frame(root, bg=bg_color)
    header_frame.pack(pady=50)

    title_label = tk.Label(header_frame, text="🎨 AI Style Transfer", font=font_large, fg=accent_color, bg=bg_color)
    title_label.pack()

    # Clock
    clock_label = tk.Label(header_frame, font=font_medium, fg=text_color, bg=bg_color)
    clock_label.pack(pady=10)
    update_time(clock_label)

    # Main Section
    main_frame = tk.Frame(root, bg=bg_color)
    main_frame.pack(expand=True)

    label = tk.Label(main_frame, text="Select an Artistic Style:", font=font_medium, fg=text_color, bg=bg_color)
    label.pack(pady=20)

    style_combobox = ttk.Combobox(main_frame, values=styles, font=font_small, width=25)
    style_combobox.set(styles[0])
    style_combobox.pack(pady=20)

    # Apply custom theme for ttk
    style = ttk.Style()
    style.theme_use("clam")
    style.configure(
        "TCombobox",
        fieldbackground="#333333",
        background="#444444",
        foreground=text_color,
        arrowcolor=text_color
    )

    capture_button = tk.Button(
        main_frame,
        text="📸 Capture & Apply Style",
        font=font_medium,
        bg=accent_color,
        fg="white",
        activebackground="#45a049",
        activeforeground="white",
        padx=20,
        pady=10,
        command=lambda: on_capture_button_click(style_combobox)
    )
    capture_button.pack(pady=40)

    # Exit button
    exit_button = tk.Button(
        root,
        text="Exit",
        font=font_small,
        bg="#ff4444",
        fg="white",
        command=root.destroy
    )
    exit_button.pack(side="bottom", pady=30)

    root.mainloop()

# ========================= MAIN =========================
if __name__ == "__main__":
    create_ui()
