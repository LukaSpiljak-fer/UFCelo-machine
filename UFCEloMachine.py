import csv

class Fighter:
    def __init__(self, name, elo=1500):
        self.name = name
        self.elo = elo

def findFighter(fightersList, name):
    for fighter in fightersList:
        if fighter.name == name:
            return fighter
    return None

def calculateElo(ratWin, ratLoss):
    eWin = 1 / (1 + 10 ** ((ratLoss - ratWin) / 400))
    eLoss = 1 - eWin
    ratNewWin = ratWin + 32 * (1 - eWin)
    ratNewLoss = ratLoss + 32 * (0 - eLoss)
    return ratNewWin, ratNewLoss

fightersList = []
INITELO = 1500
KVALUE = 32


with open('allFightHistory.txt', 'r', encoding='utf-8', newline='') as csvFile:
    
    reader = csv.reader(csvFile)
    for row in reader:

        if row[0].startswith('N') or row[0].startswith('D'):
            continue

        fighter1 = findFighter(fightersList, row[1])
        fighter2 = findFighter(fightersList, row[2])

        if (fighter1== None and not fighter2 == None):
            fighter1 = Fighter(row[1], fighter2.elo)
        elif (not fighter1 == None and fighter2 == None):
            fighter2 = Fighter(row[2], fighter1.elo)
        elif (fighter1 == None and fighter2 == None):
            fighter1 = Fighter(row[1], INITELO)
            fighter2 = Fighter(row[2], INITELO)

        fighter1.elo, fighter2.elo = calculateElo(fighter1.elo, fighter2.elo)

        if fighter1 not in fightersList:
            fightersList.append(fighter1)

        if fighter2 not in fightersList:
            fightersList.append(fighter2)


with open('fighterElos.txt', 'w', encoding='utf-8', newline='') as elosFile:
    for fighter in fightersList:
        elosFile.write(fighter.name + "," + str(fighter.elo) + "\n")
