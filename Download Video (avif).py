import subprocess, os
os.system("")

class bcolors:
    OKBLUE = '\033[94m'
    WARNING = '\033[93m'
    LINE = '\033[90m'
    ENDC = '\033[0m'
print(f"{bcolors.OKBLUE}Enter the link of the {bcolors.WARNING}video{bcolors.OKBLUE} you would like to download...{bcolors.ENDC}")
print(f"{bcolors.LINE}---------------------------------------")
link = input(f"{bcolors.WARNING}Link {bcolors.ENDC}> {bcolors.WARNING}")
print(f"{bcolors.LINE}---------------------------------------{bcolors.WARNING}")
print(f"{bcolors.OKBLUE}Now downloading...")
print(f"{bcolors.LINE}---------------------------------------{bcolors.ENDC}")
quality = "--remux mp4 "
output_path = "downloads/%(title)s.%(ext)s"
command = f"yt-dlp {quality} '{link}' --add-metadata --write-subs --embed-subs --embed-thumbnail -o \"{output_path}\""
subprocess.run(command, shell=True)

downloads_dir = "downloads"
video_file = None
mp4_files = [os.path.join(downloads_dir, f) for f in os.listdir(downloads_dir) if f.endswith(".mp4")]
if mp4_files:
    video_file = max(mp4_files, key=os.path.getmtime)

if video_file:
    avif_file = video_file.rsplit(".", 1)[0] + ".avif"
    subprocess.run(f"ffmpeg -y -i \"{video_file}\"  -c:v libsvtav1 -crf 42 -preset 6 \"{avif_file}\"", shell=True)
    print(f"{bcolors.WARNING}AVIF saved as {avif_file}{bcolors.ENDC}")
else:
    print(f"{bcolors.WARNING}No MP4 file found to convert.{bcolors.ENDC}")