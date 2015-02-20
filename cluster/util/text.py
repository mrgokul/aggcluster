from itertools import izip
import numpy as np

__author__ = "Gokul Ramesh"
__copyright__ = "Copyright 2014, LatentView Analytics Pvt. Ltd."
__email__ = "gokul.ramesh@latentview.com"
__status__ = "Development"
__version__="0.0.1"

		
def nNGrams(iterable, nList):
    if nList == [-1]:
        return [[iterable]]
    return [izip(*[iterable[i:] for i in range(n)]) for n in nList]
	
def levenshtein(source, target):
    if len(source) < len(target):
        return levenshtein(target, source)
 
    if len(target) == 0:
        return len(source)
 
    source = np.array(tuple(source))
    target = np.array(tuple(target))

    previous_row = np.arange(target.size + 1)
    for s in source:

        current_row = previous_row + 1

        current_row[1:] = np.minimum(
                current_row[1:],
                np.add(previous_row[:-1], target != s))

        current_row[1:] = np.minimum(
                current_row[1:],
                current_row[0:-1] + 1)
 
        previous_row = current_row
 
    return previous_row[-1]
