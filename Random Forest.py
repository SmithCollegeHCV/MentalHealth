
# coding: utf-8

# In[ ]:

import sklearn
from sklearn.ensemble import RandomForestClassifier
import pandas
import numpy


# In[ ]:

#ask for user input for imported pivot file from Isha's R program 
pivotfile = input('Name of file you want to import: ') #input must be in ' ' 


# In[ ]:

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

number_of_forests = 40


# In[ ]:

date = input('Enter date: ')


# In[8]:


file_name = str(date) + " Random Forest Data Variable Importance " + str(number_of_forests) + ".txt"
file = open(file_name, "w")
print(file_name)


# In[15]:

#types of models
bagged_model = RandomForestClassifier(n_estimators = 207, 
                             max_features = "auto")

 
# Loop over 5, 10, 15, 20, 25, 30
# Open new file for writing
    
for nth_model in range(1, number_of_forests + 1):
    rf_sqrt_model = RandomForestClassifier(n_estimators = nth_model,
                                                      max_features = "sqrt") 
    
    rf_sqrt_model = rf_sqrt_model.fit(X, rawdata['Code'])
    df = pandas.DataFrame(rf_sqrt_model.feature_importances_, ctgHeader) 
    df = df.sort_values(by = 0, ascending = False)
    #df_top10 = df.sort_values(by = 0, ascending = False).iloc[:10, 0]
    
    file.write(str(df) + "\n")
    
    print(df)
# Close file

    #print("#trees=", nth_model)
    #print(df_top10)
    #print(df)
    #print()
#rf_sqrt_model_500  = RandomForestClassifier(n_estimators = 500, 
                #             max_features = "sqrt")

#rf_sqrt_model_1000  = RandomForestClassifier(n_estimators = 1000, 
                   #          max_features = "sqrt")


# In[17]:

#fitting models
bagged_model = bagged_model.fit(X, rawdata['Code'])
#rf_sqrt_model_500 = rf_sqrt_model_500.fit(X, rawdata['Code'])
#rf_sqrt_model_1000 = rf_sqrt_model_1000.fit(X, rawdata['Code'])


# In[112]:

#making of generic data frame
df = pandas.DataFrame(rf_sqrt_model.feature_importances_, ctgHeader)

#data frame with values sorted in ascending order
df = df.sort_values(by = 0, ascending = False)


# In[113]:

df[2] = rf_sqrt_model_500.feature_importances_
print(df)


# In[114]:

df.sort_values(by = 2, ascending = False).iloc[:10,1]


# In[ ]:

df.sort_values(by = 0, ascending = False).iloc[:10,0]
 


# In[98]:

#i_tree = 0 
#for tree_in_forest in clf.estimators_: 
    #dot_data = StringIO()
   # tree.export_graphviz(tree_in_forest, out_file = dot_data)
  #  graph = pydot.graph_from_dot_data(dot_data.getvalue())
  #  f_name = 'tree_' + str(i_tree) + '.svg'
  #  Image(graph.write_svg(f_name))
  #  i_tree += 1


# In[ ]:



