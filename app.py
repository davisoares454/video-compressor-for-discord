import tkinter as tk
import webbrowser
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import subprocess
import threading
import sys
import os

def resource_path(relative_path):
    """ Get absolute path to resource (for PyInstaller). """
    if hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")

    # DEBUG: List files in the extracted folder
    print("\n🔍 Debugging File Paths:")
    print("Looking for files in:", base_path)
    try:
        print("Files in directory:", os.listdir(base_path))
    except Exception as e:
        print("Error listing directory:", e)

    # Return the absolute path to the file
    return os.path.join(base_path, relative_path)

def cleanup_default_pass_logs():
    # Default filenames FFmpeg uses when -passlogfile is not specified.
    log_files = ["ffmpeg2pass-0.log", "ffmpeg2pass-0.log.mbtree"]
    for filename in log_files:
        if os.path.exists(filename):
            try:
                os.remove(filename)
                print(f"Deleted {filename}")
            except Exception as e:
                print(f"Error deleting {filename}: {e}")

def get_ffmpeg_executable():
    # if getattr(sys, 'frozen', False):
    #     # In frozen mode, get the folder where the exe is located.
    #     exe_dir = os.path.dirname(sys.executable)
    #     # Assume the executables are in the _internal folder next to the exe.
    #     return os.path.join(exe_dir, "_internal", "ffmpeg.exe")
    # else:
    #     # Running from source: use the local "bin" folder.
    return "ffmpeg"

def get_ffprobe_executable():
    # if getattr(sys, 'frozen', False):
    #     exe_dir = os.path.dirname(sys.executable)
    #     return os.path.join(exe_dir, "_internal", "ffprobe.exe")
    # else:
    return "ffprobe"


def time_str_to_seconds(time_str):
    """Convert HH:MM:SS.microseconds string to seconds (float)."""
    try:
        parts = time_str.strip().split(':')
        if len(parts) == 3:
            hours = float(parts[0])
            minutes = float(parts[1])
            seconds = float(parts[2])
            return hours * 3600 + minutes * 60 + seconds
    except Exception as e:
        print("Error converting time string:", e)
    return 0.0

def get_video_duration(file_path):
    """Use ffprobe to get the input video duration in seconds."""
    ffprobe_exe = get_ffprobe_executable()
    try:
        cmd = [
            ffprobe_exe, "-v", "error", "-select_streams", "v:0",
            "-show_entries", "format=duration", "-of",
            "default=noprint_wrappers=1:nokey=1", file_path
        ]
        creationflags = subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
        result = subprocess.run(
            cmd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            text=True,
            creationflags=creationflags
        )
        duration = float(result.stdout.strip())
        return duration
    except Exception as e:
        messagebox.showerror("Error", f"Could not get video duration: {e}")
        print(e)
        return 0.0

def run_ffmpeg(pass_num, input_file, output_file, target_duration, trim_start, update_progress):
    """
    Run one pass of FFmpeg encoding with progress output.
    pass_num: 1 or 2.
    target_duration: duration of the trimmed segment.
    trim_start: start time (in seconds) for trimming.
    update_progress: callback for overall progress (0-100).
    """
    ffmpeg_exe = get_ffmpeg_executable()
    base_cmd = [
        ffmpeg_exe, "-y",
        "-ss", str(trim_start),
        "-t", str(target_duration),
        "-i", input_file,
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-profile:v", "main",
        "-level", "4.0",
        "-b:v", "2600k",
        "-r", "48",
        "-vf", "scale=1280:720",
        "-movflags", "+faststart",
        "-progress", "pipe:1"
    ]
    
    if pass_num == 1:
        # First pass: no audio, output to NUL (Windows)
        cmd = base_cmd + [
            "-pass", "1",
            "-an", "-f", "mp4", "NUL"
        ]
    else:
        # Second pass: include audio and write final output
        cmd = base_cmd + [
            "-pass", "2",
            "-c:a", "aac",
            "-b:a", "64k",
            "-ac", "2",
            "-map_metadata", "0",
            output_file
        ]
    # On Windows, pass the flag to suppress a console window.
    creationflags = subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
        
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        bufsize=1,
        creationflags=creationflags
    )
    
    for line in process.stdout:
        line = line.strip()
        if line.startswith("out_time="):
            time_str = line.split("=", 1)[1]
            current = time_str_to_seconds(time_str)
            if target_duration > 0:
                current_pass_progress = min(current / target_duration, 1.0)
                if pass_num == 1:
                    overall = current_pass_progress * 50
                else:
                    overall = 50 + current_pass_progress * 50
                update_progress(overall)
        elif line.startswith("progress="):
            if "end" in line:
                if pass_num == 1:
                    update_progress(50)
                else:
                    update_progress(100)
    process.wait()

def encode_video(input_file, output_file, progress_callback):
    """Perform two-pass encoding, trimming to the final one minute of the video."""
    full_duration = get_video_duration(input_file)
    # Determine target duration (max 60 seconds) and start time (last minute)
    target_duration = min(30, full_duration)
    trim_start = max(full_duration - 30, 0)
    
    run_ffmpeg(1, input_file, output_file, target_duration, trim_start, progress_callback)
    run_ffmpeg(2, input_file, output_file, target_duration, trim_start, progress_callback)


class VideoCompressorForDiscordApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Compressor for Discord")
        self.root.geometry("330x250")
        self.root.resizable(False, False)

        # Load the icon using the correct path
        icon_path = resource_path("icon.png")  # Use helper function
        print(f"\n🔎 Checking icon path: {icon_path}")
        if not os.path.exists(icon_path):
            print("❌ ERROR: icon.png not found in the bundle!")
            messagebox.showerror("Error", f"Missing icon.png at {icon_path}\nEnsure it's included with --add-data.")

        self.icon = tk.PhotoImage(file=icon_path)
        self.root.iconphoto(False, self.icon)

        self.input_file = ""
        self.output_file = ""
        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self.root, padding=10)
        frame.pack(expand=True, fill="both")

        # Title
        title_label = ttk.Label(frame, text="Video Compressor for Discord", font=("Arial", 14, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(5, 2))

        # Description
        description_label = ttk.Label(frame, text="Easily compress videos to share on Discord", font=("Arial", 10))
        description_label.grid(row=1, column=0, columnspan=2, pady=(0, 10))

        # Input selection
        self.input_button = ttk.Button(frame, text="Select Input", command=self.select_input, width=15)
        self.input_button.grid(row=2, column=0, padx=5, pady=5, sticky="w")

        self.input_label = ttk.Label(frame, text="No file selected", anchor="w", width=30)
        self.input_label.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        # Output selection
        self.output_button = ttk.Button(frame, text="Select Output", command=self.select_output, width=15)
        self.output_button.grid(row=3, column=0, padx=5, pady=5, sticky="w")

        self.output_label = ttk.Label(frame, text="No file selected", anchor="w", width=30)
        self.output_label.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(frame, variable=self.progress_var, maximum=100)
        self.progress_bar.grid(row=4, column=0, columnspan=2, padx=5, pady=10, sticky="ew")

        # Start encoding button
        self.start_button = ttk.Button(frame, text="Start Encoding", command=self.start_encoding, width=20)
        self.start_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        # About hyperlink-style text
        self.about_label = tk.Label(frame, text="About", fg="blue", cursor="hand2", font=("Arial", 10, "underline"))
        self.about_label.grid(row=6, column=0, columnspan=2, pady=10, sticky="s")
        self.about_label.bind("<Button-1>", lambda e: self.open_about_window())

    def select_input(self):
        file_path = filedialog.askopenfilename(title="Select Video File", filetypes=[("Video Files", "*.mp4 *.mkv *.avi *.mov"), ("All Files", "*.*")])
        if file_path:
            self.input_file = file_path
            self.input_label.config(text=os.path.basename(file_path))

    def select_output(self):
        file_path = filedialog.asksaveasfilename(title="Select Output File", defaultextension=".mp4", filetypes=[("MP4 Files", "*.mp4"), ("All Files", "*.*")])
        if file_path:
            self.output_file = file_path
            self.output_label.config(text=os.path.basename(file_path))

    def update_progress(self, value):
        self.root.after(0, self.progress_var.set, value)

    def start_encoding(self):
        if not self.input_file or not self.output_file:
            messagebox.showwarning("Missing File", "Please select both input and output files.")
            return
        self.start_button.config(state="disabled")
        self.input_button.config(state="disabled")
        self.output_button.config(state="disabled")
        threading.Thread(target=self.run_encoding_thread, daemon=True).start()

    def run_encoding_thread(self):
        try:
            encode_video(self.input_file, self.output_file, self.update_progress)
            messagebox.showinfo("Finished", "Video encoding completed!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            cleanup_default_pass_logs()
            self.root.after(0, lambda: self.start_button.config(state="normal"))
            self.root.after(0, lambda: self.input_button.config(state="normal"))
            self.root.after(0, lambda: self.output_button.config(state="normal"))

    def open_about_window(self):
        """Opens the About window with an image and GitHub link."""
        about_win = tk.Toplevel(self.root)
        about_win.title("About")
        about_win.geometry("220x210")
        about_win.resizable(False, False)

        icon_path = resource_path("icon.png")  # Get the icon path
        print(f"\n🔎 Checking About window image path: {icon_path}")
        if not os.path.exists(icon_path):
            print("❌ ERROR: icon.png not found!")
            messagebox.showerror("Error", f"Missing icon.png at {icon_path}")

        # Load and resize image
        try:
            original_image = Image.open(icon_path)  
            resized_image = original_image.resize((140, 140), Image.LANCZOS)  
            img = ImageTk.PhotoImage(resized_image)
        except Exception as e:
            messagebox.showerror("Error", f"Could not load image: {e}")
            print(f"❌ Image loading error: {e}")
            return

        # Display image
        img_label = ttk.Label(about_win, image=img)
        img_label.image = img  
        img_label.pack(pady=5)

        # Repository text
        text_label_first = ttk.Label(about_win, text="Original repository:", font=("Arial", 10, "bold"))
        text_label_first.pack()

        # GitHub hyperlink-style label
        repo_link = "https://github.com/davisoares454/video-compressor-for-discord"
        github_label = tk.Label(about_win, text="video-compressor-for-discord", fg="blue", cursor="hand2", font=("Arial", 10, "underline"))
        github_label.pack()
        github_label.bind("<Button-1>", lambda e: webbrowser.open_new(repo_link))  

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoCompressorForDiscordApp(root)
    root.mainloop()