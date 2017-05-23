
# coding: utf-8

# In[ ]:

#################################################################################################

#DSM-V Web Scraping Concise
#Ji Won Chung 2016 HCV Summer Lab

#-----------------------------------------------------------------------------------------------#

#Started: 160518
#Last Updated: 160523
#http://dsm.psychiatryonline.org/doi/10.1176/appi.books.9780890425596.dsm02

#################################################################################################


# In[ ]:

#from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests


# In[ ]:

def codeCheck(criteria):
    '''function that checks if code exists
    '''

    #look for all those classes = ICD10Code in criteria
    existence = criteria.findAll("span", {"class": "ICD10Code"})

    #return False, if code does not exist in criteria
    if existence == None:
        return(False)

    #return True, if code exists in criteria
    else:
        return(True)
        


# In[ ]:

def codeList(criteria):
    '''function that returns a list of codes in the same diagnoses
    '''

    #find all list of codes in tags
    tagcodeList = criteria.findAll("span", {"class": "ICD10Code"})

    #extract codes from tags 
    codeList = [] 
    for code in tagcodeList:
        code = code.get_text()
        codeList.append(code)

    #return list of codes with no tags
    return codeList
    


# In[ ]:

def tableCheck(criteria):
    '''function that checks if a table exists 
    '''

    #list of all tables in criteria 
    locateTableList = criteria.findAll("table", {"class": "APP-tgroup"})

    #tables don't exist
    if locateTableList == "[]" or None:
        return False

    #tables do exist
    else:
        return True 


# In[ ]:

def tableList(criteria):
    '''function that tries to write the information of the table
    '''

    #list of all tables in criteria
    locateTableList = criteria.findAll("div", {"class" : "APP-CodeNote"})

    #go through each table in the list of all tables in criteria
    for locatedTable in locateTableList:

        #find the specific table
        tableFound =  locatedTable.find("table", {"class": "APP-tgroup"})

        #case where there is a table 
        if tableFound != None:
            print('table found')
            print('############################################################################')
            tableList = locatedTable.findAll("td", {"class" : "center Center"})

            #try to extract all codes from the table 
            allCodeList = []
            for tagCode in tableList:
                textCode = tagCode.get_text()
                allCodeList.append(textCode) 

            lengthCodeList = len(allCodeList)
            print(lengthCodeList)

            codeList = []
            for position in range(lengthCodeList):
                code = allCodeList[position]
                if position%4 != 0:
                    codeList.append(code)

           #go through each code
                    # put it in a sublist
                    #for each sublist add the symptoms
                    #and then append the sublist in a gigantic list with the diagnoses 
            


# In[ ]:

def symptomsList(criteria):
    '''function that returns a list of symptoms of each diagnoses
    '''

    #find symptoms in criteria with "ol" tag
    symptomsChunk = criteria.find("ol")

    #if symptoms exist with "ol" tag, find those in "li" tag
    if symptomsChunk != None:
        body = symptomsChunk.findAll('li') #encounters problem when "ol" does not exist

        #go through each symptom in the body of symptoms 
        symptomsList = []
        for symptoms in body:
            #return a list of symptoms with tags 
            tagSymptomsList = symptoms.findAll("p", {"class" : "APP-Para FirstLineIndent CellChangeDefaultSize "})
            
            #for each symptom in the list of symptoms, delete tag, and group in a List, if they're from the same diagnoses 
            for tagSymptoms in tagSymptomsList:
                textSymptomsSublist = []
                symptoms = tagSymptoms.get_text()
                textSymptomsSublist.append(symptoms)

                #only add new symptoms if they are not already in the list
                if symptoms not in symptomsList: 
                    symptomsList.append(textSymptomsSublist)

        return symptomsList
                
               
    #if symptoms do not exist with "ol" tag, but exist in "p" tag
    else:
        symptomsList = [] 
        body = criteria.find("p", {"class" :"APP-Para FirstLineIndent CellChangeDefaultSize "} ) #problems getting text 
        body = body.get_text() #delete tag, extract text of symptoms
        symptomsList.append(body)
        
        return symptomsList
     
##def findDiagnoses(criteria):
##    diagnosesTagList = criteria.findAll("h2", {"class" : "sectionHeader"})
##    print(diagnosesTagList)
##    
##    #return diagnoses
##


# In[ ]:

def program(soup, chapter, file):
    '''function that writes on the file the symptoms and the corresponding codes and chapter found in the DSM-V
    '''
    
    #return a list of all the info of the symptoms of diagnoses
    criteriaList = soup.findAll("div", {"class":"APP-CriteriaSet"}) #basically entire text
    

    #forloop each criteria in list of criterias
    for criteria in criteriaList:
 

        #if code exists in that criteria write info on .txt file 
        if codeCheck(criteria) == True:

            #return list of codes and symptoms 
            codesUncleaned = codeList(criteria)  
            symptoms = symptomsList(criteria)
 
            
            codes = []
            for code in codesUncleaned: 
                code = code.encode('ascii', 'ignore')
                codes.append(code)
                
            #go through each symptom in the list of symptoms
            Set = set()
        
            
            for symptom in symptoms:
                
                #for those cases where symptoms is a list of sublists
                if isinstance(symptom, list):
                    for element in symptom:                        
                        string = str(codes) + "|" + chapter + "|" + str(element.encode('ascii', 'ignore')) + "\n"

                else:
                    
                    string = str(codes) + "|" + chapter + "|" + str(symptom.encode('ascii', 'ignore')) + "\n"


                #account for those cases where symptoms is just one list  
##                if type(symptom) != 'list':
##                    string = str(codes) + "|" + chapter + "|" + str(str(symptoms).encode('ascii', 'ignore')) + "\n"

                #add in set to make sure no repeats
                Set.add(string)
            for element in Set:
                file.write(element)
                    


# In[2]:

################################################################################################################################################################

def main():
    '''function that goes through each chapter of DSM-V and runs the program
    '''

    #open the text file for the list of DSM-V symptoms 
    file = open("160720 DSM-V Categorized by Symptoms.txt", "w")

    #address of the DSM-V website
    address = "http://dsm.psychiatryonline.org/doi/10.1176/appi.books.9780890425596.dsm"
     
    #go through a loop of all the chapters, basing off the DSM-V address
    for number in range(1, 21):
        if 10 > number >= 1:
##            print(" Chapter:", number)
##            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            chapterNum = str(number)
            link = address + "0" + chapterNum
            

        if number >= 10:
##            print("Chapter:", number)
##            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            chapterNum = str(number)
            link = address + chapterNum

        #chapter of the DSM-V 
        chapter = "Chapter: " + str(number)

        #convert information from the website to soup 
        html = requests.get(link)
        html = html.text
        soup = BeautifulSoup(html)

        #run the program
        program(soup, chapter, file)

    #close the file
    file.close()
        
    print('Program Completed')
 



# In[ ]:

main()

