import operator
from datetime import date,datetime,timedelta,time
import sys
import csv

class TeamEntry:
    myTeamName = ""
    TeamID = ""
    numGamesByDate = {}

class FieldInfo:
    fieldName = ""
    startTime = ""
    endTime = ""


class GameEntry:
    fieldInfo = FieldInfo()
    date = ""
    homeTeam = ""
    awayTeam = ""

SeasonHeader = 'Seasons: 4644 4684 4646 4647 4648 4744'
ColumnHeader = 'Week	Start	End	Field	Home	Away'
# 0-indexed start/end rows for data
firstDataRow = 2
lastDataRow = 9
fieldColNum = 0
startTimeColNum = 1 # Was 3
endTimeColNum = 2 # Was 4
startWeeklyColNum = 3 # Was 7
endWeeklyColNum = 23 # Was 29

inputFileName='Input.csv'

with open(inputFileName, 'rb') as csvfile:
    myReader = csv.reader(csvfile, delimiter=',')
    dateList = []
    dateMap = {}
    gameList = []
    rowNum = 0
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
                # Get start time
                if (colNum == endTimeColNum):
                    fieldInfo.endTime = item

            if (colNum >= startWeeklyColNum and colNum <=endWeeklyColNum):
                # In the first row, this is where we pull dates 
                # and make map to week number
                if (rowNum == 0 and colNum % 2 == 1):
                    dateList.append(row[colNum + 1])
                    dateMap[colNum] = row[colNum + 1]

                # In the data rows, pull the game entries
                if (rowNum >= firstDataRow and rowNum <= lastDataRow):
                    if (colNum % 2 == 1):
                        if (row[colNum] != ''):
                            gameEntry = GameEntry()
                            gameEntry.fieldInfo = fieldInfo
                            gameEntry.date = dateMap[colNum]
                            gameEntry.homeTeam = row[colNum]
                            gameEntry.awayTeam = row[colNum + 1]
                            gameList.append(gameEntry)

            colNum += 1
        rowNum += 1

# Write it out
# TODO: Should probably name this file better    
with open('Schedule.tsv', 'w') as outputFile:
    outputFile.write(SeasonHeader + "\n")
    outputFile.write(ColumnHeader + "\n")
    for game in gameList:
        outputFile.write(game.date + "\t")
        outputFile.write(game.fieldInfo.startTime + "\t")
        outputFile.write(game.fieldInfo.endTime + "\t")
        outputFile.write(game.fieldInfo.fieldName + "\t")
        outputFile.write(game.homeTeam + "\t")
        outputFile.write(game.awayTeam + "\t")
        outputFile.write("\n")

print "Num games scheduled is " + str(len(gameList))

