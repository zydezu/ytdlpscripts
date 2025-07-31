import os, random, subprocess
from os import startfile
folder = "downloads\\"
random = random.choice(os.listdir(folder))
file = folder+random
startfile(file)