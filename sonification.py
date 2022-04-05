import cv2

import numpy as np
import matplotlib.pyplot as plt
from astropy.visualization import SqrtStretch
from astropy.visualization.mpl_normalize import ImageNormalize

from astropy.convolution import Gaussian2DKernel
from photutils.background import Background2D, MedianBackground
from photutils.segmentation import detect_threshold, detect_sources, deblend_sources
from photutils.background import Background2D, MedianBackground
from astropy.stats import gaussian_fwhm_to_sigma
from photutils.segmentation import SourceCatalog

from PIL import Image

import tkinter as tk
from tkinter import filedialog
import operator

freq = []
amplitudes = []

def freq_mapping(N):

#  fl = 2**((0+1-49)/12)*440
#  fh = 2**((N+1-49)/12)*440
#  
#  for i in range(0,N):
#    a = 2**((i+1-49)/12)*440
#    freq.append(a)
  fl = 20
  fh = 20000

  for i in range(1, N+1):
    a = fl+(fh-fl)*(i-1)/(N-1)
    freq.append(a)
  
def amp_mapping():

  al = 1000
  ah = 5000
  N = 255

  for i in range(0,N):
    b = al+(ah-al)*(i-1)/(N-1)
    amplitudes.append(b)

root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilename()

image=cv2.imread(file_path)
im = Image.open(file_path)
cv2.imshow("Original",image)
cv2.waitKey(0)

data = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow("Data",data)
cv2.waitKey(0)

# threshold = detect_threshold(data, nsigma=2.)

bkg_estimator = MedianBackground()
bkg = Background2D(data, (50, 50), filter_size=(3, 3), bkg_estimator=bkg_estimator)
data = data - bkg.background  # subtract the background
threshold = 2. * bkg.background_rms  # above the background


sigma = 3.0 * gaussian_fwhm_to_sigma  # FWHM = 3.
kernel = Gaussian2DKernel(sigma, x_size=3, y_size=3)
kernel.normalize()
npixels = 5
segm = detect_sources(data, threshold, npixels=npixels, kernel=kernel)
segm_deblend = deblend_sources(data, segm, npixels=npixels,kernel=kernel, nlevels=32,contrast=0.001)

norm = ImageNormalize(stretch=SqrtStretch())
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12.5))
ax1.imshow(data, origin='lower', cmap='Greys_r', norm=norm)
ax1.set_title('Data')
cmap = segm.make_cmap(seed=123)
ax2.imshow(segm, origin='lower', cmap=cmap, interpolation='nearest')
ax2.set_title('Segmentation Image')

fig, ax = plt.subplots(1, 1, figsize=(10, 6.5))
cmap = segm_deblend.make_cmap(seed=123)
ax.imshow(segm_deblend, origin='lower', cmap=cmap, interpolation='nearest')
ax.set_title('Deblended Segmentation Image')
plt.tight_layout()
plt.show()

cat = SourceCatalog(data, segm_deblend)
tbl = cat.to_table()

tbl['xcentroid'].info.format = '.2f' 
tbl['ycentroid'].info.format = '.2f'
tbl['kron_flux'].info.format = '.2f'

tbl = sorted(tbl, key=operator.itemgetter(1))
#print(tbl['xcentroid'][0],"\n",tbl['ycentroid'])

px = im.load()
width, height = im.size

# coordinate = x, y = 401, 0
# print(im.getpixel(401, 0))

sources_count = len(tbl)
source_freqs = []
source_amplitudes = []

freq_mapping(height)
amp_mapping()
print(freq, amplitudes)

print("Sources     x-coordinate     y-coordinate      intensity                     frequency         amplitude\n")


for source in tbl:

    x, y = int(source[1]), int(source[2])
#    px_intensity = (image[y,x][0] + image[y,x][1] + image[y,x][2])//3
    px_intensity = (px[x,y][0] + px[x,y][1] + px[x,y][2])//3        
    print(source[0], "\t\t", x, "\t\t", y, "\t\t", image[y,x], px_intensity, "\t\t", freq[y], "\t\t", amplitudes[px_intensity])
    source_freqs.append(freq[y])
    source_amplitudes.append(amplitudes[px_intensity])

print(source_amplitudes)