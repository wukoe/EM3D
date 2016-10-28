# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 13:53:45 2016
@author: wubia

evaluation of segmentation.
"""
import numpy as np
#import pdb

# variance of information)
#  OE,UE = varinfo(gt,pred)
def varinfo(gt,pred):
    Z = 1
    
    sz=gt.shape
    sz=np.prod(sz)    
    gt=gt.reshape((1,sz))
    pred=pred.reshape((1,sz))
    
    gtlb=np.unique(gt)
    predlb=np.unique(pred)
    gtlbnum=len(gtlb)
    predlbnum=len(predlb)
    print('gt and pred label number:%d,%d'%(gtlbnum,predlbnum))
    
    intersectss=np.zeros((gtlbnum,predlbnum))
    predss=np.zeros(predlbnum)
    gtss=np.zeros(gtlbnum)
    # prediction have more labels due to oversegmentation, so put it in outer loop saves computation.
    for pi in range(predlbnum):
        predseg=(pred==predlb[pi])            
        predss[pi]=np.sum(predseg) # prediction size        
        for gi in range(gtlbnum):
            gtseg=(gt==gtlb[gi])
            gtss[gi]=np.sum(gtseg) # gt size (本行重复进行，但求和计算开销较小，比单独开循环合理)
            intersectss[gi,pi]=np.sum(gtseg & predseg) # intersect size
        print('|',end='')
        
    I = (intersectss>0)
    Igt = np.logical_or.reduce(I,1)
    Ipred = np.logical_or.reduce(I,0)
    
    intersectss=intersectss[Igt][:,Ipred]
    gtss=gtss[Igt]
    predss=predss[Ipred]
    
    # intersect size / gt size
    intgtR = intersectss.transpose()/gtss
    intgtR = intgtR.transpose()
    # intersect size / pred size
    intpredR = intersectss/predss
    
    # Calculate
    I = (intersectss==0)
    oe = intersectss*np.log(intgtR)
    oe[I]=0
    oe = -np.sum(oe)/Z # over segment VI
    ue = intersectss*np.log(intpredR)
    ue[I]=0
    ue = -np.sum(ue)/Z # under segment VI

    return oe,ue