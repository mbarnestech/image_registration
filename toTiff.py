from PIL import Image
import os
import sys
import re

path = sys.argv[1]
tiff_path = sys.argv[2]
directory = os.fsencode(path)
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    name_root = re.match(filename, r'[\w]+_[\d]+')
    im = Image.open(filename)
    im.save(f'{tiff_path}/{name_root}.tiff', 'TIFF')