region='45'
age='U10'
gender='B3'
firstTeamNum=1  #e.g. if Extra teams are 1&2, start with 3
numTeams=8  #total number of teams
seasons='Seasons: 4644 4684 4646 4647 4648 4744'

weekDayStart=date(2016,3,6)  # start date, year, month, day
timeSlotStart=time(13,30) #hour, minutes
gameLength=105 #minutes for game
numWeeks=7

# if you want to automatically increment time slots, set autoTimeSlot=True
# if you want to provide your own time slots,
#   fill in timeSlots with 24 hour times and set autoTimeSlot=False
#    you need to put in enough timeslots 
timeSlots=['11:45','13:10', '14:45','15:50']
autoTimeSlot=True

# Overriding week range to get better mixture of games:
weekRange = [0, 3, 6, 1, 4, 2, 5]
autoWeekRange=False

# Fill with either field names or field ID's from WYS
fieldNames=['Bubb U6 1','Bubb U6 2','Bubb U6 3','Bubb U6 4']

# Override team names with these names-- leave blank to autofill
teamNames=['43-U10B-C','44-U10B-C','45-U10B-C','109-U10B-C1','109-U10B-C2','35-U10B-C','64-U10B-C','62-U10B-C']
