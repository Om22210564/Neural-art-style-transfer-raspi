# 🎨 Neural Art Style Transfer on Raspberry Pi 4

An **edge AI application** that performs neural artistic style transfer using a
**Raspberry Pi 4**, **IMX219 camera**, and **Waveshare 7-inch DSI LCD (C)**.

The system captures an image, applies a selected artistic style using
**ONNX Runtime**, and displays the stylized output in fullscreen via a custom UI.

---

## 🚀 Features

- 📸 Live image capture using IMX219 camera
- 🎨 Multiple neural art styles (ONNX models)
- ⚡ Optimized CPU inference with ONNX Runtime
- 🖥️ Fullscreen Tkinter-based UI
- 🔌 Direct DSI display (no HDMI required)

---

## 🛠️ Hardware Setup

- **Raspberry Pi 4**
- **IMX219 Camera Module**
- **Waveshare 7-inch DSI LCD (C)**

### 📷 Hardware Assembly
![Hardware Setup](docs/hardware_setup.jpg)

---

## 🧰 Software Stack

- Python 3.9+
- PyTorch (tensor utilities)
- ONNX Runtime
- Tkinter (GUI)
- rpicam-apps (camera capture)

---

## ⚙️ Raspberry Pi Configuration

After flashing Raspberry Pi OS, update:

```bash
sudo nano /boot/config.txt


Required additions:
camera_auto_detect=0
display_auto_detect=1

dtoverlay=vc4-kms-v3d
max_framebuffers=2
disable_fw_kms_setup=1

[all]
dtoverlay=vc4-kms-dsi-waveshare-panel,7_0_inchC,i2c1
dtoverlay=imx219