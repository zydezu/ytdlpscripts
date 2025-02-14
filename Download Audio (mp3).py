import subprocess, os
os.system("")
class bcolors:
    OKBLUE = '\033[94m'
    WARNING = '\033[93m'
    LINE = '\033[90m'
    ENDC = '\033[0m'
print(f"{bcolors.OKBLUE}Enter the link of the {bcolors.WARNING}audio (can be a video link){bcolors.OKBLUE} you would like to download...{bcolors.ENDC}")
print(f"{bcolors.LINE}---------------------------------------")
link = input(f"{bcolors.WARNING}Link {bcolors.ENDC}> {bcolors.WARNING}")
print(f"{bcolors.LINE}---------------------------------------{bcolors.WARNING}")
print(f"{bcolors.OKBLUE}Now downloading...")
print(f"{bcolors.LINE}---------------------------------------{bcolors.ENDC}")
quality = "-x --audio-format mp3"
command = f"yt-dlp {quality} {link} --embed-thumbnail -P Downloads"
subprocess.run(command)