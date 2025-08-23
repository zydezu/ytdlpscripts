import subprocess, os
os.system("")
class bcolors:
    OKBLUE = '\033[94m'
    WARNING = '\033[93m'
    LINE = '\033[90m'
    ENDC = '\033[0m'
print(f"{bcolors.OKBLUE}Enter the link of the {bcolors.WARNING}image{bcolors.OKBLUE} you would like to download...{bcolors.ENDC}")
print(f"{bcolors.LINE}---------------------------------------")
link = input(f"{bcolors.WARNING}Link {bcolors.ENDC}> {bcolors.WARNING}")
print(f"{bcolors.LINE}---------------------------------------{bcolors.WARNING}")
print(f"{bcolors.OKBLUE}Now downloading...{bcolors.ENDC}")
print(f"{bcolors.LINE}---------------------------------------{bcolors.ENDC}")
command = [
    "gallery-dl",
    "-d", "downloads (images)",
    "--cookies", "cookies.txt",
    "--ugoira", "mp4",
    link
]
subprocess.run(command)