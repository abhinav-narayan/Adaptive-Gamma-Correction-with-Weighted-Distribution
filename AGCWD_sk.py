# -*- coding: utf-8 -*-
"""
 Adaptive gamma correction based on the reference.
 Reference:
   S. Huang, F. Cheng and Y. Chiu, "Efficient Contrast Enhancement Using Adaptive Gamma Correction With
   Weighting Distribution," in IEEE Transactions on Image Processing, vol. 22, no. 3, pp. 1032-1041,
   March 2013. doi: 10.1109/TIP.2012.2226047

"""
from skimage import io,color,exposure
import numpy as np

def RGB2HSV(img):
    i = color.rgb2hsv(img)
    i = i[:,:,2]
    i = i * 255
    i = np.uint8(i)
    return i

def get_pdf(img):
    pixelcounts,a = exposure.histogram(img)
    pdf = pixelcounts/np.size(img)
    return pdf

def SetValueChannel(color_image,value_channel):
    value_channel = np.double(value_channel)
    value_channel = value_channel/255
    color_image = color.rgb2hsv(color_image)
    color_image[:,:,2] = value_channel
    color_image = np.uint8(np.round(color.hsv2rgb(color_image) * 255))
    return color_image

def AGCWD(img):
    weighting_parameter = 0.5
    image = img
    image = RGB2HSV(image)
    pdf = get_pdf(image)
    Max = max(pdf)
    Min = min(pdf)
    pdf_w = Max * (((pdf-Min)/(Max - Min)) ** weighting_parameter)
    cdf_w = np.cumsum(pdf_w)/sum(pdf_w)
    l = np.arange(0,256)
    l_max = 255
    for i in l:
        l[i] = np.array([l_max * (l[i]/l_max) ** (1 - cdf_w[i])])
    l = np.uint8(l)
 
    enhanced_image = image
    h,w = image.shape
    for i in range(0,h):
        for j in range(0,w):
            intensity = enhanced_image[i][j]
            enhanced_image[i][j] = l[intensity]
    enhanced_image = SetValueChannel(img, enhanced_image)
    return enhanced_image

#Load the input image

inp_img = io.imread('C:/Users/Abhi/Downloads/10795.jpeg')
test = AGCWD(inp_img)
io.imsave('AGCWD_Output.png',test)
