import os, sys, subprocess
import tkinter as tk
from tkinter import filedialog
from catboxuploader import CatboxUploader
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
            subprocess.run(f'echo {url.strip()}| clip', shell=True, check=True)
        elif sys.platform.startswith("darwin"):
            subprocess.run("pbcopy", text=True, input=url.strip(), check=True)
        else:  # Linux (requires xclip or xsel installed)
            subprocess.run("xclip -selection clipboard", shell=True, text=True, input=url.strip(), check=True)
    except Exception as e:
        print("Failed to copy to clipboard:", e)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select the file to upload"
    )
    uploader = CatboxUploader(file_path)
    url = uploader.execute()
    copy_url_to_clipboard(url)
    print(f"{bcolors.OKGREEN}Uploaded to Catbox: {bcolors.WARNING}{url}{bcolors.ENDC}")
