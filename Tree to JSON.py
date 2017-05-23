
# coding: utf-8

# In[1]:

#import packages
from IPython.display import Image
from sklearn import tree, datasets, utils
from sklearn.externals.six import StringIO
from sklearn.tree import DecisionTreeClassifier, export_graphviz
import sklearn
import pandas
import numpy
import pydot 
import graphviz


# In[2]:

#ask for user input for imported pivot file from Isha's R program 
#pivotfile = input('Name of file you want to import: ') #input must be in ' ' 

pivotfile = '160720 Pivot.csv'


# In[3]:

#read in pivotfile in pandas dataframe format
rawdata = pandas.read_csv(pivotfile) 


# In[4]:

#put codes as Y in numpy array format 
Y = numpy.array(rawdata[[0]])  #must be in numpy array format 


# In[5]:

ctgHeader = list(rawdata.columns.values)[3:] #create a list of all the ctgs
#print(ctgHeader)


# In[6]:

#select the df of all the binary numbers from the raw data in bool format
X = numpy.array(rawdata[ctgHeader], dtype = bool)


# In[7]:

clf = tree.DecisionTreeClassifier()


# In[8]:

#fit the tree
clf = clf.fit(X, Y)


# In[9]:

#Asks user input for the name of the dotfile 
dotfilename = input('Name the dot file: ') #input must be in ' ' 


# In[15]:

#Create a dotfile of the tree
with open(dotfilename, 'w') as f:
    f = tree.export_graphviz(clf, out_file = f,
                            feature_names = ctgHeader, #must be a list 
                            class_names = rawdata['Code'] #must be in panda series,
                            )   


# In[12]:

dot_data = StringIO()


# In[13]:

#create the tree in graphviz
tree.export_graphviz(clf, out_file=dot_data, 
                     feature_names = ctgHeader, 
                     class_names = rawdata['Code'], 
                     filled = True, 
                     rounded = True,
                    leaves_parallel = True
                    #max_depth = 2) 
                     )
                     


# In[ ]:

graph = pydot.graph_from_dot_data(dot_data.getvalue()) 


# In[ ]:

#Ask user input for tree name in .svg 
svgtreename = input('Name of tree graph in .svg: ') #input must be in ' ' 


# In[15]:

#Create .svg of tree
Image(graph.write_svg(svgtreename)) 


# In[10]:

#import modules to convert dot file to JSON 
import json
import networkx
import pygraphviz
from networkx.readwrite import json_graph


# In[11]:

def dot_to_json(file_in, file_out, indent=1):
    '''function that converts dotfile into json 
    '''
    graph_dot  = pygraphviz.AGraph( file_in )
    graph_netx = networkx.nx_agraph.from_agraph( graph_dot )
    graph_json = json_graph.node_link_data( graph_netx )

    # fix formatting [graphviz to d3.js]
    for node in graph_json["nodes"]:
        # replace label by name
        node['name'] = node.pop('label')
        # id from string to integer
        node['id']   = int(node['id'])

    with open(file_out, 'w') as f:
        json.dump(graph_json, f, indent=indent)

    return 'succesfully operated'


# In[12]:

#ask user input for jsonfile name -- uncleaned version 
jsonfilename = input('Name uncleaned jsonfile: ') #input must be in ' ' 


# In[16]:

dot_to_json(dotfilename, jsonfilename)


# In[17]:

#read jsonfile in config dictionary format 
config = json.loads(open(jsonfilename).read()) 
#print(config.keys()) to show structure of config


# In[18]:

print(config)


# In[43]:

#Process to clean the JSON file 
nodesList = config["nodes"] #select the nodes of the tree graph
print(nodesList)


# In[44]:

#run through each dictionary or leaf in the nodesList 
for dictionary in nodesList:
    #split the dictionary  to return an list of uncleaned information 
    uncleaned = dictionary['name'].split("\\n") 
    
    #if category exists in the leaf
    if "<=" in uncleaned[0]:
        #create a newList of all the wanted information
        newList = uncleaned[0:3] #add category, nsamples, and criteria to newList 
        newList.append(uncleaned[-1]) #add codes to newList
        
        #create a two element list of symptoms, criteria, nsamples, dxclass 
        symptomList = newList[0].split("<=")
        criteriaList = newList[1].split("=")
        nsamplesList = newList[2].split("=")
        dxclassList = newList[3].split("=")
        codeChapList = dxclassList[1].split("_") #split the codes and the chapters
        
        #add the key 'criteria' and its values into dictionary
        dictionary['symptom'] = symptomList[0]
    
    #if category does not exist in the leaf 
    else:
        #create a newList of all the wanted information
        newList = uncleaned[0:2] #add nsamples and criteria to newList 
        newList.append(uncleaned[-1]) #add codes to newList
        
        #create a two element list of criteria, nsamples, dxclass 
        criteriaList = newList[0].split("=")
        nsamplesList = newList[1].split("=")
        dxclassList = newList[2].split("=")
        codeChapList = dxclassList[1].split("_") #split the codes and the chapters
    
    #add the keys for criteria, nsamples, dxclass, chapters and their values into dictionary
    dictionary['criteria'] = criteriaList[1]
    dictionary['nsamples'] = nsamplesList[1]
    dictionary['dx_class'] = codeChapList[0]
    dictionary['chapter'] = codeChapList[1] 
    
    #delete the key and value under "name" in the dictionary
    dictionary.pop("name", None) 


# In[45]:

print(config)


# In[46]:

#Ask user input for name of cleaned json file
jsoncleaned = input('Name cleaned json file: ') #input must be in ' ' 


# In[47]:

#Create json file with cleaned information 
with open(jsoncleaned, 'w') as outfile:
    json.dump(config, outfile)


# In[ ]:



