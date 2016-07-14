'''data processing misc'''
#

######### Create list with pre-allocated length
# here not use numpy
def newlist(l1,*args):
    L=[0*l1 for r in range(l1)] #need this no matter which option of input
    # For 2D matrix
    if len(args)==1:
        for r in range(l1):
            L[r]=[0*args[0] for k in range(args[0])]
    return L


######### Remove the diagonal element of matrix
#  Y=rmdiag(X)
# Y a numpy array
def rmdiag(X):
    dlen=min(X.shape)
    for k in range(dlen):
        X[k,k]=0
    return X


####### Find statistics of each sub-list(a cell)
def cellstat(X,opt,dim=1):
    if opt=='len':
        S=[len(it) for it in X]
    elif opt=='size':
        S=[it.shape[dim-1] for it in X]
    else:
        raise AssertionError('invalid option')
    return S

#########
def reabylb(X):
    xlen=len(X)
    if xlen==0:
        return

    ### Skim the label list for label types
    lbl=[X[0]];# label list: list for different labels
    tAmt=1;
    for m in range(1,xlen):
        # check if current label already exist in label list
        bExist=False
        for n in range(tAmt):
            if X[m]==lbl[n]:
                bExist=True
                break
        if not bExist: # if not, add it to the label list
            tAmt+=1
            lbl.append(X[m])

    # now lbl contain all the value of all kind of labels in lb
    lbl.sort(); # mentain the ascending order of different labels,

    ###
    typeAmt=newlist(tAmt)
    idx=newlist(tAmt)
    for m in range(tAmt):
        idx[m]=[i for i,x in enumerate(X) if x==lbl[m]]
        typeAmt[m]=len(idx[m])

    L={'tAmt':tAmt,'types':lbl,'typeAmt':typeAmt,'idx':idx}
    return L


########## Split each item in a list of strings to segments
def listsep(X,dechar=' '):
    ra=len(X)
    for k in range(ra):
        tp=X[k]
        if isinstance(tp,str):
            tp=tp.split(dechar)
        X[k]=tp
    return X

######### Get one "column" of list.
#  Y=getcol(X,colid,dechar=' ',bNum=False)
# bNum=True will convert the column (if string) to float number.
def getcol(X,colid,dechar=' ',bNum=False):
    X=listsep(X,dechar) # listsep will not separate if it already have multiple columns

    import numbers
    if isinstance(colid,numbers.Number):
        flagList=False
    else:
        flagList=True

    if bNum:
        if flagList:
            Y=[[float(it[k]) for k in colid] for it in X]
        else:
            Y=[float(it[colid]) for it in X]
    else:
        if flagList:
            Y=[[it[k] for k in colid] for it in X]
        else:
            Y=[it[colid] for it in X]
    return Y


######### Find index of all occurance of a target variable.
def find(X,tar):
    I=[i for i,j in enumerate(X) if j==tar]
    return I


######### Cut segment
# cutseg(xrange,seglen,bIdxSeg=True,bEqLen=False,bOverlap=False)
def cutseg(xrange,seglen,bIdxSeg=True,bOverlap=False):
# Explain:
# bOverlap=false: 段与段之间是否重叠
# bIdxSeg: 采用Index形式的分段。 Index形式：所得值皆为整数，且segm前一段尾和后一段头差1.

    #
    if type(xrange)!=list and type(xrange)!=tuple:
        xrange=[0,xrange-1]

    if bIdxSeg:
        xlen=xrange[1]-xrange[0]+1
    else:
        xlen=xrange[1]-xrange[0]

    # Check seglen and xlen input
    if bIdxSeg:
        seglen=round(seglen)
        if seglen<1:
            print('segment length smaller than 1')

    if xlen<=seglen:
        return xrange


    ##########
    if bOverlap: ### Overlap bins ! not tested.
        pass
#        if bIdxSeg:
#            seglen=floor(seglen)
#            interlen=floor(interlen)
#
#        segAmt=ceil((xlen-seglen)/interlen)+1

        # Filling the segm
#        if bIdxSeg:
#            segm=[[interlen*k+xrange[0],interlen*(k+1)-1+xrange[0]] for k in range(segAmt)]
#            segm[segAmt-1][1]=xrange[1]
#        else:
#            segm=[[interlen*k+xrange[0],interlen*(k+1)+xrange[0]] for k in range(segAmt)]
#            segm[segAmt-1][1]=xrange[1]

    else:  ### no overlap scheme
        segAmt=xlen//seglen
        if xlen%seglen>0:
            segAmt+=1

        # Filling the segm
        if bIdxSeg:
            segm=[[seglen*k+xrange[0],seglen*(k+1)-1+xrange[0]] for k in range(segAmt)]
            segm[segAmt-1][1]=xrange[1]
        else:
            segm=[[seglen*k+xrange[0],seglen*(k+1)+xrange[0]] for k in range(segAmt)]
            segm[segAmt-1][1]=xrange[1]

    return segm


###### range
def beinrange(x,r):
    if isinstance(x,list):
        if r[0]!=[]:
            x=list(map(lambda x:max(x,r[0]),x))
        if r[1]!=[]:
            x=list(map(lambda x:min(x,r[1]),x))
    else:
        if r[0]!=[]:
            x=max(x,r[0])
        if r[1]!=[]:
            x=min(x,r[1])

    return x