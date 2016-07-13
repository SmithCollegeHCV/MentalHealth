
# coding: utf-8

# In[ ]:

#Compiled merges all 3 programs: "DSM Redundancy Eliminator.py", "160603 Remove Or.py", & "160603 Duplicate Or.py" 
#Program Functionality 1: Eliminates redundancy in categories and chapters of the DSM-V 
#Program Functionality 2: Creates a .xls file of all the data with the "or's" and without the "or's" 
#Program the .xls file returned by program functionality 2 is supposed to be manually manipulated for collapse_pivot_code.R 


# In[3]:

#Import all necessary pacagkes 
import pandas as pd
import numpy as np


# In[4]:

def noRepeatChap(table, colname):
    '''function that takes in the table and the column name of the chapters to return a dataframe with no repeat chapters
    '''
    
    #extract column of chapters from the table 
    chapCol = table[colname]

    chap_df = pd.DataFrame( ) #create an empty dataframe 
    
    #iterate through each list of chapters in the column of chapters
    for chapList in chapCol: 
        chapList = unicode(chapList) #convert all the list format to unicode 
        
        if type(chapList) == unicode:  
            chapList = chapList.split(",") #split the chapterList by commas
            chapList = np.unique(chapList) #eliminate redundancy of chapters
            chapList_df = pd.DataFrame(chapList) #create a dataframe of the chapters 
         
        else: #if it is still not a unicode type, print out message 
            print('format not in unicode')
        
        #create a new dataframe with no repeat chapters 
        chap_df = chap_df.append(chapList_df, ignore_index = True) 
    
    chap_df.index +=1 #change the index so it corresponds to table index
    table[colname] = chap_df #reassign column of chapters of table with new, abridged version
    
    return table 


# In[5]:

def noRepeatCtg(table, colname):
    '''function that takes in the table and the column name of the categories to return a dataframe with no repeat categories
    '''
    
    #extract column of categories from the table 
    ctgCol = table[colname] 

    numrows = len(ctgCol.index) #numrows is the number of rows in the ctgCol/table 
    
    #iterate through by the number of rows 
    for num in range(numrows):
        ctgList = ctgCol.iloc[num] #ctgList is the list of categories indexed from the category colum
        ctgList = ctgList.split(",") #split the ctgList by commas 
        
        stripList = [] #stripList is a list of all the non-redundant ctgList 
        for ctg in ctgList: #iterate through each category in ctgList
            ctg = ctg.strip() #eliminate blank white spaces in each category 
            stripList.append(ctg) #append category to stripList
        stripList = np.unique(stripList) #remove all redundant ctgs in stripList
        ctgCol.iloc[num] = stripList #alter each list of categories with the non-redundant one 
    
    #return the altered table with no repeat categories
    return table 
    


# In[6]:

def delOr(table, colname):
    '''function that returns a dataframe and deletes all the ors indicated by / in the categories column
    '''
    ctgCol = table[colname] #extract the category column from the table 
    
    #iterate through the index of the loop and each list of categories in the ctgCol
    for idx, ctgList in enumerate(ctgCol):
        ctgList = str(ctgList) #convert ctgList into a string format 
        if "/" in ctgList: 
            tableidx = idx + 1 #table idx starts with 1, not 0 like idx 
            table = table.drop([tableidx]) #drop the row with the '/' in it 
    
    table = table.reset_index() #reset the index of the table
    table.index +=1 #shift the index of the table by one 
    table = table.drop('index', axis = 1) #drop the column 'index' in the table
    
    #return the table with no or's or '/'
    return table


# In[7]:

def extractOr(table, colname):
    '''function that returns a dataframe that returns a dataframe with only the ors 
    '''
    ctgCol = table[colname] #extract category column from the table 
    orList = [] #orList is a list of categories with no '/' 
    
    #iterate through the index of the loop and each list of categories in the ctgCol
    for idx, ctgList in enumerate(ctgCol): 
        ctgList = str(ctgList) #convert ctgList into a string format 
        if "/" in ctgList:
            tableidx = idx + 1 #table idx starts with 1, not 0 like idx 
            orRow = table.ix[tableidx] #name the row with the '/' in it orRow
            orList.append(orRow) #append orRow to orList
    
    orList_df = pd.DataFrame(orList) #create a dataframe of orList 
    orList_df = orList_df.reset_index()  #reset the index of the dataframe 
    orList_df.index +=1 #shift the index of the dataframe by one 
    orList_df = orList_df.drop('index', axis = 1) #drop the column 'index' in the dataframe
    
    #return a dataframe with only or's 
    return orList_df


# In[8]:

