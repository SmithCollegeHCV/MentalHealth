#import requests
from bs4 import BeautifulSoup
#import pandas
from html.parser import HTMLParser

def main():
	of = open("icd_data.csv", "w")
	soup = BeautifulSoup(open("icd_bluebook.html"), "html.parser")
	#print(soup.prettify())
	names_codes_list = soup.find_all("p", {"class" : "p26"})
	for diagnosis in names_codes_list:
		stringified = str(diagnosis).split('<span class="s1">')[1].split('</b>)')[0].split('</span>')[0]
		if "<b>" in stringified:
                        stringified = stringified.split("<b>")[1]
                        if "</b>" in stringified:
                                stringified = stringified.split("</b>")[0]
		of.write(stringified + "\n")

main()
