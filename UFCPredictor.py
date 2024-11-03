import csv
import math

def findFighterElo(fightersList, name):
    for fighter in fightersList:
        if fighter[0].upper() == name.upper():
            return fighter[1]
    return 0

with open("fighterElos.txt", 'r', encoding='utf-8', newline='') as csvFile:
    reader = csv.reader(csvFile)
    fightersList = list(reader)

while True:
    
    try:
        name1, name2 = input("format: ime1, ime2\n").split(", ")
    except:
        print("invalid input")
        continue

    fighter1Elo = findFighterElo(fightersList, name1)
    fighter2Elo = findFighterElo(fightersList, name2)

    if(fighter1Elo == 0 or fighter2Elo == 0):
        print("One or both fighters don't exist")
        continue

    fighter1WinChance = (1 / (1 + math.pow(10, ((float(fighter2Elo) - float(fighter1Elo)) / 400))))*100

    if(fighter1WinChance >= 50):
        print(name1 + " Wins " + str(round(fighter1WinChance)) + "%\n")
    else:
        print(name2 + " Wins " + str(round(100-fighter1WinChance)) + "%\n")