def writeToExcel(table, filename):
    '''function that writes a pandas.dataframe onto an .xls
    '''
    writer = pd.ExcelWriter(filename, engine='xlsxwriter') #define writer 
    table.to_excel(writer, sheet_name='Sheet1') #name the sheet 
    writer.save() #save excelsheet 


# In[10]:

def main():
    '''program that executes and writes files based on user input 
    '''
    
    errorMsg = "Name does not exist or incorrect naming. Please check name again. The name must be put in '' or string format in [example: 'filename' or 'name'] "
    #import files in .xls format 
    
    
    while True: #prevents user from re-running the programming because of incorrect format
        try:
            importFile = input('Name of the xls file to import: ') #must be put in '' or string format in .xls
            break 
        
        #return errorMsgs in these cases 
        except SyntaxError:
            print(errorMsg)
            
        except NameError:
            print(errorMsg)
            
        except IOError:
            print(errorMsg)
        
        except KeyError:
            print(errorMsg)
            
    #creates a data frame of the imported file 
    table = pd.read_excel(importFile)
    
    print(table.describe())
    
    while True: #prevents user from re-running the programming because of incorrect format
        try: 
            chapColName = input('Name of the column of the chapters (case-sensitive): ') #ask user input for the name of chapter columns
            break 
        
        #return errorMsgs in these cases 
        except SyntaxError:
            print(errorMsg)
            
        except NameError:
            print(errorMsg)
            
        except IOError:
            print(errorMsg)
            
        except KeyError: 
            print(errorMsg)
            
    table = noRepeatChap(table, chapColName) #delete repeats in chapters
    
    
    while True: #prevents user from re-running the programming because of incorrect format
        try:
            chapCtgName = input('Name of the column of the categories (case-sensitive): ') #ask user input for the name of category columns
            break 
        
        #return errorMsgs in these cases 
        except SyntaxError:
            print(errorMsg)
            
        except NameError:
            print(errorMsg)
            
        except IOError:
            print(errorMsg)
        
        except KeyError:
            print(errorMsg)
            
    table = noRepeatCtg(table, chapCtgName) #delete repeats in category column
    
    noOrTable = delOr(table, chapCtgName) #table with no or's
    orTable = extractOr(table, chapCtgName) #table with only or's
    
    while True: #prevents user from re-running the programming because of incorrect format
        try:
            orTable_write = input("Do you want to save the orTable in a xls? ['y'/'n']: ") #ask if user wants to save orTable
            break
        
        #return errorMsgs in these cases 
        except SyntaxError:
            print(errorMsg)
            
        except NameError:
            print(errorMsg)
            
        except IOError:
            print(errorMsg)
        
        except KeyError:
            print(errorMsg)
        
    while True: #prevents user from re-running the programming because of incorrect format
        try: #case in which user wants to save file
            orTable_write == 'y'
            orTablefilename = input('Filename for the orTable: ') #ask user input for file name
            writeToExcel(orTable, orTablefilename) #create excel file of orTable 
            print('orTable saved as', orTablefilename)
            break 
        
        #return errorMsgs in these cases 
        except SyntaxError:
            print(errorMsg)
            
        except NameError:
            print(errorMsg)
            
        except IOError:
            print(errorMsg)
        
        except KeyError:
            print(errorMsg)
        
        except: #case in which user does not want to save file
            orTable_write == 'n'
            print('orTable not saved')
            break
            
    
    while True: #prevents user from re-running the programming because of incorrect format
        try: 
            noOrTable_write = input("Do you want to save the noOrTable in a xls? ['y'/'n']: ")#ask if user wants to save noOrTable
            break
    
        #return errorMsgs in these cases 
        except SyntaxError:
            print(errorMsg)
            
        except NameError:
            print(errorMsg)
            
        except IOError:
            print(errorMsg)
        
        except KeyError:
            print(errorMsg)
        
    
    while True: #prevents user from re-running the programming because of incorrect format
        try: #case in which user wants to save file
            noOrTable_write == 'y'
            noOrTablefilename = input('Filename for the noOrTable: ' ) #ask user input for file name
            writeToExcel(noOrTable, 'No Ors.xlsx') #create excel file of noOrTable
            print('noOrTable saved as', noOrTablefilename)
            break 
    
        #return errorMsgs in these cases 
        except SyntaxError:
            print(errorMsg)
            
        except NameError:
            print(errorMsg)
            
        except IOError:
            print(errorMsg)
        
        except KeyError:
            print(errorMsg)
        
        except: #case in which user does not want to save file
            noOrTable_write == 'n'
            print('noOrTable not saved')
            break
       
main()
   
    


# In[ ]:



