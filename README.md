# VideoCompressorForDiscord

Easily compress and convert videos for Discord using **VideoCompressorForDiscord**! This simple Windows app trims your video to the final 30 seconds and optimizes it for Discord.

It is designed specifically for **non-Nitro** users who need their videos to be **10MB or less** to send them in Discord chats. The user-friendly interface lets you select a video, choose an output file, and track progress with a status bar.

---

## 🛠️ How to Install

### 1️⃣ Install Python
You need **Python 3.8 or newer**. Download and install it from:
👉 [Python Official Site](https://www.python.org/downloads/)

Make sure to check **"Add Python to PATH"** during installation!

### 2️⃣ Install FFmpeg
FFmpeg is required for video processing. Follow these steps:

#### **🚀 AUTOMATIC INSTALLATION (Using Chocolatey)**
Chocolatey is a package manager for Windows that makes installing software easy.

1. **Install Chocolatey:**
   - Open **PowerShell** as Administrator and run:
     ```powershell
     Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
     ```
   - Close and reopen PowerShell after installation.

2. **Install FFmpeg using Chocolatey:**
   ```powershell
   choco install ffmpeg
   ```

3. **Verify installation:**
   ```powershell
   ffmpeg -version
   ```
   If FFmpeg is installed correctly, you'll see version details in the terminal.

#### **🔧 MANUAL INSTALLATION**

1. Download FFmpeg from [FFmpeg Official Site](https://ffmpeg.org/download.html).
2. Extract the downloaded file (e.g., to `C:\ffmpeg`).
3. Add the `bin` folder to your system PATH:
   - Open **Control Panel** > **System** > **Advanced system settings**.
   - Click **Environment Variables**.
   - Find `Path` under **System Variables** and click **Edit**.
   - Click **New** and add `C:\ffmpeg\bin`.
   - Click **OK** to save.
4. Verify installation:
   - Open **PowerShell**.
   - Execute this command:
     ```powershell
     ffmpeg -version
     ```
   If FFmpeg is installed correctly, you'll see version details in the terminal.

---

## ▶️ How to Use

### 1️⃣ Download the Application
1. Go to the **[Releases](https://github.com/davisoares454/video-compressor-for-discord/releases)** page of this repository.
2. Download the latest `.zip` file.
3. Extract the contents to a folder of your choice.

### 2️⃣ Run the Application
1. Open the extracted folder.
2. Double-click **`VideoCompressorForDiscord.exe`**.
3. The application interface will open.

### 3️⃣ Compress a Video
1. **Select an input video** – Choose the video you want to compress.
2. **Choose an output location** – Select where to save the new video.
3. **Start encoding** – Click **"Start Encoding"** and wait for the process to complete.

---

## 🏗️ How to Build an Executable (For Developers)
If you want to create a standalone version of the app:
```bash
pyinstaller --onedir --noupx --windowed app.py --name VideoCompressorForDiscord
```
This will create a folder `dist/VideoCompressorForDiscord`, containing everything needed to run the app.

---

## 🔧 Troubleshooting

- **FFmpeg Not Found?**
  Ensure it’s installed and added to PATH. Run `ffmpeg -version` to verify.

- **Antivirus Warnings?**
  If the built executable triggers warnings, disable UPX compression:
  ```bash
  pyinstaller --noupx --onedir --windowed app.py --name VideoCompressorForDiscord
  ```

---

## 📜 License
This project is licensed under the **MIT License**. See the `LICENSE` file for details.

## ❤️ Acknowledgments
Thanks to the contributors and the FFmpeg community for their incredible tools!
