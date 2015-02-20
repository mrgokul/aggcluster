import json
import os
import pkg_resources  
  
class DendrogramForD3():

    def __init__(self,clusters,folder=None):
        self.folder=folder
        self.root = {"name":"root","children":clusters}
        self._unpackDict(self.root)		
        self.html = pkg_resources.resource_string('cluster', 
		                                          'templates/dendrogram.html')
	
    def _unpackDict(self,aDict):
        if aDict.has_key('children'):
            self._unpackList(aDict['children'])
        if aDict.has_key('leaf'):
            aDict['link'] = os.path.join(self.folder,aDict['name'])     
            aDict['leaf'] = str(aDict['leaf']).lower()			
			
    def _unpackList(self,aList):
        for i in aList:
            self._unpackDict(i)        
			
    def write(self,out):
        html = self.html.replace('%JSON%', json.dumps(self.root))
        f = open(out,'w')
        f.write(html)
        f.close()

    