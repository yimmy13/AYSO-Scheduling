import operator
from datetime import date,datetime,timedelta,time
import sys
import csv

class TeamEntry:
    myTeamName = ""
    teamID = ""
    division = ""
    homeCount = 0
    awayCount = 0

class FieldInfo:
    fieldName = ""
    startTime = ""
    # MSL uses duration instead of end time (like WYS)
    duration = ""


class GameEntry:
    fieldInfo = FieldInfo()
    date = ""
    homeTeam = ""
    awayTeam = ""

teamMap = {}
teamList = []
# Import team name to MSL ID info:
with open('TeamList.csv', 'rb') as csvTeamFile:
    myReader = csv.reader(csvTeamFile, delimiter=',')
    for row in myReader:
        teamEntry = TeamEntry()
        if len(row) >= 2:
            teamEntry.myTeamName = row[1]
            teamEntry.teamID = row[0]
            teamEntry.division = row[2]
            teamMap[row[1]] = teamEntry
            teamList.append(row[1])
    print "Read " + str(len(teamMap)) + " rows of teams"

# 0-indexed start/end rows for data
firstDataRow = 2
lastDataRow = 1000
fieldColNum = 2
startTimeColNum = 6 # Was 3
durationColNum = 7
#endTimeColNum = 2 # Was 4
startWeeklyColNum = 8 # Was 7
endWeeklyColNum = 30 # Was 29

inputFileName='MSL-Input.csv'

# Header file looks something like this...
#							3/6/2016	3/6/2016,,,,,,,,3/6/2016,3/6/2016,3/13/2016,3/13/2016,3/20/2016,3/20/2016,3/27/2016,3/27/2016,4/3/2016,4/3/2016,4/10/2016,4/10/2016,4/17/2016,4/17/2016,4/24/2016,4/24/2016,5/1/2016,5/1/2016,5/8/2016,5/8/2016,5/15/2016,5/15/2016,5/22/2016,5/22/2016
#Area,Region,Field,Division,Type,Order,Start Time,Duration,1,Away,2,Away,3,Away,4,Away,5,Away,6,Away,7,Away,8,Away,9,Away,10,Away,11,Away,12,Away

with open(inputFileName, 'rb') as csvfile:
    myReader = csv.reader(csvfile, delimiter=',')
    dateList = []
    dateMap = {}
    gameList = []
    rowNum = 0
    hasGameList = {}
    for row in myReader:
        fieldInfo = FieldInfo()
        colNum = 0
        for item in row:
            # Pull the field, start & end times from the beginning of the row
            if (rowNum >= firstDataRow):
                # Get field name
                if (colNum == fieldColNum):
                    fieldInfo.fieldName = item
                # Get start time
                if (colNum == startTimeColNum):
                    fieldInfo.startTime = item
                # Get duration
                if (colNum == durationColNum):
                    fieldInfo.duration = item

            if (colNum >= startWeeklyColNum and colNum <=endWeeklyColNum):
                # In the first row, this is where we pull dates 
                # and make map to week number
                if (rowNum == 0 and colNum % 2 == 0):
                    dateList.append(row[colNum + 1])
                    dateMap[colNum] = row[colNum + 1]
                    hasGameList[row[colNum + 1]] = []

                # In the data rows, pull the game entries
                if (rowNum >= firstDataRow and rowNum <= lastDataRow):
                    if (colNum % 2 == 0):
                        if (row[colNum] != ''):
                            gameEntry = GameEntry()
                            gameEntry.division = teamMap[row[colNum]].division
                            gameEntry.fieldInfo = fieldInfo
                            gameEntry.date = dateMap[colNum]
                            gameEntry.homeTeam = row[colNum]
                            gameEntry.awayTeam = row[colNum + 1]
                            teamMap[gameEntry.homeTeam].homeCount += 1
                            teamMap[gameEntry.awayTeam].awayCount += 1
                            gameList.append(gameEntry)
                            
                            print gameEntry.homeTeam + ", "+ gameEntry.awayTeam + ", " + gameEntry.date
                            hasGameList[gameEntry.date].append(gameEntry.homeTeam)
                            hasGameList[gameEntry.date].append(gameEntry.awayTeam)
            colNum += 1
        rowNum += 1

# Write it out
# TODO: Should probably name this file better    
#with open('PCSSL-2016-Schedule-'+fileDate+'.tsv', 'w') as outputFile:
with open('PCSSL-2016-Schedule.tsv', 'w') as outputFile:
    for date in dateList:
        if (date is '3/6/2016'):
            pass
        fileDate = date
        fileDate = fileDate.replace('/','-')
        for game in gameList:
            if (date is game.date):
                outputFile.write("game\t")
                outputFile.write(teamMap[game.homeTeam].division + "\t")
                outputFile.write(game.date + "\t")
                outputFile.write(teamMap[game.homeTeam].teamID + "\t")
                outputFile.write(teamMap[game.awayTeam].teamID + "\t")
                outputFile.write(game.fieldInfo.startTime + "\t")
                outputFile.write(game.fieldInfo.duration + "\t")
                outputFile.write(game.fieldInfo.fieldName + "\t")
                outputFile.write("\n")

        byeCount = 0
        for team in teamList:
            if team not in hasGameList[date]:
                print team + ", " + date + ": no games"
                outputFile.write("bye\t")
                outputFile.write(teamMap[team].division + "\t")
                outputFile.write(date + "\t")
                outputFile.write(teamMap[team].teamID + "\n")
                byeCount += 1
        print "For " + date + ", " + str(byeCount) + " byes"
                
print "\n\nStats:"
for team in teamMap:
    print str(team) + ", " + str(teamMap[team].homeCount) + ", home, " + str(teamMap[team].awayCount) + ", away games"

print "Num games scheduled is " + str(len(gameList))
