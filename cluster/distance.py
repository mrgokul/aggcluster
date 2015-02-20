import math
from collections import OrderedDict
import util.text as textutil

__author__ = "Gokul Ramesh"
__copyright__ = "Copyright 2014, LatentView Analytics Pvt. Ltd."
__email__ = "gokul.ramesh@latentview.com"
__status__ = "Development"
__version__="0.0.1"


def cosine(dictA, dictB):
    Asquare = sum([x**2 for x in dictA.values()])
    Bsquare = sum([x**2 for x in dictB.values()])
    common = set(dictA.keys()) & set(dictB.keys())
    AdotB = sum([dictA[key] * dictB[key] for key in common])
    denom = math.sqrt(Asquare * Bsquare)
    return (1.0-AdotB/denom) if denom else 1.0
	
def tanimoto(dictA, dictB):
    Asquare = sum([x**2 for x in dictA.values()])
    Bsquare = sum([x**2 for x in dictB.values()])
    common = set(dictA.keys()) & set(dictB.keys())
    AdotB = sum([dictA[key] * dictB[key] for key in common])
    denom = Asquare+Bsquare - AdotB
    return (1.0-AdotB/(1.0*denom)) if denom else 1.0
	
def jaccard(dictA, dictB):
    keys = set(dictA.keys()) | set(dictB.keys())
    num, denom = zip(*[(min(dictA.get(i,0),dictB.get(i,0)),
                        max(dictA.get(i,0),dictB.get(i,0))) for i in keys]) 
    return 1-sum(num)/(1.0*sum(denom))
		
def euclidean(dictA, dictB):
    keys = set(dictA.keys()) | set(dictB.keys())
    return math.sqrt(sum([(dictA.get(i,0) - dictB.get(i,0))**2 for i in keys]))
	
def manhattan(dictA, dictB):
    keys = set(dictA.keys()) | set(dictB.keys())
    return sum([math.fabs((dictA.get(i,0) - dictB.get(i,0))) for i in keys])
	
def pearson(dictA, dictB):
    keys = set(dictA.keys()) | set(dictB.keys())
    avg_x = sum(dictA.values()) / (1.0*len(keys))
    avg_y = sum(dictB.values()) / (1.0*len(keys))
    num = sum([(dictA.get(key,0) - avg_x)*(dictB.get(key,0) - avg_y) 
               for key in keys])
    denomX = sum([(dictA.get(key,0) - avg_x)**2 for key in keys])
    denomY = sum([(dictB.get(key,0) - avg_y)**2 for key in keys])
    return 1 - num / (1.0*math.sqrt(denomX * denomY))
	
def levenshtein100(dictA, dictB):
    dictA = OrderedDict(sorted(dictA.items(), 
                       key=lambda t: t[1],reverse=True)[:10])
    dictB = OrderedDict(sorted(dictB.items(), 
                       key=lambda t: t[1],reverse=True)[:10])
    return sum([v1*v2*textutil.levenshtein(k1,k2) for k1,v1 in dictA.iteritems()
                for k2,v2 in dictB.iteritems()])