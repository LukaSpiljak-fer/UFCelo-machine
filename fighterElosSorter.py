import csv

with open("fighterElos.txt", 'r', encoding='utf-8', newline='') as csvFile:
    reader = csv.reader(csvFile)
    data = list(reader)

sorted_data = reversed(sorted(data, key=lambda row: float(row[1])))

with open("fighterElosSorted.txt", 'w', encoding='utf-8', newline='') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerows(sorted_data)