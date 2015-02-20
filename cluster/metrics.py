from matrices import ContingencyTable

def nc2(n):
    return n*(n-1)/2

class Rand:
    
    def __init__(self, xDict, yDict):
        self.ct = ContingencyTable(xDict, yDict)

        shape = self.ct.shape
        pairs = nc2(int(self.ct.sum()))
        a = sum([nc2(int(a)) for row in self.ct for a in row])
        rowwise = sum([nc2(int(b)) for b in self.ct.rowsum()])
        colwise = sum([nc2(int(c)) for c in self.ct.colsum()])
        b = rowwise - a
        c = colwise - a
        d = pairs - a - b - c
  
        self.RandIndex = (a + d)/(1.0 * pairs)
        
        numer = a - (rowwise * colwise)/(1.0 * pairs)
        denom = 0.5 * (rowwise + colwise) - (rowwise * colwise)/(1.0 * pairs)
        self.adjustedRandIndex = numer/denom
        
    def __str__(self):
        out = self.ct.__str__()
        out += '\nRandIndex: ' + str(round(self.RandIndex,4)) + '\n'
        out += 'Adjusted RandIndex: ' + str(round(self.adjustedRandIndex,4))
        return out
    
    def __repr__(self):
        return self.__str__()
    
    def writeCT(self, out):
        f = open(out,'w')
        for j in range(self.ct.shape[1]):
            f.write(',' + str(self.ct.yLabels[j]))
        f.write('\n')
        for i in range(self.ct.shape[0]):
            f.write(str(self.ct.xLabels[i]))
            for j in range(self.ct.shape[1]):
                f.write(',' + str(self.ct[i][j]))
            f.write('\n')
        f.close()