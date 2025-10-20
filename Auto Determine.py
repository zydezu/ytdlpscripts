import subprocess, os, sys
import win32clipboard as clip
from pathlib import Path
uploadfile = __import__("Upload File")
os.system("")
class bcolors:
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    LINE = '\033[90m'
    ENDC = '\033[0m'

def get_downloads_folder():
    return os.path.join(os.getcwd(), "downloads")

def get_image_downloads_folder():
    return os.path.join(os.getcwd(), "downloads (images)")

def get_all_files_in_directory(directory):
    all_files = []
    if os.path.exists(directory):
        for root, dirs, files in os.walk(directory):
            for file in files:
                all_files.append(os.path.join(root, file))
    return all_files

def find_new_files(initial_files, final_files):
    return list(set(final_files) - set(initial_files))

def filter_out_json_files(files):
    return [f for f in files if not f.lower().endswith('.json')]

def open_file_in_explorer_and_copy_to_clipboard(file_path):
    if not file_path or not os.path.exists(file_path):
        return False

    try:
        if sys.platform.startswith("win"):
            subprocess.run(f'explorer /select,"{os.path.normpath(file_path)}"')
        elif sys.platform.startswith("darwin"):
            subprocess.run(["open", "-R", file_path])
        else:
            subprocess.run(["xdg-open", os.path.dirname(file_path)])
    except Exception as e:
        print("Failed to open file explorer:", e)
        return False

    try:
        abs_path = os.path.abspath(file_path)

        if sys.platform.startswith("win"):
            clip.OpenClipboard()
            clip.EmptyClipboard()

            # CF_HDROP = list of files as UTF-16 with double null terminator
            files = abs_path + '\0'
            data = files.encode('utf-16le') + b'\0\0'
            clip.SetClipboardData(clip.RegisterClipboardFormat("FileNameW"), data)

            clip.CloseClipboard()

        elif sys.platform.startswith("darwin"):
            applescript = f'''
            set theFile to POSIX file "{abs_path}" as alias
            tell application "Finder"
                set the clipboard to (theFile as alias)
            end tell
            '''
            subprocess.run(["osascript", "-e", applescript])

        else:
            uri = f"file://{abs_path}"
            process = subprocess.Popen(
                ['xclip', '-selection', 'clipboard', '-t', 'x-special/gnome-copied-files'],
                stdin=subprocess.PIPE
            )
            process.communicate(input=f"copy\n{uri}".encode())

    except Exception as e:
        print("Clipboard copy failed:", e)
        return False

    return True

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

def download_with_ytdlp(link):        
    downloads_dir = get_downloads_folder()

    quality = "--remux mp4"
    
    # Get files before download
    initial_files = get_all_files_in_directory(downloads_dir)
    
    # Run the download command
    command = f'yt-dlp {quality} "{link}" --add-metadata --write-subs --embed-subs --cookies cookies.txt --embed-thumbnail -P {downloads_dir}'
    result = subprocess.run(command, shell=True)
    
    if result.returncode != 0:
        return None
    
    # Get files after download and find new ones
    final_files = get_all_files_in_directory(downloads_dir)
    new_files = find_new_files(initial_files, final_files)
    
    if new_files:
        # Return the largest file (likely the main download)
        return max(new_files, key=lambda x: os.path.getsize(x))
    
    return None

def download_with_gallery_dl(link):    
    downloads_dir = get_image_downloads_folder()

    # Get files before download
    initial_files = get_all_files_in_directory(downloads_dir)

    # Run the download command
    command = f'gallery-dl -d "{downloads_dir}" --cookies "cookies.txt" --ugoira mp4 "{link}"'

    result = subprocess.run(command, shell=True)

    if result.returncode != 0:
        return None

    # Get files after download and find new ones
    final_files = get_all_files_in_directory(downloads_dir)
    new_files = find_new_files(initial_files, final_files)

    return new_files if new_files else None

def main():
    print(f"{bcolors.OKBLUE}Enter the link of the {bcolors.WARNING}media{bcolors.OKBLUE} you would like to download...{bcolors.ENDC}")
    print(f"{bcolors.LINE}---------------------------------------")
    link = input(f"{bcolors.WARNING}Link {bcolors.ENDC}> {bcolors.WARNING}")
    print(f"{bcolors.LINE}---------------------------------------{bcolors.WARNING}")
    print(f"{bcolors.OKBLUE}Now downloading...")
    print(f"{bcolors.LINE}---------------------------------------{bcolors.ENDC}")

    probably_a_video = False
    if ("youtube.com" or "youtu.be") in link:
        probably_a_video = True

    downloaded_files = []
    if not probably_a_video:
        downloaded_files = download_with_gallery_dl(link)
    if not downloaded_files:
        downloaded_file = download_with_ytdlp(link)

    if downloaded_files:      
        non_json_files = filter_out_json_files(downloaded_files)
        open_file_in_explorer_and_copy_to_clipboard(non_json_files[0])  
    elif downloaded_file:
        open_file_in_explorer_and_copy_to_clipboard(downloaded_file)
        # uploadfile.upload(downloaded_file)
    else:
        print(f"{bcolors.FAIL}Download failed or no file was downloaded.{bcolors.ENDC}")

    sys.exit()

if __name__ == "__main__":
    main()