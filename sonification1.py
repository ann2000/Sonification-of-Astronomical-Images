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

import operator

import pandas as pd
from moviepy.editor import *

def freq_mapping(N):

#  fl = 2**((0+1-49)/12)*440
#  fh = 2**((N+1-49)/12)*440
#  
#  for i in range(0,N):
#    a = 2**((i+1-49)/12)*440
#    freq.append(a)
  global freq
  freq = []
  fl = 20
  fh = 20000

  for i in range(1, N+1):
    a = fl+(fh-fl)*(i-1)/(N-1)
    freq.append(a)
  
def amp_mapping():

  global amplitudes
  amplitudes = []
  al = 1000
  ah = 5000
  N = 255

  for i in range(0,N):
    b = al+(ah-al)*(i-1)/(N-1)
    amplitudes.append(b)

def get_freqandamp(file_path):

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

  #norm = ImageNormalize(stretch=SqrtStretch())
  #fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12.5))
  #ax1.imshow(data, origin='lower', cmap='Greys_r', norm=norm)
  #ax1.set_title('Data')
  #cmap = segm.make_cmap(seed=123)
  ##ax2.imshow(segm, origin='lower', cmap=cmap, interpolation='nearest')
  #ax2.set_title('Segmentation Image')
  #
  #fig, ax = plt.subplots(1, 1, figsize=(10, 6.5))
  #cmap = segm_deblend.make_cmap(seed=123)
  ##ax.imshow(segm_deblend, origin='lower', cmap=cmap, interpolation='nearest')
  #ax.set_title('Deblended Segmentation Image')
  #plt.tight_layout()
  #plt.show()

  cat = SourceCatalog(data, segm_deblend)
  tbl = cat.to_table()

  tbl['xcentroid'].info.format = '.2f' 
  tbl['ycentroid'].info.format = '.2f'
  tbl['kron_flux'].info.format = '.2f'

  tbl = pd.DataFrame(sorted(tbl, key=operator.itemgetter(1)))
  #print(tbl['xcentroid'][0],"\n",tbl['ycentroid'])
  tbl = tbl.astype({1: int, 2:int})

  px = im.load()
  width, height = im.size
  size = (width, height)
  # coordinate = x, y = 401, 0
  # print(im.getpixel(401, 0))

  sources_count = len(tbl)
  source_freqs = dict()
  source_amplitudes = dict()

  freq_mapping(height)
  amp_mapping()

  print("Sources     x-coordinate     y-coordinate      intensity                     frequency         amplitude\n")

  for source in tbl.index:

      x, y = int(tbl[1][source]), int(tbl[2][source])
  #    px_intensity = (image[y,x][0] + image[y,x][1] + image[y,x][2])//3
      px_intensity = (px[x,y][0] + px[x,y][1] + px[x,y][2])//3        
      print(tbl[0][source], "\t\t", x, "\t\t", y, "\t\t", image[y,x], px_intensity, "\t\t", freq[y], "\t\t", amplitudes[px_intensity])
      source_freqs.setdefault(x,[]).append(freq[y])
      source_amplitudes.setdefault(x,[]).append(amplitudes[px_intensity])

  print(source_freqs)
  song_freqs = []
  song_amplitudes = []

  for pos in range(width):

    if pos in source_freqs.keys():
        song_freqs.append(source_freqs[pos])
        song_amplitudes.append(source_amplitudes[pos])
    else:
        song_freqs.append([0])
        song_amplitudes.append([0])

  return song_freqs, song_amplitudes

#img_array = []


#create video
out_video = cv2.VideoWriter('video.avi',cv2.VideoWriter_fourcc(*'DIVX'), 4, size)

for i in range(width):

  img = image

  if i in source_freqs.keys():
    tbl_copy = tbl.loc[tbl[1]==i]
    print(tbl_copy)
    for y in tbl_copy[2]:
      img[y, i] = (255,255,255)
  
  out_video.write(img)

out_video.release()
clip = VideoFileClip("video.avi")
 