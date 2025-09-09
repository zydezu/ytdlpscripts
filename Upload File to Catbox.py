import os, sys, time, re, subprocess
import pyperclip
import tkinter as tk
from tkinter import filedialog
# from catboxuploader import CatboxUploader
os.system("")
class bcolors:
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    LINE = '\033[90m'
    ENDC = '\033[0m'

def copy_url_to_clipboard(url):
    try:
        if sys.platform.startswith("win"):
            pyperclip.copy(url)
        elif sys.platform.startswith("darwin"):
            subprocess.run("pbcopy", text=True, input=url.strip(), check=True)
        else:  # Linux (requires xclip or xsel installed)
            subprocess.run("xclip -selection clipboard", shell=True, text=True, input=url.strip(), check=True)
    except Exception as e:
        print("Failed to copy to clipboard:", e)

def uniquify_filename(filename: str) -> str:
    name, ext = os.path.splitext(filename)
    timestamp = int(time.time())
    return f"{name}_{timestamp}{ext}"

def sanitize_filename(filename: str) -> str:
    filename = filename.replace(" ", "").replace("-", "_")
    filename = re.sub(r"[\[\]{}()<>:\"'`^&*?=+$,;|]", "", filename)
    return filename

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select the file to upload"
    )
    if not file_path:
        print("No file selected.")
        exit(1)
    # uploader = CatboxUploader(file_path)
    # url = uploader.execute()
    # copy_url_to_clipboard(url)

    filename = uniquify_filename(sanitize_filename(os.path.basename(file_path)))
    url = f"https://files.zydezu.com/uploads/{filename}"

    # Run curl command
    try:
        subprocess.run(
            ["curl", "--globoff", "-T", file_path, url],
            check=True
        )
        copy_url_to_clipboard(url)
        print(f"{bcolors.OKGREEN}Upload to files.zydezu.com: {bcolors.WARNING}{url}{bcolors.ENDC}")
    except subprocess.CalledProcessError as e:
        print(f"Upload failed: {e}")

    # print(f"{bcolors.OKGREEN}Uploaded to Catbox: {bcolors.WARNING}{url}{bcolors.ENDC}")
