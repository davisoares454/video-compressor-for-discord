# Video Compressor For Discord

**VideoCompressorForDiscord** is a Windows application that compresses and transforms videos to match the max file size for Discord. It uses FFmpeg and FFprobe to perform two-pass encoding—trimming the video to the final 30 seconds and converting it using preset parameters (e.g., 2750k bitrate, 48fps, 1280x720 resolution). The GUI, built with Tkinter, allows you to select an input video, specify an output file, and displays a progress bar during encoding.

## Prerequisites

- **Operating System**: Windows  
- **Python**: Python 3.x (3.8+ is recommended)  
- **FFmpeg/FFprobe**: System-installed versions must be available in your `PATH`. Alternatively, update the helper functions in `app.py` to point to their locations if they are not in `PATH`.  
- **Tkinter**: Usually included with most Python distributions on Windows.  

## Installing FFmpeg

If you do not have FFmpeg and FFprobe installed, follow these steps:

1. Download the latest FFmpeg build from [FFmpeg's official site](https://ffmpeg.org/download.html).
2. Extract the downloaded file to a convenient location (e.g., `C:\ffmpeg`).
3. Add the `bin` directory to your system `PATH`:
   - Open **Control Panel** > **System** > **Advanced system settings**.
   - Click on **Environment Variables**.
   - Under **System Variables**, find `Path`, select it, and click **Edit**.
   - Click **New**, then enter the path to the FFmpeg `bin` directory (e.g., `C:\ffmpeg\bin`).
   - Click **OK** to save the changes.
4. Verify installation by running the following command in Command Prompt:
   ```bash
   ffmpeg -version
   ```

## Local Setup

### Clone or Download the Repository

Open a terminal, navigate to your desired folder, and run:

```bash
git clone https://github.com/davisoares454/video-compressor-for-discord.git
cd video-compressor-for-discord
```

### Create a Virtual Environment

```bash
python -m venv venv
```

### Activate the Virtual Environment

**On Windows:**

```cmd
venv\Scripts\activate
```

**On macOS/Linux:**

```bash
source venv/bin/activate
```

### Install Required Packages

Install TK and any other necessary packages using pip:

```bash
pip install tk
pip install pyinstaller
```

## Running the Application Locally

With your virtual environment activated, run:

```bash
python app.py
```

This will launch the **VideoCompressorForDiscord** GUI. From the interface, you can:

- **Select Input Video**: Choose the video you wish to compress.
- **Select Output File**: Specify the output file path.
- **Start Encoding**: Click the "Start Encoding" button to begin processing.

## Building the Application

To create a distributable version of your app without an accompanying console window, use the following PyInstaller command:

```bash
pyinstaller --onedir --windowed app.py --name VideoCompressorForDiscord
```

### Explanation:

- `--onedir`: Creates a folder containing the executable and all dependent files.
- `--windowed`: Prevents a console window from opening when the app runs.
- `--name VideoCompressorForDiscord`: Sets the name of the output folder/executable.

After running this command, you will find a folder named `VideoCompressorForDiscord` in the `dist` directory. This folder contains the executable along with the necessary files to run your application.

## Usage Tips & Troubleshooting

### FFmpeg/FFprobe Availability:
Ensure that both executables are installed on your system and available via the system `PATH`. If not, update the helper functions (`get_ffmpeg_executable()` and `get_ffprobe_executable()`) in `app.py` to point to their absolute paths.

### Suppressing Console Windows:
When calling FFmpeg/FFprobe via `subprocess.Popen`, the code sets the `creationflags` parameter to `subprocess.CREATE_NO_WINDOW` on Windows to prevent additional terminal windows from opening.

### Antivirus/Defender Alerts:
If the built executable triggers warnings, consider disabling UPX compression using the `--noupx` flag or signing your executable with a valid code signing certificate.

## License

This project is licensed under the **MIT License**. See the `LICENSE` file for details.

## Acknowledgments

Special thanks to the contributors and the FFmpeg community for the tools and libraries that made this project possible.