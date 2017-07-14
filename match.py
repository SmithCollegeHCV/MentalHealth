#Matches each DSM code to its corresponding diagnosis name
#Kelly Pien

import csv
import codecs

def main():
    #open and read file with diagnosis codes and corresponding names
    with codecs.open('7clusters_withNames.csv', 'r', encoding='utf-8', errors='ignore') as dataFile:
        informationRead = csv.reader(dataFile)
        #create dictionary of name code pairs
        d = {}
        for row in informationRead:
            d[row[0]] = row[2]
        
    #open and read csv containing codes and cluster numbers
    with codecs.open('12clusters.csv', 'r', encoding='utf-8', errors='ignore') as clustersFile:
        clustersRead = csv.reader(clustersFile)
        of = csv.writer(open('12clusters_withNames.csv', 'w'))
        #write headers to output file
        of.writerow(['code', 'cluster', 'diagnosis'])
        #match codes to names
        for row in clustersRead:
            for k in d:
                if k == row[0]:
                    row.append(d[k])
            #write all data to csv
            of.writerow(row)
    
main()
