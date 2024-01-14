import os, random, subprocess
from os import startfile
folder = "Downloads\\"
random = random.choice(os.listdir(folder))
file = folder+random
startfile(file)