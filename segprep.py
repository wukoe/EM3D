# -*- coding: utf-8 -*-
"""
Created on Tue Aug 30 21:23:32 2016

@author: wubia
"""
import h5py
import dataloader
import numpy as np

###### Squeeze label types values.
def labelsqueeze(X):
    lbtp=np.unique(X)
    Y = np.zeros(X.shape)
    for k in range(len(lbtp)):
        I = X==lbtp[k]
        Y[I] = k+1
    return Y

###### Create boundary out of the segmentation.
### Auxiliary functions

# range in [-width/2+1,  width/2]
def smeardata(X,width,axis=1):
    if axis==0:
        X=X.transpose()
    
    width=int(np.floor(width/2))
    tp=np.array(X)
    for k in range(width-1):
        tp[:,0:-1-k] += X[:,1+k:]        
    for k in range(width):
        tp[:,1+k:] += X[:,0:-1-k]    
    X=tp
    
    if axis==0:
        X=X.transpose()
        
    return X>0

### Methods
# seg2bound option - with 6 connect filter.
def getbound_6con(seglabels,width):
    lsize=seglabels.shape

    new_labels_1=np.zeros(lsize,dtype=bool)
    rowfill=np.zeros((1,lsize[1]),dtype=bool)
    colfill=np.zeros((lsize[2],1),dtype=bool)    
    for k in range(lsize[0]):
        a=seglabels[k,:,:]
        I = abs(np.diff(a,axis=0))>0.5
        tp = smeardata(np.concatenate((I,rowfill)),width,axis=0)
        I = abs(np.diff(a,axis=1))>0.5
        new_labels_1[k,:,:] = tp | smeardata(np.concatenate((I,colfill),axis=1),width)

    new_labels_2 = np.zeros(lsize,dtype=bool)
    rowfill=np.zeros((1,lsize[0]),dtype=bool)
    colfill=np.zeros((lsize[2],1),dtype=bool)
    for k in range(lsize[1]):
        a=seglabels[:,k,:]
        I = abs(np.diff(a,axis=0))>0.5
        tp = smeardata(np.concatenate((I,rowfill)),width,axis=0) 
        I = abs(np.diff(a,axis=1))>0.5
        new_labels_2[:,k,:] = tp | smeardata(np.concatenate((I,colfill),axis=1),width) 
        
    new_labels_3 = np.zeros(lsize,dtype=bool)
    rowfill=np.zeros((1,lsize[0]),dtype=bool)
    colfill=np.zeros((lsize[1],1),dtype=bool)
    for k in range(lsize[2]):
        a=seglabels[:,:,k]
        I = abs(np.diff(a,axis=0))>0.5
        tp = smeardata(np.concatenate((I,rowfill)),width,axis=0) 
        I = abs(np.diff(a,axis=1))>0.5
        new_labels_3[:,:,k] = tp | smeardata(np.concatenate((I,colfill),axis=1),width)

    I = new_labels_1 | new_labels_2 | new_labels_3
    a=np.zeros(lsize)
    a[I]=1
    return a

### Section main
# width determine the width of boudary. 
def seg2bound(segFileName,opt,width,flagReturnBound=False):
    curSaveFile=segFileName[:-3]+'_boundary.h5'    
    seglabels=dataloader.h5read(segFileName,'/label')
    
    if opt=='6con':
        B = getbound_6con(seglabels,width)
    else:
        print('no such option')
        return
    
    with h5py.File(curSaveFile,'w') as fh:
        fh.create_dataset('/label',data=B)
        fh.close()        
    print(['Saved  ', curSaveFile,  '...'])
    
    if flagReturnBound:
        return B
    else:
        return

###### Data augmentation
def dataug(datafile,labelfile):
    # Read in data.
    data = dataloader.h5read(datafile,'/data')
    lb = dataloader.h5read(labelfile,'/data')
    datafile=datafile[:-3] # remove '.h5'
    
    # first    
    X,L = create8var(data,lb)
    saveaug(datafile,1,X,L)
    
    # flip along z axis
    data=data[::-1,:,:]; lb=lb[::-1,:,:]
    X,L = create8var(data,lb)
    saveaug(datafile,9,X,L)

    return    

def create8var(data,lb):
    # 0: original
    X=[data]; L=[lb];
    # 1: flip along x axis
    X.append(data[:,:,::-1]); L.append(lb[:,:,::-1]);
    # 2: flip along y axis
    X.append(data[:,::-1,:]); L.append(lb[:,::-1,:]);
    # 3: rotate 90
    X.append(np.rot90(data)); L.append(np.rot90(lb));
    # 4: rotate 180 (=flip x and y)
    X.append(X[1][:,::-1,:]); L.append(L[1][:,::-1,:]);
    # 5: rotate -90
    X.append(np.rot90(data,-1)); L.append(np.rot90(lb,-1));
    # 6: rotate 90 + flip x
    X.append(np.rot90(X[1])); L.append(np.rot90(L[1]));
    # 7: rotate 90 + flip y
    X.append(np.rot90(X[2])); L.append(np.rot90(L[2]));
    return X,L
    
def saveaug(fn,basenum,X,L):
    with h5py.File(fn,'w') as fh:
        fh.create_dataset('/data',data=X)
        fh.create_dataset('/label',data=L)
        fh.close()        
    return
    
###### Split large volume
# in default assume data is 3D.
def volsplit(volFileName,blocksize,stride=None):
    import dm
    
    blocksize=tuple(blocksize)
    if stride==None:
        stride=blocksize 
        
    # open input file
    with h5py.File(volFileName) as fh:
        X=fh['/data']

        datasize=X.shape
        blocksize=min(blocksize,datasize)    
        segs = [dm.cutseg(datasize[k],blocksize[k],stride[k]) for k in range(3)]
        volFileName=volFileName[:-3]
        for zi in range(len(segs[2])):
            for yi in range(len(segs[1])):
                for xi in range(len(segs[0])):
                    vol = X[segs[2][zi][0]:segs[2][zi][1]+1, segs[1][yi][0]:segs[1][yi][1]+1, segs[0][xi][0]:segs[0][xi][1]+1]                    
                    blockFileName=volFileName+'_z'+str(zi)+'y'+str(yi)+'x'+str(xi)
                    
                    with h5py.File(blockFileName,'w') as bf:
                        bf.create_dataset('/data',data=vol)
                        bf.close()
                    print(blockFileName+' saved')
        fh.close()
    return segs

# memory version of volume split
def volsplit_mem(X,blocksize,stride=None):
    import dm
    
    blocksize=tuple(blocksize)
    if stride==None:
        stride=blocksize
    datasize=X.shape
    blocksize=min(blocksize,datasize)    
    segs = [dm.cutseg(datasize[k],blocksize[k],stride[k]) for k in range(3)]
                
    SZ = []
    for zi in range(len(segs[2])):
        SY = []
        for yi in range(len(segs[1])):
            SX =[]
            for xi in range(len(segs[0])):
                SX.append(X[segs[2][zi][0]:segs[2][zi][1]+1, segs[1][yi][0]:segs[1][yi][1]+1, segs[0][xi][0]:segs[0][xi][1]+1])
            SY.append(SX)            
        SZ.append(SY)
    
    return SZ
    
######