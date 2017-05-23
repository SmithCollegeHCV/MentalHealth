
# coding: utf-8

# In[1]:

import pandas


# In[16]:

#read xls file that lists Random Forest Data Variable Importance
topTen = pandas.read_excel("160629 Random Forest Data Variable Importance.xls", 
                           header = None,
                          keep_default_na = False)


# In[17]:

#open Positions.txt file to write positions 
file = open("160630 Positions.txt", "w") 


# In[18]:

nforests = 20 #assign number of forests used 

topPosition = 10 #assign number of top Positions used 

#iterate to write a list of topPositions on Positions.txt
for nth_time in range(nforests): 
    for number in range(1, topPosition+1, 1):
        string = str(number) + "\n"
        file.write(string) #write the positions on the text file 


# In[19]:

#read Positions.txt file 
positions = pandas.read_csv("160630 Positions.txt", header = None)


# In[132]:

#add positions dataframe as third column in topTen dataframe
topTen[3] = positions


# In[133]:

#print(topTen)


# In[161]:

#list of categories to append as the key values of the dictionary 
categoriesList = ['adl', 'apathy', 'attachment', 'attention','avoidance', 
                  'behavior', 'cogdev', 'communication', 'eating', 'memory', 
                  'delusion', 'detachment', 'feeling', 'hallucination', 'iho', 
                  'impulse', 'mood', 'motor', 'orientation', 'rigidity', 'risk', 
                  'ritual', 'self.concept', 'self.harm', 'sensory', 'sleep', 
                  'sexual', 'somatic', 'substance', 'thought'] 

#length of categoryList 
categoryLength = len(categoriesList)


# In[162]:

#create list of zeroes for the dictionary
zeroList = []
for number in range(categoryLength):
    zeroList.append(0)


# In[174]:

#create a position frequency dictionary referenced by categories 
posfreq_dict = {}
for i in range(categoryLength):
    posfreq_dict[categoriesList[i]] = []
    for number in range(categoryLength):
        posfreq_dict[categoriesList[i]].append(0)
    
 


# In[175]:

#iterate through rows of the topTen dataframe 
for row in topTen.iterrows():
    category_name = row[1][0] #name of the category of the row 
    category_pos = row[1][3] #position of the category of the row 
    dict_value = posfreq_dict[category_name] #returns the value of the key "category_name"
    dict_value[category_pos - 1] = dict_value[category_pos - 1] + 1 #change the value of the key


# In[176]:

#print(posfreq_dict)


# In[ ]:



