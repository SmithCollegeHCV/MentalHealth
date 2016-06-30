
# coding: utf-8

# In[1]:

import pandas


# In[16]:

topTen = pandas.read_excel("160629 Random Forest Data Variable Importance.xls", 
                           header = None,
                          keep_default_na = False)


# In[17]:

file = open("160630 Positions.txt", "w") 


# In[18]:

nforests = 20 
topPosition = 10 
for nth_time in range(nforests): 
    for number in range(1, topPosition+1, 1):
        string = str(number) + "\n"
        file.write(string)


# In[19]:

positions = pandas.read_csv("160630 Positions.txt", header = None)


# In[132]:

topTen[3] = positions


# In[133]:

print(topTen)


# In[161]:

#list of categories to append as the key values of the dictionary 
categoriesList = ['adl', 'apathy', 'attachment', 'attention','avoidance', 
                  'behavior', 'cogdev', 'communication', 'eating', 'memory', 
                  'delusion', 'detachment', 'feeling', 'hallucination', 'iho', 
                  'impulse', 'mood', 'motor', 'orientation', 'rigidity', 'risk', 
                  'ritual', 'self.concept', 'self.harm', 'sensory', 'sleep', 
                  'sexual', 'somatic', 'substance', 'thought'] 

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

for row in topTen.iterrows():
    category_name = row[1][0]
    category_pos = row[1][3]
    dict_value = posfreq_dict[category_name]
    dict_value[category_pos - 1] = dict_value[category_pos - 1] + 1
    #print(type(dict_value[category_pos - 1]))
    #if category_name == "adl": 
        #print(category_name, category_pos)
        #print(row)


# In[176]:

print(posfreq_dict)


# In[ ]:



