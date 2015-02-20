# aggcluster

Agglomerative Hierarchical Clustering done in Python. Supports the following similarity functions
* cosine
* euclidean
* pearson
* manhattan
* tanimoto
* jaccard

Also supports the following linkage methods
* single
* complete
* average
* centroid
* ward

Other useful features include
* scaling clusters by proportion
* saving the cluster as a model for classification purposes
* calculating error metrics - RandIndex and AdjustedRandIndex
* Dendrogram in D3.js - output as a HTML file

##Example

```python
inp = {'0': {'checking': 60, 'first': 60, 'without': 60},
 '1': {'consulting': 15, 'first': 15, 'without': 15},
 '10': {'first': 5, 'looking': 5, 'without': 5},
 '11': {'checking': 5, 'first': 5, 'reviews': 5},
 '12': {'first': 5, 'using': 5, 'without': 5},
 '13': {'first': 5, 'plan': 5, 'without': 5},
 '14': {'checking': 4, 'reviews': 4, 'without': 4},
 '15': {'first': 4, 'go': 4, "it's": 4},
 '16': {'first': 4, 'go': 4, 'without': 4},
 '17': {'first': 4, 'look': 4, 'place': 4},
 '18': {'first': 4, 'time': 4, 'use': 4},
 '19': {'checking': 4, 'vacation': 4, 'without': 4},
 '2': {'first': 13, 'time': 13, 'using': 13},
 '20': {'apps': 4, 'first': 4, 'one': 4},
 '21': {'first': 4, 'planning': 4, 'stop': 4},
 '22': {'checking': 4, 'travel': 4, 'without': 4},
 '23': {'first': 4, 'reviewing': 4, 'without': 4},
 '24': {'checking': 4, 'hotel': 4, 'without': 4},
 '25': {'first': 3, 'go': 3, 'travel': 3},
 '26': {'first': 3, 'time': 3, 'trying': 3},
 '27': {'anywhere': 3, 'go': 3, 'never': 3},
 '28': {'anything': 3, 'checking': 3, 'without': 3},
 '29': {'check': 3, 'first': 3, 'travel': 3},
 '3': {'first': 12, 'time': 12, 'used': 12},
 '30': {'always': 3, 'choice': 3, 'first': 3},
 '31': {'california': 3, 'first': 3, 'time': 3},
 '32': {'check': 3, 'first': 3, 'hotels': 3},
 '33': {'checking': 3, 'first': 3, 'must': 3},
 '34': {'first': 3, 'time': 3, 'vacation': 3},
 '35': {'first': 3, 'place': 3, 'time': 3},
 '36': {'check': 3, 'first': 3, 'place': 3},
 '37': {'back': 3, 'first': 3, 'page': 3},
 '38': {'first': 3, 'going': 3, 'without': 3},
 '39': {'first': 3, 'go': 3, 'planning': 3},
 '4': {'first': 12, 'go': 12, 'place': 12},
 '40': {'first': 3, 'read': 3, 'reviews': 3},
 '41': {'always': 3, 'first': 3, 'go': 3},
 '42': {'anywhere': 3, 'stay': 3, 'without': 3},
 '43': {'first': 2, 'phoenix': 2, 'time': 2},
 '44': {'book': 2, 'hotel': 2, 'without': 2},
 '45': {'attractions': 2, 'first': 2, 'hotels': 2},
 '46': {'checking': 2, 'reservation': 2, 'without': 2},
 '47': {'booking': 2, 'check': 2, 'first': 2},
 '48': {'first': 2, 'go': 2, 'site': 2},
 '49': {'beat': 2, "can't": 2, 'first': 2},
 '5': {'anywhere': 10, 'checking': 10, 'without': 10},
 '6': {'always': 8, 'check': 8, 'first': 8},
 '7': {'anywhere': 7, 'first': 7, 'without': 7},
 '8': {'anywhere': 6, 'go': 6, 'without': 6},
 '9': {'always': 6, 'first': 6, 'stop': 6}}

agg = Agglomerator(inp,threshold=0.66,metric='cosine',method='average') 
agg.cluster()

for cluster in agg:
    print cluster, [inp[r] for r in cluster.records] , '\n'
    
'''

<Cluster: 49, #Records: 1> [{'beat': 2, "can't": 2, 'first': 2}] 

<Cluster: Node35, #Records: 3> [{'read': 3, 'reviews': 3, 'first': 3}, {'checking': 5, 'reviews': 5, 'first': 5}, {'checking': 3, 'must': 3, 'first': 3}] 

<Cluster: 27, #Records: 1> [{'go': 3, 'anywhere': 3, 'never': 3}] 

<Cluster: Node41, #Records: 18> [{'without': 3, 'anywhere': 3, 'stay': 3}, {'checking': 10, 'anywhere': 10, 'without': 10}, {'without': 7, 'anywhere': 7, 'first': 7}, {'go': 6, 'anywhere': 6, 'without': 6}, {'checking': 4, 'hotel': 4, 'without': 4}, {'checking': 4, 'travel': 4, 'without': 4}, {'checking': 2, 'reservation': 2, 'without': 2}, {'checking': 3, 'without': 3, 'anything': 3}, {'checking': 60, 'without': 60, 'first': 60}, {'checking': 4, 'reviews': 4, 'without': 4}, {'checking': 4, 'without': 4, 'vacation': 4}, {'without': 4, 'reviewing': 4, 'first': 4}, {'consulting': 15, 'without': 15, 'first': 15}, {'without': 3, 'going': 3, 'first': 3}, {'looking': 5, 'without': 5, 'first': 5}, {'without': 5, 'plan': 5, 'first': 5}, {'using': 5, 'without': 5, 'first': 5}, {'hotel': 2, 'book': 2, 'without': 2}] 

<Cluster: 20, #Records: 1> [{'one': 4, 'apps': 4, 'first': 4}] 

<Cluster: Node42, #Records: 25> [{'go': 2, 'site': 2, 'first': 2}, {'go': 3, 'travel': 3, 'first': 3}, {'go': 3, 'always': 3, 'first': 3}, {'go': 12, 'place': 12, 'first': 12}, {'go': 3, 'planning': 3, 'first': 3}, {'go': 4, "it's": 4, 'first': 4}, {'go': 4, 'without': 4, 'first': 4}, {'planning': 4, 'stop': 4, 'first': 4}, {'always': 6, 'stop': 6, 'first': 6}, {'always': 3, 'first': 3, 'choice': 3}, {'check': 2, 'booking': 2, 'first': 2}, {'travel': 3, 'check': 3, 'first': 3}, {'always': 8, 'check': 8, 'first': 8}, {'place': 3, 'check': 3, 'first': 3}, {'hotels': 3, 'check': 3, 'first': 3}, {'attractions': 2, 'hotels': 2, 'first': 2}, {'time': 2, 'phoenix': 2, 'first': 2}, {'trying': 3, 'time': 3, 'first': 3}, {'time': 12, 'used': 12, 'first': 12}, {'using': 13, 'time': 13, 'first': 13}, {'use': 4, 'time': 4, 'first': 4}, {'time': 3, 'california': 3, 'first': 3}, {'time': 3, 'vacation': 3, 'first': 3}, {'place': 4, 'look': 4, 'first': 4}, {'time': 3, 'place': 3, 'first': 3}] 

<Cluster: 37, #Records: 1> [{'page': 3, 'back': 3, 'first': 3}] 


'''
```
