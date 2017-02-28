import csv
from datetime import date,datetime,timedelta,time
import operator
import random
import sys


class GameEntry:
    date = ""
    homeTeam = ""
    awayTeam = ""

#####IMPLEMENT WEEKLY COUNT...
# 0-indexed start/end rows for data
firstDataRow = 1 # Row where the date headings are.  Data follows this row
teamNameColNum = 5
startWeeklyColNum = 19
endWeeklyColNum = 30 # Was 29

#inputFileName='PCSSL Teams - Matchups - 2016-02-27.csv'
inputFileName='Matchup-Input2.csv'

teamList = []
gameList = {}
gameCount = {}
homeCount = {}
awayCount = {}
with open(inputFileName, 'rb') as csvfile:
    myReader = csv.reader(csvfile, delimiter=',')
    rowNum = 0
    # Make one pass to collect all the names and the date list
    for row in myReader:
        teamName = ''
        if rowNum == firstDataRow:
            dateList = row
        if rowNum > firstDataRow:
            colNum = 0
            for item in row:
                if colNum == teamNameColNum and item != '':
                    teamName = item
                    teamList.append(item)
                    gameCount[teamName] = 0
                    gameList[teamName] = []
                    homeCount[teamName] = 0
                    awayCount[teamName] = 0
                if teamName != '' and colNum >= startWeeklyColNum and colNum <= endWeeklyColNum:
                    if (item != 'NO') and (item != 'BYE'):
                        gameCount[teamName] += 1
                        if (str(item) > str(teamName)):
                            game = GameEntry()
                            game.date = dateList[colNum]
                            game.homeTeam = teamName
                            game.awayTeam = item
                            gameList[teamName].append(game)
                colNum += 1
        rowNum += 1

print "Writing out file\n\n"
# Write it out
# TODO: Should probably name this file better    
with open('GameTable.csv', 'w') as outputFile:
    outputFile.write("Team Name,")
    for colNum in range(startWeeklyColNum, endWeeklyColNum + 1):
        outputFile.write(dateList[colNum] + ",")
        outputFile.write(dateList[colNum] + ",")
    outputFile.write("\n")
        
    for team in teamList:
#        print "Checking team " + team
        outputFile.write(team + ",")
        for colNum in range(startWeeklyColNum, endWeeklyColNum + 1):
            foundGame = False
            for game in gameList[team]:
                if game.date == dateList[colNum]:
                    homeTeam = game.homeTeam
                    awayTeam = game.awayTeam
                    # Randomly flip home and away, for balance
                    if (random.randint(1,1000000) > 500000):
                        homeTeam = game.awayTeam
                        awayTeam = game.homeTeam
                    outputFile.write(homeTeam + ",")
                    outputFile.write(awayTeam + ",")
                    if (homeTeam not in homeCount):
                        homeCount[homeTeam] = 0
                    if (awayTeam not in awayCount):
                        awayCount[awayTeam] = 0
                    homeCount[homeTeam] += 1
                    awayCount[awayTeam] += 1
#                    print homeTeam, str(homeCount[homeTeam]), str(awayCount[homeTeam]), str(";; ") , awayTeam, str(homeCount[awayTeam]), str(awayCount[awayTeam])
                    foundGame = True
            # Write in exra commas if needed
            if (foundGame == False):
                outputFile.write(",,")
        outputFile.write("\n")

    with open('checkFile.csv', 'w') as checkFile:
        checkFile.write("Team, # games, # home, # away\n")
        for team in teamList:        
            checkFile.write(team + "," + str(gameCount[team]) + "," \
                + str(homeCount[team]) + "," + str(awayCount[team]) + "\n")
            if (gameCount[team] != homeCount[team] + awayCount[team]):
                print "Need to check: Team " + team + " had " + str(gameCount[team]) + " games; " \
                    + str(homeCount[team]) + " home; " + str(awayCount[team]) + " away"
#                checkFile.write("Need to check: Team " + team + " had " + str(gameCount[team]) + " games; " \
#                    + str(homeCount[team]) + " home; " + str(awayCount[team]) + " away\n")

