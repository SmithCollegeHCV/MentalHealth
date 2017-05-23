
# coding: utf-8

# In[1]:

import sklearn
from sklearn.ensemble import RandomForestClassifier
import pandas
import numpy
import copy
import matplotlib.pyplot as plt
import seaborn as sns 


# In[2]:

def heatmap(dictionary, ntrees, date, n_features):
    '''function that makes a heatmap from a dictionary and saves it as a .png depending on ntrees and image_num
    '''
    
    #creates dataframe of the dictionary 
    heatmap_df = pandas.DataFrame.from_dict(dictionary, orient = 'index')
    
    #creates the heatmap 
    heatmap = sns.heatmap(heatmap_df,
                     vmin = 0) 
    
    #sets orientation of labels 
    for item in heatmap.get_yticklabels():
        item.set_rotation(0)
    
    #creates labels of axes of heatmap
    plt.ylabel('Category')
    plt.xlabel('Position')
    title = str(n_features) + " Features" + str(ntrees) + " Trees" 
    plt.title(title)
    #plt.show(heatmap)
    
    heatmap_file = str(date) + " HeatMap by features " + " trees:" + str(ntrees) + " features:" + str(n_features) + ".png"
    plt.savefig(heatmap_file, bbox_inches = 'tight')
    plt.close()


# In[3]:

def posfreqDict():
    '''function that creates and returns position frequency dictionary 
    '''
    
    categoriesList = ['adl', 'apathy', 'attachment', 'attention','avoidance', 
                  'behavior', 'cogdev', 'communication', 'concentration', 'eating', 'memory', 
                  'delusion', 'detachment', 'duration', 'feeling', 'hallucination', 'iho', 
                  'impulse', 'mood', 'motor', 'orientation', 'onset', 'prereq', 'rigidity', 'risk', 
                  'ritual', 'self.concept', 'self.harm', 'sensory', 'sleep', 
                  'sexual', 'somatic', 'substance', 'thought'] 
    
    
    categoryLength = len(categoriesList) #length of categoriesList
    
    #creating position frequency dictionary 
    posfreq_dict = {} #position frequency dictionary 
    for i in range(categoryLength):
        posfreq_dict[categoriesList[i]] = []
        for number in range(categoryLength):
            posfreq_dict[categoriesList[i]].append(0)
                
    return posfreq_dict


# In[4]:

def posfreqDictValues(): 
    '''function that updates the values of the position frequency dictionary 
    '''
    for row in topTen.iterrows():
        category_name = row[1][0] #name of the category of the row 
        category_pos = int(row[1][3]) #position of the category of the row 
        dict_value = posfreq_dict[category_name] #returns the value of the key "category_name"
        dict_value[category_pos - 1] = dict_value[category_pos - 1] + 1 #change the value of the key
    


# In[5]:

def posrateDict(posfreq_dict, ntrees):
    '''function that creates and returns position rate dictionary 
    '''
    #make a clone of the position frequency dictionary 
    posrate_dict = (copy.deepcopy(posfreq_dict)) 
    
    #iterate through a loop to create they values of the posrate_dict
    for category in posrate_dict:
        category_value = posrate_dict[category]
        for nth_value in range(len(category_value)): 
            category_value[nth_value] = (float(category_value[nth_value])/ntrees)

    
    return posrate_dict 


# In[6]:

def posDataframe(topPosition): 
    '''creating a position data frame to add to tree data frame, depending on topPosition value
    '''
    posList = []
    for i in range(1, topPosition +1, 1):
        posList.append(i)
        pos_df = pandas.DataFrame(posList)
        
    return(pos_df)


# In[7]:

def updateValues(posfreq_dict, tree_df):
    """ updating values of the dictionary by incrementing by 1's for a position
    each time a cateogry appears in that position 
    """
    for row in tree_df.iterrows():
        category_name = row[1][0] #name of the category of the row 
        category_pos = int(row[1][2]) #position of the category of the row 
        dict_value = posfreq_dict[category_name] #returns the value of the key "category_name"
        value_pos = category_pos -1 #position of value: needs to subtract 1 becuase index starts from 0 
        dict_value[value_pos] = dict_value[value_pos] + 1 #change value by adding 1 
        
    return posfreq_dict #new, updated posfreq_dict


# In[8]:

def treeDataframe(tree, binaries, pos_df):
    '''function that returns a tree dataframe with categories, feature importances, and position 
    '''
    
    #creates a dataframe of feature importance and categories
    tree_df = pandas.DataFrame(tree.feature_importances_, binaries.columns.values) 
    tree_df = tree_df.sort_values(by = 0, ascending = False) #sorting the dataframe values by feature importance
    tree_df.reset_index(level = 0, inplace = True) #convert the 'index' of categories to column in dataframe
    tree_df['Positions'] = pos_df #set third column as positions 
    tree_df.columns = ['Categories', 'Feature Importances', 'Positions'] #name each column
    
    return tree_df 


# In[11]:

def main():   
    #pivotfile = input('Name of file you want to import: ') #input must be in ' ' 

    pivotfile = '160720 Pivot.csv'
    rawdata = pandas.read_csv(pivotfile) 
    
   #put codes as Y in numpy array format 
    Y = numpy.array(rawdata[[0]])  #must be in numpy array format 
    ctgHeader = list(rawdata.columns.values)[4:] #create a list of all the ctgs
    
    #select the df of all the binary numbers from the raw data in bool format
    X = numpy.array(rawdata[ctgHeader], dtype = bool)
    
    ntrees = input("Enter # of Trees: ")
    date = input('Enter date: ')
    numFeatures = input('Enter the max # of Features: ')
    for n_features in range(1, numFeatures +1 ):
    
        #building RandomForest 
        rf_sqrt_model = RandomForestClassifier(n_estimators = ntrees,
                                                  max_features = n_features) 
        rf_sqrt_model = rf_sqrt_model.fit(X, rawdata[[0]])
        
        #create the position dataframe 
        topPosition = 33
        pos_df = posDataframe(topPosition)
        
        #creates an position frequency dictionary with only the keys
        posfreq_dict = posfreqDict()
        
        for tree in rf_sqrt_model: 
            #creates a tree data frame 
            tree_df = treeDataframe(tree, rawdata[ctgHeader], pos_df)
    
            #the values of posfreq_dict is updated with corresponding frequency 
            posfreq_dict = updateValues(posfreq_dict, tree_df)
            
        #creates a position rate dictionary 
        posrate_dict = posrateDict(posfreq_dict, ntrees)
        
        print('Creating Heat Maps...')
        heatmap(posrate_dict, ntrees, date, n_features)
        
        print('Program Completed')

main()


# In[ ]:



