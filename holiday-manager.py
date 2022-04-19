import datetime as dt
import json
from unicodedata import name
from bs4 import BeautifulSoup
import requests
import calendar
from dataclasses import dataclass


# -------------------------------------------
# Modify the holiday class to 
# 1. Only accept Datetime objects for date.
# 2. You may need to add additional functions
# 3. You may drop the init if you are using @dataclasses
# --------------------------------------------

class Holiday:

    def __init__(self, name, date):
        self.name = name
        self.date = date
    
    def __str__(self):
        return f"{self.name} ({self.date})"

    def getData(self):
        returnList = [self.name, self.date]
        return returnList
        # String output
        # Holiday output when printed.
          
           
# -------------------------------------------
# The HolidayList class acts as a wrapper and container
# For the list of holidays
# Each method has pseudo-code instructions
# --------------------------------------------

class HolidayList:

    # displays if there is unsaved work
    def __init__(self):
        self.innerHolidays = []
        self.notSaved = True
    # shows users that the work is unsaved
    def pendingSave(self):
        if self.notSaved == True:
            return True
        else:
            return False
    
    def getData(self):
        returnList = [self.name, self.date]
        return returnList

    def getResponse(self):
        while 1:
            responseInput = input("yes or no: ")
            if responseInput == 'yes' or responseInput == 'no':
                return responseInput
            else:
                print("Invalid input, please try again.")

        # getting user input response of yes or no
   
    def addHoliday(self, holidayObj):
        if type(holidayObj) == Holiday:
            self.innerHolidays.append(holidayObj)
            print(f'{holidayObj}')
            print("""
            =================
            new holiday entry
            =================
            """)
            self.notSaved = True
        else:
            print("Not a valid input, please try again.") 

        # Check user if holiday is valid

        # Make sure holidayObj is an Holiday Object by checking the type
        # Use innerHolidays.append(holidayObj) to add holiday
        # print to the user that you added a holiday

    # def findHoliday(HolidayName, Date):
    #     # Find Holiday in innerHolidays
    #     # Return Holiday


    def removeHoliday(self, HolidayName, Date):
        selectedHoliday = Holiday(HolidayName, Date)
        deleteHoliday = False

        # if inupts are valid it will delete holiday
        for x in self.innerHolidays:
            if vars(x) == vars(selectedHoliday):
                self.innerHolidays.remove(x)
                print("""
                ===============
                Holiday removed
                ===============
                """)
                deleteHoliday = True
                self.notSaved = True
        
        if not deleteHoliday:
            print("Invalid holiday, try again.")
        # Find Holiday in innerHolidays by searching the name and date combination.
        # remove the Holiday from innerHolidays
        # inform user you deleted the holiday

    def readJson(self, filelocation):
        with open(filelocation, 'r') as file:
            dict = json.load(file)
        dictList = dict['holidays']
        for holiday in dictList:
            strDate = holiday['date'].split('-')
            intDate = [int(x) for x in strDate]
            dateObj = dt.date(intDate[0], intDate[1], intDate[2])
            self.innerHolidays.append(Holiday(holiday['name'], dateObj))
        # Read in things from json file location

    def saveJson(self, filelocation):
        file = open(filelocation, 'w')
        holdList = []
        dictList_2 = {'holidays': holdList}
        for x in self.innerHolidays:
            nameDate = x.getData()
            holdList.append({'name': nameDate[0], 'date': str(nameDate[1])})
        json.dump(dictList_2, file, indent = 2)
        file.close()
        print("""
        =================
        Added to new file
        =================
        """)
        self.notSaved = False
        # Write out json file to selected file.

    def makeDate(self, date, year):
        dateStr = date.split(" ")
        monthNum = list(calendar.month_abbr).index(dateStr[0])
        day = int(dateStr[1])
        dateObject = dt.date(int(year), monthNum, day)
        return dateObject


    def getDateInput(self):
        while 1:
            userInput = input("Enter a date 'YYYY-MM-DD': ")
            try:
                inputList = [int(x) for x in list(userInput.split("-"))]
                myDate = dt.date(inputList[0], inputList[1], inputList[2])
                print('======================')
                return myDate

            except:
                print("Invalid input, please try again")
    
    def getWeekInput(self):     #get week input in range 1-53, return integer (0 for current week)
        while 1:
            week = input("What week? '1-53'")
            if week == '':
                return 0
            else:
                try:
                    week = int(week)
                    if week in range(1,54):
                        return week
                    else:
                        print("Not valid input, try again.")
                except:
                    print("Invalid input, integers only.")

    def getYearInput(self):     #get year input in range 2020-2024, return integer
        while 1:
            year = input("What year? '2020-2024':")
            try:
                year = int(year)
            except:
                print("Invalid input, year must be an integer")
            else:
                if year in range(2020,2025):
                    return year
                else:
                    print("Invalid year, fix format")   
    def scrapeHolidays(self):
        # getting 2 years in the past, current year, and 2 years in future
        years = [2020, 2021, 2022, 2023, 2024]
        for year in years:
            html = requests.get(f"https://www.timeanddate.com/holidays/us/{year}?hol=33554809")
            soup = BeautifulSoup(html.text, 'html.parser')
            table = soup.find('tbody')
            rows = table.find_all(attrs = {'class':'showrow'})
            for row in rows:
                date = self.makeDate(row.find('th').text, year)
                name = row.find('a').text
                grabHoliday = Holiday(name, date)
                self.innerHolidays.append(grabHoliday)
        # Scrape Holidays from https://www.timeanddate.com/holidays/us/ 
        # Remember, 2 previous years, current year, and 2  years into the future. You can scrape multiple years by adding year to the timeanddate URL. For example https://www.timeanddate.com/holidays/us/2022
        # Check to see if name and date of holiday is in innerHolidays array
        # Add non-duplicates to innerHolidays
        # Handle any exceptions.     

    def numHolidays(self):
        print('''
Holiday Management
==================
        ''')
        print(f"The total number of Holidays are:  {len(self.innerHolidays)}.")
        # Return the total number of holidays in innerHolidays
    
    def filter_holidays_by_week(self, year, weekNumber):
        filteredHWList = list(filter(lambda x: x.getData()[1].isocalendar()[1] == weekNumber 
            and x.getData()[1].isocalendar()[0] == year, self.innerHolidays))

        return filteredHWList
        # Use a Lambda function to filter by week number and save this as holidays, use the filter on innerHolidays
        # Week number is part of the the Datetime object
        # Cast filter results as list
        # return your holidays

    def displayHolidaysInWeek(self, holidayList):
        for x in holidayList:
            print(x)
        # Use your filter_holidays_by_week to get list of holidays within a week as a parameter
        # Output formated holidays in the week. 
        # * Remember to use the holiday __str__ method.

    # def getWeather(self):
    #     url = "https://community-open-weather-map.p.rapidapi.com/forecast"
    #     params = {"q":"Milwaukee,us"}
    #     headers = {
	#         "X-RapidAPI-Host": "community-open-weather-map.p.rapidapi.com",
	#         "X-RapidAPI-Key": "5cb86d699dmshd363812faa5fe6dp1d9ea1jsnc3ebf5ca00ea"
    #     }
    #     response = requests.request("GET", url, headers = headers, params = params)
    #     data = response.json()
    #     weatherList = []
    #     for i in range(5):
    #         weatherList.append(data['list'][8*i]['weather'][0]['description'])
    #     return weatherList
    #     # Convert weekNum to range between two days
    #     # Use Try / Except to catch problems
    #     # Query API for weather in that week range
    #     # Format weather information and return weather string.

    def viewCurrentWeek(self):
        now = dt.datetime.now()
        weekNum = now.isocalendar()[1]
        year = now.year
        day = now.day
        validInput = 0
        filteredHWList = self.filter_holidays_by_week(year, weekNum)
        self.displayHolidaysInWeek(filteredHWList)
        
    #     print("Would you like to see the weather?")
    #     response = self.getResponse()
    #     if response == 'n':
    #         self.displayHolidaysInWeek(filteredHWList)
    #     else:
    #         weatherList = self.getWeather()     #weather from today for 5 days
    #         for x in filteredHWList:
    #             if x.getData()[1].day in range(day, day+5):
    #                 print(f"{x} {weatherList[x.getData()[1].day - day]}")   #calculates index for weatherList
    #             else:
    #                 print(x)
        # Use the Datetime Module to look up current week and year
        # Use your filter_holidays_by_week function to get the list of holidays 
        # for the current week/year
        # Use your displayHolidaysInWeek function to display the holidays in the week
        # Ask user if they want to get the weather
        # If yes, use your getWeather function and display results

    def mainMenu(self):
        # displays menu and prompts user to select an option
        print('''
Holiday Menu
=============
1. Add a Holiday
2. Remove a Holiday
3. Save Holiday List
4. View Holidays
5. Exit
        ''')
        # 1: add a holiday; sort by numbers, makes it easier.
        while 1:
            try:
                userInput = int(input("Please select an option, 1 - 5: "))
                if userInput in range(1,6):
                    return userInput
                else:
                    print("Invalid input, please try again.")
            except:
                print("Invalid input, please try an int.")


def main():
    closeOut = False

    displayHolidayList = HolidayList()
    displayHolidayList.readJson("preloaded-holidays.json")
    displayHolidayList.scrapeHolidays()
    displayHolidayList.numHolidays()
    
    # while the game has not been given the value to shut down
    while not closeOut:
        userInput = displayHolidayList.mainMenu()
        validInput = 0

    # nums = the options user can select off of main menu
        if userInput == 1:
            print('''
Adding Holiday
==============''')
            name = input("Please ADD holiday: ")
            date = displayHolidayList.getDateInput()
            displayHolidayList.addHoliday(Holiday(name, date))

        elif userInput == 2:
            print('''
Remove a Holiday
================''')
            name = input("REMOVE holiday:  ")
            date = displayHolidayList.getDateInput()
            displayHolidayList.removeHoliday(name, date)

        elif userInput == 3:
            print('''
Saving Holiday List
===================''')
            print("Would you like to SAVE? [yes/no]: ")
            choice = displayHolidayList.getResponse()
            if choice == 'yes':
                displayHolidayList.saveJson('newHolidayList.json')
            else:
                print("File will not be saved and data will be lost.")

        elif userInput == 4:
            print('''
View Holidays
=============''')
            year = displayHolidayList.getYearInput()
            weekNum = displayHolidayList.getWeekInput()
            now = dt.datetime.now()
            if weekNum == 0:
                weekNum = now.isocalendar()[1]
            if weekNum == now.isocalendar()[1] and year == now.year:
                displayHolidayList.viewCurrentWeek()
            else:
                tempList = displayHolidayList.filter_holidays_by_week(year, weekNum)
                displayHolidayList.displayHolidaysInWeek(tempList)

        else:
            print("""
Exit
====""")
            if displayHolidayList.pendingSave():
                print("If you exit, all unsaved data will be lost.")
                choice = displayHolidayList.getResponse()
                if choice == 'yes':
                    print("Ending program.")
                    closeOut = True
            else:
                print("Exit program?")
                choice = displayHolidayList.getResponse()
                if choice == 'yes':
                    print("Ending program.")
                    closeOut = True


main()
    # Large Pseudo Code steps
    # -------------------------------------
    # 1. Initialize HolidayList Object
    # 2. Load JSON file via HolidayList read_json function
    # 3. Scrape additional holidays using your HolidayList scrapeHolidays function.
    # 3. Create while loop for user to keep adding or working with the Calender
    # 4. Display User Menu (Print the menu)
    # 5. Take user input for their action based on Menu and check the user input for errors
    # 6. Run appropriate method from the HolidayList object depending on what the user input is
    # 7. Ask the User if they would like to Continue, if not, end the while loop, ending the program.  If they do wish to continue, keep the program going. 


# if __name__ == "__main__":
#     main();


# Additional Hints:
# ---------------------------------------------
# You may need additional helper functions both in and out of the classes, add functions as you need to.
#
# No one function should be more then 50 lines of code, if you need more then 50 lines of code
# excluding comments, break the function into multiple functions.
#
# You can store your raw menu text, and other blocks of texts as raw text files 
# and use placeholder values with the format option.
# Example:
# In the file test.txt is "My name is {fname}, I'm {age}"
# Then you later can read the file into a string "filetxt"
# and substitute the placeholders 
# for example: filetxt.format(fname = "John", age = 36)
# This will make your code far more readable, by seperating text from code.
