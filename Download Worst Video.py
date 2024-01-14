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
quality = f" -f bestvideo[height<=144][vcodec^=avc][ext=mp4]+worstaudio --remux mp4 "
command = "yt-dlp" + quality + link + " --add-metadata --write-subs --embed-subs -P Downloads "
subprocess.run(command)