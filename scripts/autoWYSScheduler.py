import operator
from datetime import date,datetime,timedelta,time
import sys
import itertools

# Initialize default team names.  Can be overridden in config
#execfile('Config-U6G.py')
execfile('Config-U12BD.py')

if len(teamNames) == 0:
    # build a team name given the index number
    for teamNum in range(numTeams):
        teamNames.append(region+'-'+age+gender+'-'+str(firstTeamNum+teamNum))

#Handle odd number of teams...
if len(teamNames) % 2 == 1:
    teamNames.append('BYE')

# Set numTeams here, even if it was initialized elsewhere
numTeams = len(teamNames)

## Set the output filenames based on the info we have
outputFileBaseName='Schedule-' + region + '-' + age + gender + '-' + str(date.today())
## This is the main output file, for uploading to WYS
outputFileName = outputFileBaseName + '.tsv'
## This is to import into Excel and get a snapshot.  Also includes
## home/away counts
outputWeekByWeekFileName = outputFileBaseName + '-weekbyweek.csv'

#iterate over fields, then time slots
numGamesPerWeek = (numTeams/2)
numTimeSlots= (numGamesPerWeek+1) / len(fieldNames)

if (autoTimeSlot):
    #build a list of time slots
    timeSlots=[]
    ts=timeSlotStart
    for t in range(numTimeSlots):
        timeSlots.append(ts)
        ts=(datetime.combine(date.today(),ts)+timedelta(minutes=gameLength)).time()
else: #convert the input time strings to time objects
    tts=[]
    for t in timeSlots:
        tts.append((datetime.strptime( t,'%H:%M')).time())
    timeSlots=tts

#for t in timeSlots:
#    print t.strftime('%H:%M')

#build a list of field+time slots
fieldTimes=[]
for r in itertools.product(timeSlots,fieldNames): fieldTimes.append(r)

teams = range(numTeams)

# Initialize the weeklyMap (it will contain the list of games for each week)
weeklyMap = {}
for j in range(0,numTeams):
    weeklyMap[j] = []
# And initialize the home/away counts
homeCount = [0] * numTeams
awayCount = [0] * numTeams

for j in range(0, len(teams)-1):
    for i in range (j+1,len(teams)):
        weekNum = ((i + j - 1) % (numTeams -1))
        if (weekNum == j - 1):
            weekNum = ((j + j - 1) % (numTeams -1)) 

        homeTeam = i
        awayTeam = j
        # Flip home away every other week, to give better balance to home/away
        if(weekNum%2==0):
            homeTeam = j
            awayTeam = i

        weeklyMap[weekNum].append([teams[homeTeam],teams[awayTeam]])
        homeCount[homeTeam] += 1
        awayCount[awayTeam] += 1

## If we haven't manually specified home/away, do it auto here
## If we have fewer teams than weeks, it may be best to manually
## specify the weeks to use, to give better variety in matchups
if (autoWeekRange):
    weekRange = range(0,numWeeks)

##
# Write out the file to import into WYS
##
weekDay=weekDayStart  # start date, year, month, day
# Use sys.stdout if we want to see the output printed out
#with sys.stdout as outFile:
with open(outputFileName, 'w') as outFile:
    for week in weekRange:
        # Allow for fewer teams than weeks.  Just wrap and start over
        ww = week % (numTeams - 1)
        for field in range(0,len(fieldTimes)):
            thisField=weeklyMap[ww][field]
            timeSlotStart=fieldTimes[field][0]
            timeSlotEnd=datetime.combine(date.today(),timeSlotStart)+timedelta(minutes=gameLength)
        
            outFile.write('{dt.month}/{dt.day}/{dt.year}'.format(dt=weekDay))
            outFile.write('\t' + timeSlotStart.strftime('%H:%M')+ '\t' +timeSlotEnd.strftime('%H:%M'))
            outFile.write('\t' + str(fieldTimes[field][1]))
            outFile.write('\t' +teamNames[thisField[0]] + '\t'+ teamNames[thisField[1]])
            outFile.write('\n')
        weekDay=weekDay+timedelta(days=7)

##
# Write out a week-by-week csv file for sharing
##
weekDay=weekDayStart  # start date, year, month, day
weekCount = 1
# Use sys.stdout if we want to see the output printed out
#with sys.stdout as outFile:
with open(outputWeekByWeekFileName, 'w') as outWeekFile:
    outWeekFile.write(seasons + ',,Week')
    for week in weekRange:
        outWeekFile.write(',' + str(weekCount) + ',{dt.month}/{dt.day}/{dt.year}'.format(dt=weekDay))
        weekDay=weekDay+timedelta(days=7)
        weekCount += 1
    outWeekFile.write('\n')

    # Date, Start, End, Field
    outWeekFile.write('Field,Start Time,End Time')
    for week in weekRange:
        outWeekFile.write(',Home,Away')
    outWeekFile.write('\n')

    for field in range(0,len(fieldTimes)):
        timeSlotStart=fieldTimes[field][0]
        timeSlotEnd=datetime.combine(date.today(),timeSlotStart)+timedelta(minutes=gameLength)
        outWeekFile.write(str(fieldTimes[field][1]))
        outWeekFile.write(',' + timeSlotStart.strftime('%H:%M')+ ',' +timeSlotEnd.strftime('%H:%M'))
        for week in weekRange:
            # Allow for fewer teams than weeks.  Just wrap and start over
            ww = week % (numTeams - 1)
            thisField=weeklyMap[ww][field]
            outWeekFile.write(',' +teamNames[thisField[0]] + ','+ teamNames[thisField[1]])
        outWeekFile.write('\n')

    outWeekFile.write('\n\n\n')
    outWeekFile.write('Team,#Home,#Away,#Total\n')
    for teamNum in range(0, numTeams):
        outWeekFile.write(teamNames[teamNum])
        outWeekFile.write(',' + str(homeCount[teamNum]) + ',' + str(awayCount[teamNum]))
        outWeekFile.write(',' + str(homeCount[teamNum] + awayCount[teamNum]) + '\n')
        
