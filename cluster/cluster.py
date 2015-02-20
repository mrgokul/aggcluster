import warnings
import pickle
import types

import distance

from copy import deepcopy
from collections import Counter

from matrices import SparseFeatureDistanceMatrix
from metrics import Rand
          
__author__ = "Gokul Ramesh"
__copyright__ = "Copyright 2014, LatentView Analytics Pvt. Ltd."
__email__ = "gokul.ramesh@latentview.com"
__status__ = "Development"
__version__="0.0.1"
		  
		
class Cluster():
    
    def __init__(self, name, left=None, right=None, distance=0.0):
        self.name = name
        self.children = []
        self.attrs = {}
        self.root = True
        self.dendro = {}
        self.distance = distance
        self.leaf = False
        
        if left:
            self.children.append(left)
            self.children.append(right)
            left.root = False
            right.root = False
            self.numRecords = left.numRecords + right.numRecords 
            self.records = left.records + right.records
        else:
            self.leaf = True
            self.numRecords = 1
            self.records = [self.name]
           
        self.attrs['name'] = self.name
        self.attrs['distance'] = self.distance
        self.attrs['num_records'] = self.numRecords
        if self.leaf:
            self.attrs['leaf'] = True
		
        self._constructDendro()
        
    def _constructDendro(self):
        if not self.leaf:
            self.dendro['children'] = []
            self.dendro['children'].append(self.children[0].dendro)
            self.dendro['children'].append(self.children[1].dendro)
        for k,v in self.attrs.iteritems():
            self.dendro[k] = v
			
    def __str__(self):
        out = '<Cluster: ' + self.name
        out += ', #Records: ' + str(self.numRecords) + '>'
        return out
    
    def __repr__(self):
        return self.__str__() 
		
