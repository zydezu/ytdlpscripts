import os
import subprocess
import sys

from shared import (
    bcolors,
    copy_file_path_to_clipboard,
    copy_url_to_clipboard,
    filter_out_json_files,
    find_new_files,
    get_all_files_in_directory,
    get_downloads_folder,
    get_image_downloads_folder,
    get_latest_mp4,
    open_file_in_explorer,
    start_downloading,
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


def main():
    print(
        f"{bcolors.OKBLUE}Enter the link of the {bcolors.WARNING}media{bcolors.OKBLUE} you would like to download...{bcolors.ENDC}"
    )
    print(f"{bcolors.LINE}---------------------------------------")
    link = input(f"{bcolors.WARNING}Link {bcolors.ENDC}> {bcolors.WARNING}")
    print(f"{bcolors.LINE}---------------------------------------{bcolors.WARNING}")
    print(f"{bcolors.OKBLUE}Now downloading...")
    print(f"{bcolors.LINE}---------------------------------------{bcolors.ENDC}")

    probably_a_video = False
    is_music = "music.youtube.com" in link
    if "youtube.com" in link or "youtu.be" in link:
        probably_a_video = True

    downloaded_files = []
    downloaded_file = None
    if is_music:
        downloaded_file = download_with_ytdlp(link, audio_only=True)
    elif not probably_a_video:
        downloaded_files = download_with_gallery_dl(link)
    if not downloaded_files and not is_music:
        downloaded_file = download_with_ytdlp(link)

    if downloaded_files:
        non_json_files = filter_out_json_files(downloaded_files)
        open_file_in_explorer_and_copy_to_clipboard(non_json_files[0])
    elif downloaded_file:
        open_file_in_explorer_and_copy_to_clipboard(downloaded_file)
    else:
        print(f"{bcolors.FAIL}Download failed or no file was downloaded.{bcolors.ENDC}")

    sys.exit()


if __name__ == "__main__":
    main()
