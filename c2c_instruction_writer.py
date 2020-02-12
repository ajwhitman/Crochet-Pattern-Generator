# -*- coding: utf-8 -*-
"""
Created on Fri Nov  2 22:40:02 2018

@author: aj
"""

import os
from PIL import Image
import numpy as np

def compress(a, eDict=None):
    prev_e=None
    n=1
    #compList = []
    compStr = ''
    for e in a:
        if prev_e == None: 
            prev_e = e
            continue
        if e == prev_e:
            n+=1
        elif e != prev_e:
            if eDict == None:
                #compList.append((prev_e, n))
                compStr += str(n)+str(prev_e)+', '
            else:
                #compList.append((eDict[tuple(prev_e)],n))
                compStr += str(n)+str(eDict[tuple(prev_e)])+', '
            prev_e = e
            n=1
    if eDict == None:
        #compList.append((prev_e, n))
        compStr += str(n)+str(prev_e)
    else:
        #compList.append((eDict[tuple(prev_e)],n))
        compStr += str(n)+str(eDict[tuple(prev_e)])
    #return compList
    return compStr

##Put these in gui: 
folder = 'C:/Users/alana/Pictures/d20_tentacles_design/Finals'
#fname = 'test-5x6.png' 
fname = 'D20_PatternEaseEdit.png' #'d20_tentacles_resized_2color.png'

starting_corner = 'bottom-right' ##Where you want to start your pattern
flip = True ##False for evens up, true for evens down

os.chdir(folder)
im = Image.open(fname)

if starting_corner == 'bottom-left':
    pass #do nothing to the image
elif starting_corner == 'bottom-right':
    im = im.transpose(Image.FLIP_LEFT_RIGHT)
elif starting_corner == 'top-left':
    im = im.transpose(Image.FLIP_TOP_BOTTOM)
elif starting_corner == 'top-right':
    im = im.transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.FLIP_TOP_BOTTOM)
else:
    raise Exception('Please use a valid starting corner')
    
width, height = im.size
c2cRows = width+height-1 #(2*min(width,height))

imarray = np.array(im)
imw,imh,imc = imarray.shape
imarrayR = imarray.reshape((imw*imh),imc)
colors = np.unique(imarrayR,axis=0)
#colors = colors.tolist()

cTuple = tuple(map(tuple, colors))
cNames = tuple(map(chr,range(65,65+len(colors))))
cDict = dict(zip(cTuple , cNames))

print(f'This pattern has {len(colors)} colors:')
for c in cDict:
    print(f"{cDict[c]} --> {c}")

for i in range(c2cRows): #range(15,19): 
    d = np.diagonal(im,(i-height+1))
    d = d.T.tolist()
    if flip:
        d.reverse()
    instr = compress(d,cDict)
    flip = not flip
    print(f'row {i+1}, {len(d)} cells; {instr}')

