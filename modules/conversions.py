#Created on 6/18/2015
#@author: rspies
# Python 2.7

######################################################################################################
#This script contains several functions for common conversions:
#1 dms_to_dd: degrees, minutes, seconds to decimal degrees
######################################################################################################

# degrees, minutes, seconds to decimal degrees
def dms_to_dd(d,m,s,hemi):
    if hemi == 'S' or hemi == 'W':
        print 'Note: dms_to_dd conversion assumes you are using absolute degrees!!!'
        d = -1*d
        dd = -(float(s)/3600) - float(m)/60 + float(d)  
    else:
        dd = float(d) + float(m)/60 + float(s)/3600
    return dd

# remove accents on letters
import unicodedata
def strip_accents(s):
    s = unicode(s, "utf-8")
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')
