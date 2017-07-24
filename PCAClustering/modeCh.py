import csv
from collections import Counter
from operator import itemgetter


def main():
    file = open("20clusters30PCs_v2_withNames.csv", "r")
    read = csv.reader(file)
    clusters = []
    for row in read:
        clusters.append(row)
    clusters = clusters[1:]

    for miniList in clusters:
        miniList[1] = int(miniList[1])

    num_single_ch_clusters = 0
    
    for i in range(1,21):
        temp_lst = []
        for line in clusters:
            if line[1] == i:
                temp_lst.append(line)
        chap_lst = []
        for dx in temp_lst:
            chap_lst.append(dx[3])
        data = Counter(chap_lst)
        #print(data.most_common())
        #data.most_common()[0]
        if len(data.most_common()) == 1:
            num_single_ch_clusters += 1
    print(num_single_ch_clusters)

    #clusters = sorted(clusters, key = itemgetter(1))

    file.close()

main()