class Agglomerator():
    
    similarityfn =  {a:distance.__dict__.get(a) for a in dir(distance)
              if isinstance(distance.__dict__.get(a), types.FunctionType)}
    
    
    def __init__(self, records, proportion=False, metric='cosine', method='centroid'
                 ,maxClusters=None, threshold=None, supervise=None, nodeFolder=None):
        
        methodNames = {'single': self.single,
                       'complete': self.complete,
                       'average': self.average,
                       'centroid': self.centroid,
                       'ward': self.ward,                             
                       }
        
        if threshold is None and maxClusters is None and supervise is None:
            raise ValueError("Either max clusters or threshold value"
                             "or supervise should be specified") 
        if supervise:
            if threshold or maxClusters:
                raise ValueError("Do not specify threshold or maxClusters"
                             " in supervise mode")
        self.records = records
        self.proportion = proportion
        self.metric = metric
        self.method = method
        self.maxClusters = maxClusters
        self.threshold = threshold
        self.supervise = supervise
        self.__clusterNumber = 0
        self.similarityfn = Agglomerator.similarityfn[metric]
        self.method = methodNames[method]
        self.superviseComplete = False
        
        self.num_clusters = len(records)
        if self.proportion:
            self.weights = {k:sum(v.values()) for k,v in self.records.iteritems()}
            self.records = {k:{r:a/(1.0 *sum(v.values())) for r, a in v.iteritems()} 
                            for k, v in self.records.iteritems()}
        self.dm = SparseFeatureDistanceMatrix(self.records,self.similarityfn)
        self.dm.fill_diagonal(None)
        self.singletonDM = deepcopy(self.dm)
        self.singletonDM.invLabels = self.dm.invLabels
        
        self.clusters = {}
        for name in self.records.keys():
            singleton = Cluster(name)
            self.clusters[tuple([name])] = singleton
            
        if self.supervise:
            self.maxClusters = 1
            self.__allErrors = []           
            self.cluster()
            self.__forceLearn()
        
    def completed(self):
        if self.maxClusters:
            complete = self.num_clusters == self.maxClusters
            if self.threshold:
                complete = complete or self.dm.coordmin()[0] > self.threshold
        else:
            complete =  self.dm.coordmin()[0] > self.threshold
        return complete
    
    def __nameNode(self):
        name = 'Node' + str(self.__clusterNumber)
        self.__clusterNumber += 1
        return name
    
    def mergeOne(self):
        if self.superviseComplete:
            raise ValueError("Supervised mode on! Cannot cluster!")
        
        val, coord = self.dm.coordmin()
        dist = round(float(val),4)
        left = self.clusters[tuple(self.dm.labels[coord[0]])]
        right = self.clusters[tuple(self.dm.labels[coord[1]])]
        newcluster = Cluster(self.__nameNode(), left, right, dist)
        
        self.merge(coord[0],coord[1])
        self.num_clusters -= 1
        self.clusters[tuple(self.dm.labels[coord[0]])] = newcluster
        if self.supervise:
            rand = self.evaluate(self.supervise)
            error = {'rand':rand.RandIndex, 
                     'N': self.num_clusters,
                     'adjRand':rand.adjustedRandIndex} 
            self.__allErrors.append(error)
            
    def merge(self, x, y):
        self.dm.labels[x].extend(self.dm.labels[y])
        self.dm.labels[x] = sorted(self.dm.labels[x])
        self.dm.labels[y] = None
        self.dm[y,0:] = None
        self.dm[0:,y] = None
        for index, label in self.dm.labels.iteritems():
            if not label or index==x:
                continue
            distance = self.method(self.dm.labels[x], self.dm.labels[index])
            self.dm[x][index] = self.dm[index][x] = distance
            
    def average(self, xlabels, ylabels):
        distances = []
        for x in xlabels:
            xindex = self.singletonDM.invLabels[x]
            for y in ylabels:
                yindex = self.singletonDM.invLabels[y]
                distances.append(self.singletonDM[xindex][yindex])
        return sum(distances)/(1.0*len(xlabels)*len(ylabels))
    
    def single(self, xlabels, ylabels):
        distances = []
        for x in xlabels:
            xindex = self.singletonDM.invLabels[x]
            for y in ylabels:
                yindex = self.singletonDM.invLabels[y]
                distances.append(self.singletonDM[xindex][yindex])
        return min(distances)
    
    def complete(self, xlabels, ylabels):
        distances = []
        for x in xlabels:
            xindex = self.singletonDM.invLabels[x]
            for y in ylabels:
                yindex = self.singletonDM.invLabels[y]
                distances.append(self.singletonDM[xindex][yindex])
        return max(distances)
    
    def centroid(self, xlabels, ylabels):
        if self.proportion:
            weightX = {k:{r:a * self.weights[k] for r, a in 
                          self.records[k].iteritems()} for k in xlabels}
            weightY = {k:{r:a * self.weights[k] for r, a in 
                          self.records[k].iteritems()} for k in ylabels}
  
            sumX = Counter()
            for v in weightX.values():
                for k,v1 in v.iteritems():
                    sumX[k] += v1
 
            sumY = Counter()
            for v in weightY.values():
                for k,v1 in v.iteritems():
                    sumY[k] += v1  
					
            centX = {k:v/(1.0 *sum(sumX.values())) for k, v in sumX.iteritems()} 
            centY = {k:v/(1.0 *sum(sumY.values())) for k, v in sumY.iteritems()}                     
        else:
            sumX = Counter()
            for v in xlabels:
                for k,v1 in self.records[v].iteritems():
                    sumX[k] += v1
            sumY = Counter()
            for v in ylabels:
                for k,v1 in self.records[v].iteritems():
                    sumY[k] += v1
            centX = {k:v/(1.0*len(xlabels)) for k,v in sumX.iteritems()}
            centY = {k:v/(1.0*len(ylabels)) for k,v in sumY.iteritems()}
        return self.similarityfn(centX,centY)
    
    def ward(self, xlabels, ylabels):
        centroid = self.centroid(xlabels, ylabels)
        factor = (len(xlabels)*len(ylabels))/(1.0*(len(xlabels)+len(ylabels)))
        return centroid**2 * factor    
                 
    def cluster(self):
        while not self.completed():
            self.mergeOne()         
        print 'Clustering completed'
        if self.supervise:
            self.superviseComplete = True
        
    def __forceLearn(self):
        d = dict()
        if isinstance(self.supervise, file):
            for row in self.supervise:
                record, cluster = row.strip().split(',')
                if d.has_key(cluster):
                    d[cluster].append(record)
                else:
                    d[cluster] = [record]
        elif isinstance(self.supervise, dict):
            for record,cluster in self.supervise.items():
                if d.has_key(cluster):
                    d[cluster].append(record)
                else:
                    d[cluster] = [record] 
                    
        self.clusters = {}
        newRecords = {}
        for k,v in d.iteritems():
            self.clusters[tuple(v)] = Cluster(k)
            newRecords[tuple(v)] = {}
        self.num_clusters = len(self.clusters)
        self.maxClusters = None
            
        self.__selectBest()
        
        self.dm = SparseFeatureDistanceMatrix(newRecords,self.similarityfn)
        self.dm.fill_diagonal(None)
        for x in range(self.num_clusters):
            for y in range(self.num_clusters):
                if x>=y:
                    continue
                distance = self.method(self.dm.labels[x], self.dm.labels[y])
                self.dm[x][y] = self.dm[y][x] = distance
            
    def __selectBest(self):
        N, R, AR = [], [], []
        for error in self.__allErrors:
            N.append(round(error['N'],6))
            R.append(round(error['rand'],6))
            AR.append(round(error['adjRand'],6))
        self.best, rand, adjRand = dict(), dict(), dict()
        r = max(R)
        nrand = N[R.index(r)]
        ar = max(AR)
        nArand = N[AR.index(ar)]
        rand['value'], rand['N'] = r, nrand
        adjRand['value'], adjRand['N'] = ar, nArand
        self.best['rand'] = rand
        self.best['adjRand'] = adjRand
             
    def writeClusters(self, out):
        if not self.completed():
            warnings.warn("Clustering not yet completed")
        f = open(out,'w')
        f.write("record,cluster\n")
        for k,v in self.clusters.iteritems():
            if v.root:
                for record in k:
                    line = record + ',' + v.name + '\n'
                    f.write(line)
        f.close()
		
    def evaluate(self, y):
        if not self.completed() and not self.supervise:
            warnings.warn("Clustering not yet completed")
        x = {t:v.name for k,v in self.clusters.iteritems() for t in k if v.root}
        if isinstance(y, file):
            d = dict()
            for row in y:
                rowList = row.strip().split(',')
                d[rowList[0]] = rowList[1]
            y.seek(0)
        elif isinstance(y, dict):
            d = y
        else:
            raise ValueError("File or dictionary expected")
        return Rand(x,d)
    
    def saveClassifier(self, out):
        if not self.completed():
            warnings.warn("Clustering not yet completed")
        outDict = dict()
        outDict['metric'] = self.metric
        outDict['method'] = self.method.__name__
        outDict['clusters'] = {}
        outDict['centers'] = {}
        for  k,v in self.clusters.iteritems():
            if v.root:
                outDict['clusters'][v.name] = []
                sumX = Counter()
                for t in k:
                    outDict['clusters'][v.name].append(self.records[t])
                    if self.proportion:
                        weightX = {r:a * self.weights[t] for r, a in 
                                   self.records[t].iteritems()}
                        for k1,v1 in weightX.iteritems():
                            sumX[k1] += v1  
                    else:
                        for k1,v1 in self.records[t].iteritems():
                            sumX[k1] += v1
                if self.proportion:
                    outDict['centers'][v.name] = {k2:v2/(1.0 *sum(sumX.values()))
                                                  for k2,v2 in sumX.iteritems()} 
                else:                       
                    outDict['centers'][v.name] ={k2:v2/(1.0*len(k))
                                                 for k2,v2 in sumX.iteritems()}                    
        pickle.dump(outDict,open(out,'wb'))        
		
    def getDendrogram(self):
        if not self.completed():
            warnings.warn("Clustering not yet completed")
        roots = []
        for c in self:
            c.dendro['root'] = True
            roots.append(c.dendro)
        return roots
 		
    def __iter__(self):
        return iter([c for c in self.clusters.values() if c.root])
        
    def __str__(self):
        out = '#Records: ' + str(len(self.records))
        out += ', #ClustersPresent: ' + str(self.num_clusters)
        out += ', Max.Cluster: ' + str(self.maxClusters) + '\n\nClusters:\n' + 30*'-'+'\n'
        for k,v in self.clusters.iteritems():
            if v.root:
                out += v.name + ' => ' + ','.join(k) + '\n'
        return out
    
    def __repr__(self):
        return self.__str__()        