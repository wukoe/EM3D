# -*- coding: utf-8 -*-
"""
Created on Thu May 12 12:28:38 2016
MISC data loader
@author: wb
"""
import numpy as np

""" TIFF image (multi-page) loader
"""
def imgtiff(fileName,idx=None):
    from PIL import Image

    with Image.open(fileName) as im:
        # Preprocessing.
        if idx==None:
            # determine number of pages in tiff and index
            try:
                ct=0
                while ct<10000:
                    im.seek(ct)
                    ct+=1
            except:
                imnum=ct-1
                idx=range(ct)

        else: # determine number of reading by idx
            imnum=len(idx)

        # Load in the data.
        try:
            im.seek(0)
            x=np.array(im)
            imshape=x.shape
            X = np.zeros([imshape[0],imshape[1],imnum])
            for k in range(imnum):
                im.seek(idx[k])
                X[:,:,k]=im
        except:
            im.close()
            print('can not fetch page %d'%idx[k])
            return

        if imnum==1:
            X=np.squeeze(X)

    return X