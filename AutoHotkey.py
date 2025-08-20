import subprocess, os
os.system("")
class bcolors:
    OKBLUE = '\033[94m'
    WARNING = '\033[93m'
    LINE = '\033[90m'
    ENDC = '\033[0m'
link = input(f"{bcolors.WARNING}Link {bcolors.ENDC}> {bcolors.WARNING}")
print(f"{bcolors.LINE}---------------------------------------{bcolors.WARNING}")
print(f"{bcolors.OKBLUE}Now downloading...")
print(f"{bcolors.LINE}---------------------------------------{bcolors.ENDC}")
quality = "--remux mp4"
command = f"yt-dlp {quality} {link} --add-metadata --write-subs --embed-subs --cookies cookies.txt --embed-thumbnail -P downloads"
subprocess.run(command)
command = [
    "gallery-dl",
    "-d", "downloads (images)",
    "--cookies", "cookies.txt",
    "--write-metadata",
    "--ugoira", "mp4",
    link
]
subprocess.run(command)
os.startfile(os.getcwd())