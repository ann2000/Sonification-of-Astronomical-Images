# alpha blending for merging different image components (ir, optical, x-ray)

import numpy as np
from PIL import Image

def merge_images(file_path):

    dst = 0

    for i in range (len(file_path)):

        if i == 0:
            src = np.array(Image.open(file_path[i]))
        else:          
            src = np.array(Image.open(file_path[i]).resize(src.shape[1::-1], Image.BILINEAR))

        dst += src * (1/len(file_path))
    
    Image.fromarray(dst.astype(np.uint8)).save('blended_image.jpg')