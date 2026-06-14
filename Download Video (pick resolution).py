from shared import bcolors, prompt_link, start_downloading, run_ytdlp

link = prompt_link("video")
print(f"{bcolors.OKBLUE}Enter the max resolution of the {bcolors.WARNING}video{bcolors.OKBLUE} to download...{bcolors.ENDC}")
print(f"{bcolors.LINE}---------------------------------------")
res = input(f"{bcolors.WARNING}Resolution {bcolors.ENDC}> {bcolors.WARNING}")
start_downloading()
quality = f'-f "bestvideo[height<={res}][format_note!*=AI-upscaled]+bestaudio/best[ext=mp4]/best" --remux mp4'
run_ytdlp(quality, link, "--add-metadata --write-subs --embed-subs --embed-thumbnail")
