################################################################################

# Web Scraper for DSM5
# Zainab Aqdas Rizvi
# Code adapted from Ji Won Chung's parser

################################################################################

from bs4 import BeautifulSoup
import requests

def tagCheck(tag):
    contents = tag.findAll("p", {"class":"APP-Para"})
    if contents == None:
        return False
    else:
        return True

def cleanText(tag):
        tagcodeList = tag.findAll("p", {"class":"APP-Para"})
        codeList = []
        for code in tagcodeList:
            code = code.get_text(" ",strip=True)
            codeList.append(code)

        return codeList

def codeCheck(criteria):
    existence = criteria.findAll("span", {"class": "ICD10Code"})
    if existence == None:
        returnFalse
    else:
        returnTrue

def parse(soup, chapter, file):
    tagList = soup.findAll("div", {"class":"APP-CultureRelatedDiagnosticIssues"})

    for tag in tagList:
        if tagCheck(tag) == True:
            cleanCodes = cleanText(tag);

        file.write(chapter + " | " + str(cleanCodes)[1:-1] + "\n")

def main():
    file = open("CultureRelatedDiaognosticIssues.txt", "w")

    address = "http://dsm.psychiatryonline.org/doi/10.1176/appi.books.9780890425596.dsm"

    for number in range(1, 21):
        if 10 > number >= 1:
            chapterNum = str(number)
            link = address + "0" + chapterNum


        if number >= 10:
            chapterNum = str(number)
            link = address + chapterNum

        chapter = "Chapter: " + str(number)
        html = requests.get(link)
        html = html.text
        soup = BeautifulSoup(html, "html5lib")

        parse(soup, str(number), file)

    file.close()

    print('Parsing Complete!')

main()
