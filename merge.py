import numpy as np
from PIL import Image

src1 = np.array(Image.open('xray1.jpeg'))
src2 = np.array(Image.open('optical.jpg').resize(src1.shape[1::-1], Image.BILINEAR))
src3 = np.array(Image.open('IR.jpg').resize(src1.shape[1::-1], Image.BILINEAR))
print(src1.dtype)
# uint8

dst = src1 * 0.5 + src2 * 0.5 + src3 * 0.2

print(dst.dtype)
# float64

Image.fromarray(dst.astype(np.uint8)).save('numpy_image_alpha_blend.jpg')