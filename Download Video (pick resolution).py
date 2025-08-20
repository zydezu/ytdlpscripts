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
print(f"{bcolors.OKBLUE}Enter the max resolution of the {bcolors.WARNING}video{bcolors.OKBLUE} to download...{bcolors.ENDC}")
print(f"{bcolors.LINE}---------------------------------------")
res = input(f"{bcolors.WARNING}Resolution {bcolors.ENDC}> {bcolors.WARNING}")
print(f"{bcolors.LINE}---------------------------------------{bcolors.WARNING}")
print(f"{bcolors.OKBLUE}Now downloading...")
print(f"{bcolors.LINE}---------------------------------------{bcolors.ENDC}")
quality = f"-f bestvideo[height<={res}][vcodec^=avc][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best --remux mp4"
command = f"yt-dlp {quality} {link} --add-metadata --write-subs --embed-subs --embed-thumbnail -P downloads"
subprocess.run(command)