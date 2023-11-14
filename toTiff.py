from PIL import Image
import os
import sys

path = sys.argv[1]
tiff_path = sys.argv[2]
directory = os.fsencode(path)
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    name_root = filename.split('.')[0]
    print(name_root, type(name_root))
    im = Image.open(f'{path}{filename}')
    im.save(f'{tiff_path}/{name_root}.tiff', 'TIFF')