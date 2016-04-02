"""
Utilities for numpy structured arrays
"""

import numpy as np
import sys
import pdb

def pformat(file,val,iformat,fformat,sformat) :
    """ Utility routine for printing a value """
    #print 'type: ', val, type(val)
    if isinstance(val,np.ndarray) :
        for v in val :
            #call pformat in case of Nd array
            pformat(file,v,iformat,fformat,sformat)
    elif isinstance(val,(float,np.float32)) :
        file.write(fformat.format(val))
    elif isinstance(val,(int,np.int32,np.int16)) :
        file.write(iformat.format(val))
    else :
        file.write(sformat.format(str(val)))

def list(s,cols=None, cond=None, ind=None, table=None, iformat='{:6d}',fformat='{:8.2f}', sformat='{:<12s}',file=None) :
    """
    List columns of requested row

    Args:
      s (numpy structured array)  : array to show

    Keyword args:
      cols : list of columns to list
      cond : tuple of (column, value); rows where column==value will be listed
      ind : list of index(es) to print
      table : use table format

    Returns:
    """
    if file is None :
       f = sys.stdout
    else :
       f = open(file,'w')

    # Use input columns if given, else all columns
    if cols is None :
        cols = s.names

    # Use condition if given, else specified index (default ind=0)
    if cond is not None :
        inds = np.where(s[cond[0]] == cond[1])[0]
    elif ind is not None :
        try :
            test=len(ind)
        except :
            ind=[ind]
        inds = np.array(ind)
    else :
        inds = np.arange(len(s))
   
    # if not specified, use table format for multiple entries
    if table is None :
        if len(inds) > 1 :
            table = True
        else :
            table = False

    # in table format, print column names 
    if table :
        for col in cols :
            f.write(sformat.format(col))
        f.write('\n')

    # print
    for i in inds :
        for col in cols :
            if not table :
                f.write(sformat.format(col))
            pformat(f,s[i][col],iformat,fformat,sformat)
            if not table : 
                f.write('\n')
        if table :
            f.write('\n')

def add_cols(a,b):
    """ 
    Add empty columns from recarray b to existing columns from a,
    return new recarray
    """

    #newdtype = sum((tmp.dtype.descr for tmp in [a,b]), [])

    # need to handle array elements properly
    newdtype = []
    names = a.dtype.names+b.dtype.names
    descrs = a.dtype.descr+b.dtype.descr
    for i in range(len(descrs)) :
        name= names[i]
        desc= descrs[i]
        if i < len(a.dtype.names) :
            shape= a[name][0].shape
        else :
            shape= b[name][0].shape
        if len(desc) > 2 :
            newdtype.append((desc[0],desc[1],shape))
        else :
            newdtype.append((desc[0],desc[1]))
    # create new array
    newrecarray = np.empty(len(a), dtype = newdtype)
    # fill in all of the old columns
    print 'copying...'
    for name in a.dtype.names:
         print name
         newrecarray[name] = a[name]
    return newrecarray

