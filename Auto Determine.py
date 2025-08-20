import subprocess, os, sys, shutil
from pathlib import Path
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

def open_file_in_explorer(file_path):
    if not file_path or not os.path.exists(file_path):
        return False

    # if sys.platform.startswith("win"):
    #     subprocess.run(f'explorer /select,"{os.path.normpath(file_path)}"')
    # elif sys.platform.startswith("darwin"):
    #     subprocess.run(["open", "-R", file_path])
    # else:
    #     subprocess.run(["xdg-open", os.path.dirname(file_path)])

    try:
        if sys.platform.startswith("win"):
            powershell_cmd = f'Set-Clipboard -Path "{os.path.abspath(file_path)}"'
            subprocess.run(["powershell", "-Command", powershell_cmd], check=True)
        elif sys.platform.startswith("darwin"):
            subprocess.run(f'echo "{os.path.abspath(file_path)}" | pbcopy', shell=True)
        else:
            subprocess.run(f'echo "{os.path.abspath(file_path)}" | xclip -selection clipboard', shell=True)
    except Exception as e:
        print("Clipboard copy failed:", e)
        return False

    return True

def download_with_ytdlp(link):        
    downloads_dir = get_downloads_folder()
    quality = "--remux mp4"
    
    # Get files before download
    initial_files = get_all_files_in_directory(downloads_dir)
    
    # Run the download command
    command = f"yt-dlp {quality} {link} --add-metadata --write-subs --embed-subs --cookies cookies.txt --embed-thumbnail -P {downloads_dir}"
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
    command = [
        "gallery-dl",
        "-d", downloads_dir,
        "--cookies", "cookies.txt",
        "--write-metadata",
        "--ugoira", "mp4",
        link
    ]

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

    downloaded_files = download_with_gallery_dl(link)
    if not downloaded_files:
        downloaded_file = download_with_ytdlp(link)

    if downloaded_files:      
        non_json_files = filter_out_json_files(downloaded_files)
        open_file_in_explorer(non_json_files[0])  
    elif downloaded_file:
        open_file_in_explorer(downloaded_file)
    else:
        print(f"{bcolors.FAIL}Download failed or no file was downloaded.{bcolors.ENDC}")

    sys.exit()

if __name__ == "__main__":
    main()