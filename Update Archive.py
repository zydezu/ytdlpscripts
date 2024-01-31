import subprocess, os
import re
from os import walk
from os import path
os.system("")
class bcolors:
    OKBLUE = '\033[94m'
    WARNING = '\033[93m'
    LINE = '\033[90m'
    ENDC = '\033[0m'

quality = """ -f bestvideo[vcodec^=avc][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best --remux mp4 """

print(f"{bcolors.WARNING}Getting currently downloaded videos...{bcolors.ENDC}")

filenames = next(walk(os.path.join(os.getcwd(), "Downloads", "Archive")), (None, None, []))[2]  # [] if no file
filenames = [filename.replace('.info.json', '').replace('.mp4', '') for filename in filenames]

pattern = re.compile(r'\[([^\]]+)\]')
videoIDs = {(filename, match.group(1)) for filename in filenames for match in pattern.finditer(filename)}

print(f"{bcolors.LINE}---------------------------------------{bcolors.WARNING}")
print(f"{bcolors.OKBLUE}Updating...")
for video in videoIDs:
    print(f"{bcolors.LINE}---------------------------------------{bcolors.WARNING}")
    print(f"{bcolors.WARNING}Checking: {bcolors.OKBLUE}{video[0]}{bcolors.ENDC}")
    command = "yt-dlp" + quality + video[1] + " --skip-download --add-metadata --embed-subs --write-subs --write-comments -P Downloads/Archive"
    subprocess.run(command)
print(f"{bcolors.LINE}---------------------------------------{bcolors.WARNING}")
print(f"{bcolors.OKBLUE}Done!")