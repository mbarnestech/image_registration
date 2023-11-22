import os
import sys
import numpy as np
from matplotlib import pyplot as plt
from skimage import transform, io, exposure
from PIL import Image
import glob
import tifffile

from pystackreg import StackReg
import pystackreg

if __name__ == "__main__":
    path = sys.argv[1]
    if path[-1] != "/":
        path = path + "/"
    if len(sys.argv) > 2:
        tiff_path = sys.argv[2]
        if tiff_path[-1] != "/":
            tiff_path = tiff_path + "/"
    else: 
        tiff_path = path[:-1] + "_tiff/"
        os.mkdir(tiff_path)
    

def convert_images(path = path, tiff_path = tiff_path):
    """Convert images from .jpg or .jpeg to .tiff in new directory"""
    
    directory = os.fsencode(path)

    for file in os.listdir(directory)[:10]:
        filename = os.fsdecode(file)
        name_root = filename.split('.')[0]
        im = Image.open(f'{path}{filename}')
        im.save(f'{tiff_path}{name_root}.tiff', 'TIFF')
        print(name_root)
    
def create_stack(tiff_path = tiff_path):
    with tifffile.TiffWriter('Stack.tiff') as stack:
        for filename in glob.glob(f'{tiff_path}*.tiff'):
            stack.write(
                tifffile.imread(filename), 
                # photometric='minisblack', 
                contiguous=True
            )


def overlay_images(imgs, equalize=False, aggregator=np.mean):
    
    if equalize:
        imgs = [exposure.equalize_hist(img) for img in imgs]
    
    imgs = np.stack(imgs, axis=0)
    
    return aggregator(imgs, axis=0)

def composite_images(imgs, equalize=False, aggregator=np.mean):
    
    if equalize:
        imgs = [exposure.equalize_hist(img) for img in imgs]
    
    imgs = [img / img.max() for img in imgs]
    
    if len(imgs) < 3:
        imgs += [np.zeros(shape=imgs[0].shape)] * (3-len(imgs))
  
    imgs = np.dstack(imgs)
    
    return imgs