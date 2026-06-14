import os
import re
import subprocess
import sys

from shared import (
    bcolors,
    copy_file_path_to_clipboard,
    filter_out_json_files,
    find_new_files,
    get_all_files_in_directory,
    get_downloads_folder,
    get_image_downloads_folder,
    open_file_in_explorer,
)


def open_file_in_explorer_and_copy_to_clipboard(file_path):
    if not open_file_in_explorer(file_path):
        return False
    return copy_file_path_to_clipboard(file_path)


def download_with_ytdlp(link, audio_only=False):
    downloads_dir = get_downloads_folder()

    if audio_only:
        quality = "-x --embed-thumbnail"
        extra = ""
    else:
        quality = "--remux mp4"
        extra = "--add-metadata --write-subs --embed-subs --embed-thumbnail"

    initial_files = get_all_files_in_directory(downloads_dir)

    output_template = os.path.join(downloads_dir, "%(playlist|)s", "%(title)s.%(ext)s")
    command = f'yt-dlp {quality} "{link}" {extra} --cookies cookies.txt -o "{output_template}"'
    result = subprocess.run(command, shell=True)

    if result.returncode != 0:
        return None

    final_files = get_all_files_in_directory(downloads_dir)
    new_files = find_new_files(initial_files, final_files)

    if new_files:
        return max(new_files, key=lambda x: os.path.getsize(x))

    return None


def download_with_gallery_dl(link):
    downloads_dir = get_image_downloads_folder()

    initial_files = get_all_files_in_directory(downloads_dir)

    command = (
        f'gallery-dl -d "{downloads_dir}" --cookies "cookies.txt" --ugoira mp4 "{link}"'
    )

    result = subprocess.run(command, shell=True)

    if result.returncode != 0:
        return None

    final_files = get_all_files_in_directory(downloads_dir)
    new_files = find_new_files(initial_files, final_files)

    return new_files if new_files else None


def download_with_khinsider(link):
    from khinsider import (
        NonexistentFormatsError,
        NonexistentSoundtrackError,
        Soundtrack,
        to_valid_filename,
    )

    m = re.match(
        r"^https?://downloads\.khinsider\.com/game-soundtracks/album/(?P<id>[^/]+)/?$",
        link,
        re.IGNORECASE,
    )
    soundtrack_id = m.group("id") if m else link
    downloads_dir = get_downloads_folder()

    try:
        soundtrack = Soundtrack(soundtrack_id)
        path = os.path.join(downloads_dir, to_valid_filename(soundtrack.name))
        soundtrack.download(path, formatOrder=["flac", "mp3"], verbose=True)
        return path
    except (NonexistentSoundtrackError, NonexistentFormatsError) as e:
        print(f"{bcolors.FAIL}{e}{bcolors.ENDC}")
        return None


def main():
    print(
        f"{bcolors.OKBLUE}Enter the link of the {bcolors.WARNING}media{bcolors.OKBLUE} you would like to download...{bcolors.ENDC}"
    )
    print(f"{bcolors.LINE}---------------------------------------")
    link = input(f"{bcolors.WARNING}Link {bcolors.ENDC}> {bcolors.WARNING}")
    print(f"{bcolors.LINE}---------------------------------------{bcolors.WARNING}")
    print(f"{bcolors.OKBLUE}Now downloading...")
    print(f"{bcolors.LINE}---------------------------------------{bcolors.ENDC}")

    is_khinsider = "khinsider.com" in link
    is_music = "music.youtube.com" in link
    probably_a_video = "youtube.com" in link or "youtu.be" in link

    if is_khinsider:
        path = download_with_khinsider(link)
        if path:
            open_file_in_explorer(path)
        else:
            print(f"{bcolors.FAIL}Download failed or no file was downloaded.{bcolors.ENDC}")
    elif is_music:
        downloaded_file = download_with_ytdlp(link, audio_only=True)
        if downloaded_file:
            open_file_in_explorer_and_copy_to_clipboard(downloaded_file)
        else:
            print(f"{bcolors.FAIL}Download failed or no file was downloaded.{bcolors.ENDC}")
    elif not probably_a_video:
        downloaded_files = download_with_gallery_dl(link)
        if downloaded_files:
            non_json_files = filter_out_json_files(downloaded_files)
            open_file_in_explorer_and_copy_to_clipboard(non_json_files[0])
        else:
            downloaded_file = download_with_ytdlp(link)
            if downloaded_file:
                open_file_in_explorer_and_copy_to_clipboard(downloaded_file)
            else:
                print(f"{bcolors.FAIL}Download failed or no file was downloaded.{bcolors.ENDC}")
    else:
        downloaded_file = download_with_ytdlp(link)
        if downloaded_file:
            open_file_in_explorer_and_copy_to_clipboard(downloaded_file)
        else:
            print(f"{bcolors.FAIL}Download failed or no file was downloaded.{bcolors.ENDC}")

    sys.exit()


if __name__ == "__main__":
    main()
