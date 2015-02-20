import numpy as np
from collections import OrderedDict

__author__ = "Gokul Ramesh"
__copyright__ = "Copyright 2014, LatentView Analytics Pvt. Ltd."
__email__ = "gokul.ramesh@latentview.com"
__status__ = "Development"
__version__="0.0.1"

class SparseFeatureDistanceMatrix(np.ndarray):
    
    def __new__(cls, records, metric):
        obj = np.zeros((len(records), len(records))).view(cls)
        return obj
    
    def __init__(self, records, metric):
        self.records = records
        self.metric = metric
        self.labels = {}
        self.invLabels = {}
        self.construct()
          
    def construct(self):
        for i, ikey in enumerate(self.records.keys()):
            for j, jkey in enumerate(self.records.keys()):
                if i > j:
                    self[i][j] = self[j][i]
                    continue
                dictA = self.records[ikey]
                dictB = self.records[jkey]
                self[i][j] = self.metric(dictA, dictB)
            if isinstance(ikey, str):
                self.labels[i] = [ikey]
            else:
                self.labels[i] = [n for n in ikey]
            self.invLabels[ikey] = i
                
    def fill_diagonal(self, val):
        np.fill_diagonal(self, val)
        
    def coordmax(self):
        return np.nanmax(self), divmod(np.nanargmax(self), len(self.records))
    
    def coordmin(self):
        return np.nanmin(self), divmod(np.nanargmin(self), len(self.records))
    
    def _all(self, cond):
        return bool(np.all(cond))
    
    def _any(self, cond):
        return bool(np.any(cond))
    
    def __str__(self):
        
        coord = self.coordmin()[1]
        matrix = '  '

        for rownum, row in enumerate(self):
            strnum = str(rownum)
            while len(strnum) < 3:
                strnum = ' '+strnum
            matrix += '   ' + strnum + '    '
                
        matrix += '\n    ' + 10*self.shape[0]*'-' +'\n'
        
        for rownum, row in enumerate(self):
            strnum = str(rownum)
            while len(strnum) < 3:
                strnum = ' '+strnum
            matrix += strnum + '|'
            for colnum, column in enumerate(row):        
                if not np.isnan(column):
                    val = str(round(column,4))
                    while len(val) < 6:
                        val += '0'
                    if (rownum, colnum) == coord: 
                        val = '*' + val[:-1]
                else:
                    val = 6*' '
                matrix += '  ' + val + '  '

            matrix += '|\n   |\n'
        matrix = matrix[:-2]
        Labels = '\n\nLabels: '
        for k,v in self.labels.iteritems():
            if v:
                Labels += str(k) + ' => ' + ','.join(v) + '; '
        Labels = Labels[:-2]
        matrix += Labels
        return matrix
        
    def __repr__(self):
        if not hasattr(self,'metric'):
            return super(SparseFeatureDistanceMatrix, self).__repr__()
        return self.__str__()
        
    
class ContingencyTable(np.ndarray):

    def __new__(cls, xDict, yDict):
        x = set(xDict.values())
        y = set(yDict.values())
        obj = np.zeros((len(x), len(y)), dtype=np.int).view(cls)
        return obj
    
    def __init__(self, xDict, yDict):
        xkeys = set(xDict.keys())
        ykeys = set(yDict.keys())
        if xkeys != ykeys:
            raise AssertionError("The two inputs have different records")
        self.records = xkeys
        self.xDict = xDict
        self.yDict = yDict
        
        self.construct()
        
    def construct(self):
        xMap = {clus:num for num, clus in enumerate(set(self.xDict.values()))}
        yMap = {clus:num for num, clus in enumerate(set(self.yDict.values()))}
        for record in self.records:
            x, y = xMap[self.xDict[record]], yMap[self.yDict[record]]
            self[x][y] += 1
        self.xLabels = OrderedDict(sorted(map(lambda y: y[::-1], xMap.items()),
                                          key=lambda t: t[0]))
        self.yLabels = OrderedDict(sorted(map(lambda y: y[::-1], yMap.items()),
                                          key=lambda t: t[0]))
            
    def rowsum(self):
        rs = np.zeros(self.shape[0], dtype=np.int)
        for i in range(self.shape[0]):
            rs[i] = int(self[i,:].sum())
        return rs
    
    def colsum(self):
        cs = np.zeros(self.shape[1], dtype=np.int)
        for i in range(self.shape[1]):
            cs[i] = int(self[:,i].sum())
        return cs   
		
    def rowmax(self):
        rs = np.zeros(self.shape[0], dtype=np.int)
        for i in range(self.shape[0]):
            rs[i] = int(self[i,:].max())
        return rs
    
    def colmax(self):
        cs = np.zeros(self.shape[1], dtype=np.int)
        for i in range(self.shape[1]):
            cs[i] = int(self[:,i].max())
        return cs  
    
    def rowmin(self):
        rs = np.zeros(self.shape[0], dtype=np.int)
        for i in range(self.shape[0]):
            rs[i] = int(self[i,:].min())
        return rs
    
    def colmin(self):
        cs = np.zeros(self.shape[1], dtype=np.int)
        for i in range(self.shape[1]):
            cs[i] = int(self[:,i].min())
        return cs  
        
    def __str__(self):
        rowsum, colsum = self.rowsum(), self.colsum()
            
        matrix = '  '

        for colnum in range(self.shape[1]):
            strnum = str(colnum)
            while len(strnum) < 4:
                strnum = ' '+strnum
            matrix += ' ' + strnum + '   '
                
        matrix += '\n    ' + 8*self.shape[1]*'-' + ' Total\n'
        
        for rownum, row in enumerate(self):
            strnum = str(rownum)
            while len(strnum) < 3:
                strnum = ' '+strnum
            matrix += strnum + '|'
            for colnum, column in enumerate(row):
                val = str(column)
                while len(val) < 4:
                    val += ' '
                matrix += '  ' + val + '  '
            matrix += '| ' + str(rowsum[rownum]) + ' \n   |\n'
        matrix = matrix[:-2] + ' ' +8*self.shape[1] *'-' + '\nTotal '
        for num in colsum:
            strnum = str(num)
            while len(strnum) < 4:
                strnum = strnum + ' '
            matrix += strnum + '    '
        matrix += str(int(self.sum()))
        
        xLabels = '\n\nRow-Labels: '
        for k,v in self.xLabels.iteritems():
            xLabels += str(k) + ' => ' + str(v) + ', '
        xLabels = xLabels[:-2]
        matrix += xLabels
        
        yLabels = '\nColumn-Labels: '
        for k,v in self.yLabels.iteritems():
            yLabels += str(k) + ' => ' + str(v) + ', '
        yLabels = yLabels[:-2]
        matrix += yLabels
            
        return matrix
        
    def __repr__(self):
        return self.__str__()
        