import pickle
import types

import distance

__author__ = "Gokul Ramesh"
__copyright__ = "Copyright 2014, LatentView Analytics Pvt. Ltd."
__email__ = "gokul.ramesh@latentview.com"
__status__ = "Development"
__version__="0.0.1"


class ClusterClassifier():

    similarityfn =  {a:distance.__dict__.get(a) for a in dir(distance)
              if isinstance(distance.__dict__.get(a), types.FunctionType)}
    
    def __init__(self, model, metric=None, method=None):
	
        methodNames = {'single': self.single,
                       'complete': self.complete,
                       'average': self.average,
                       'centroid': self.centroid,
                       'ward': self.ward,                             
                       }
	
        self.model = pickle.load(open(model))
        metricName = metric if metric else self.model.get('metric')
        self.metric = ClusterClassifier.similarityfn[metricName]
        methodName = method if method else self.model.get('method')
        self.method = methodNames[methodName] 
		
    def label(self, dictY, proportion=False):
        if proportion:
            dictY = {k:v/(1.0 *sum(dictY.values())) for k,v in dictY.iteritems()} 
        return self.method(dictY)
        
    def average(self, dictY):
        distances = {}
        for name, xList in self.model['clusters'].iteritems():
            distances[name] = (sum([self.metric(dictX, dictY) for dictX in xList])
                               /(1.0*len(xList)))
        return min(distances, key=distances.get)
    
    def single(self, dictY):
        distances = {}
        for name, xList in self.model['clusters'].iteritems():
            distances[name] = min([self.metric(dictX, dictY) for dictX in xList])
        return min(distances, key=distances.get)
    
    def complete(self, dictY):
        distances = {}
        for name, xList in self.model['clusters'].iteritems():
            distances[name] = max([self.metric(dictX, dictY) for dictX in xList])
        return min(distances, key=distances.get)
    
    def centroid(self, dictY):
        distances = {}
        for name, dictX in self.model['centers'].iteritems():
            distances[name] = self.metric(dictX, dictY) 
        return min(distances, key=distances.get)
    
    def ward(self,  dictY):
        distances = {}
        for name, dictX in self.model['centers'].iteritems():
            factor = len(dictX)/(1.0*(len(dictX)+1))
            distances[name] = self.metric(dictX, dictY) * factor      
        return min(distances, key=distances.get)
			
    def __str__(self):
        out = '<Classifier; '
        out += 'Metric: ' + str(self.metric.__name__) 
        out += ', Method: ' + str(self.method.__name__) + ' >' 
        return out
    
    def __repr__(self):
        return self.__str__() 