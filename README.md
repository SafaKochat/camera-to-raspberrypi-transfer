# 📸 Raspberry Pi Automatic Photo Transfer System

A Python-based automation project that captures images from a webcam at fixed intervals and securely transfers them to a Raspberry Pi using SSH and SCP. The system runs continuously and is designed for lightweight IoT/edge-computing use cases.

---

## 🚀 Features

- 📷 Real-time image capture using OpenCV
- 🖼️ Automatic image resizing for optimized transfer
- ⏱️ Configurable time interval between captures
- 🔐 Secure file transfer via SSH (Paramiko)
- 📡 SCP transfer to Raspberry Pi directory
- 🧹 Automatic deletion of local images after transfer
- 🔄 Continuous loop execution (automation mode)

---

## 🛠️ Technologies Used

- Python 3
- OpenCV
- Paramiko (SSH connection)
- SCP (file transfer)
- Raspberry Pi (remote device)
- Linux file system

---

---

## ⚙️ Configuration

Before running the script, update the following variables in `photo_transfer.py`:

```python
REMOTE_HOST = "192.168.1.10"
REMOTE_USER = "hp"
REMOTE_PASSWORD = "raspberrypi"
REMOTE_PATH = "/media/hp/MyMedia USB/ps/ps/images"

PHOTO_INTERVAL = 60  # seconds between captures
