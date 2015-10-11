# Input file for U6 Boys

region='45'
age='U06'
gender='B'
firstTeamNum=1  #e.g. if Extra teams are 1&2, start with 3
numTeams=22  #total number of teams
seasons='Seasons: 4648'

weekDayStart=date(2015,9,12)  # start date, year, month, day
timeSlotStart=time(15,15) #hour, minutes
gameLength=105 #minutes for game
numWeeks=10

# if you want to automatically increment time slots, set autoTimeSlot=True
# if you want to provide your own time slots,
#   fill in timeSlots with 24 hour times and set autoTimeSlot=False
#    you need to put in enough timeslots 
timeSlots=['11:45','13:10', '14:45','15:52','17:04']
autoTimeSlot=True

# Overriding week range to get better mixture of games:
weekRange = [0, 3, 6, 9, 12, 1, 4, 7, 10, 2]
autoWeekRange=False

fieldNames=['Bubb U6 1','Bubb U6 2','Bubb U6 3','Bubb U6 4','Bubb U6 5','Bubb U6 6','Bubb U6 7','Bubb U6 8','Bubb U6 9','Bubb U6 11','Bubb U6 12']  

outputFileBaseName='Schedule-' + region + '-' + age + gender + '-' + str(date.today())
