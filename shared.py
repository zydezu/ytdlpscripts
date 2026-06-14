import os
import shutil
import subprocess
import sys

os.system("")


class bcolors:
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    LINE = "\033[90m"
    ENDC = "\033[0m"


OUTPUT_TEMPLATE = "downloads/%(playlist|)s/%(title)s.%(ext)s"
COOKIES_FILE = "cookies.txt"
DOWNLOADS_DIR = "downloads"


def prompt_link(media_type="video"):
    print(
        f"{bcolors.OKBLUE}Enter the link of the {bcolors.WARNING}{media_type}{bcolors.OKBLUE} you would like to download...{bcolors.ENDC}"
    )
    print(f"{bcolors.LINE}---------------------------------------")
    link = input(f"{bcolors.WARNING}Link {bcolors.ENDC}> {bcolors.WARNING}")
    print(f"{bcolors.LINE}---------------------------------------{bcolors.WARNING}")
    return link


def start_downloading():
    print(f"{bcolors.OKBLUE}Now downloading...")
    print(f"{bcolors.LINE}---------------------------------------{bcolors.ENDC}")


def run_ytdlp(quality, link, extra_args=""):
    command = f'yt-dlp {quality} "{link}" --cookies {COOKIES_FILE} -o "{OUTPUT_TEMPLATE}" {extra_args}'.strip()
    subprocess.run(command, shell=True)


def get_latest_mp4(directory=DOWNLOADS_DIR):
    mp4_files = []
    for root, _, files in os.walk(directory):
        for f in files:
            if f.endswith(".mp4"):
                mp4_files.append(os.path.join(root, f))
    if mp4_files:
        return max(mp4_files, key=os.path.getmtime)
    return None


def convert_to_gif(mp4_path):
    gif_path = mp4_path.rsplit(".", 1)[0] + ".gif"
    subprocess.run(f'ffmpeg -y -i "{mp4_path}" -vf palettegen palette.png', shell=True)
    subprocess.run(
        f'ffmpeg -i "{mp4_path}" -i palette.png -filter_complex "[0:v][1:v]paletteuse" "{gif_path}"',
        shell=True,
    )
    os.remove("palette.png")
    print(f"{bcolors.WARNING}GIF saved as {gif_path}{bcolors.ENDC}")


def convert_to_avif(mp4_path):
    avif_path = mp4_path.rsplit(".", 1)[0] + ".avif"
    subprocess.run(
        f'ffmpeg -y -i "{mp4_path}" -c:v libsvtav1 -crf 42 -preset 6 "{avif_path}"',
        shell=True,
    )
    print(f"{bcolors.WARNING}AVIF saved as {avif_path}{bcolors.ENDC}")


def copy_url_to_clipboard(url):
    try:
        if sys.platform.startswith("win"):
            subprocess.run(f"echo {url.strip()}| clip", shell=True, check=True)
        elif sys.platform.startswith("darwin"):
            subprocess.run("pbcopy", text=True, input=url.strip(), check=True)
        else:
            subprocess.run(
                "xclip -selection clipboard",
                shell=True,
                text=True,
                input=url.strip(),
                check=True,
            )
    except Exception as e:
        print("Failed to copy to clipboard:", e)


def open_file_in_explorer(file_path):
    if not file_path or not os.path.exists(file_path):
        return False
    try:
        if sys.platform.startswith("win"):
            if os.path.isdir(file_path):
                subprocess.run(f'explorer "{os.path.normpath(file_path)}"')
            else:
                subprocess.run(f'explorer /select,"{os.path.normpath(file_path)}"')
        elif sys.platform.startswith("darwin"):
            subprocess.run(["open", "-R", file_path])
        else:
            target = file_path if os.path.isdir(file_path) else os.path.dirname(file_path)
            subprocess.run(["xdg-open", target])
        return True
    except Exception as e:
        print("Failed to open file explorer:", e)
        return False


def copy_file_path_to_clipboard(file_path):
    if not file_path or not os.path.exists(file_path):
        return False
    try:
        abs_path = os.path.abspath(file_path)
        if sys.platform.startswith("win"):
            import win32clipboard as clip

            clip.OpenClipboard()
            clip.EmptyClipboard()
            files = abs_path + "\0"
            data = files.encode("utf-16le") + b"\0\0"
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
            if shutil.which("wl-copy"):
                subprocess.run(
                    ["wl-copy", "-t", "text/uri-list"], input=uri.encode(), check=True
                )
            elif shutil.which("xclip"):
                subprocess.run(
                    [
                        "xclip",
                        "-selection",
                        "clipboard",
                        "-t",
                        "x-special/gnome-copied-files",
                    ],
                    input=f"copy\n{uri}".encode(),
                    check=True,
                )
            else:
                raise RuntimeError("No clipboard utility found (wl-copy/xclip)")
        return True
    except Exception as e:
        print("Clipboard copy failed:", e)
        return False


def get_downloads_folder():
    return os.path.join(os.getcwd(), DOWNLOADS_DIR)


def get_image_downloads_folder():
    return os.path.join(os.getcwd(), "downloads (images)")


def get_all_files_in_directory(directory):
    all_files = []
    if os.path.exists(directory):
        for root, _, files in os.walk(directory):
            for file in files:
                all_files.append(os.path.join(root, file))
    return all_files


def find_new_files(initial_files, final_files):
    return list(set(final_files) - set(initial_files))


def filter_out_json_files(files):
    return [f for f in files if not f.lower().endswith(".json")]
