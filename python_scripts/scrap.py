import mysql.connector
import re
import glob
import os
import datetime
import time
import urllib.request

index = 0
WeatherDataArrReversed = []
WeatherLatestXml = ""

thisYear  = time.strftime("%Y",time.localtime())
thisMonth = time.strftime("%m",time.localtime())
thisDay   = time.strftime("%d",time.localtime())

urlDate = thisYear + '-' + thisMonth + '-' + thisDay

# url = 'https://cuwx.clarkson.edu/xml/NoaaExt-' + urlDate + '.xml'
url = 'https://cuwx.clarkson.edu/json/NoaaExt-' + urlDate + '.json'
fullJsonData = urllib.request.urlopen(url).read().decode('utf-8')
# r = requests.get(url)
# fullXmlData = r.json()

# try:
#    os.remove('temp.txt')
# except OSError:
#     pass

# with open('temp.txt', 'w') as tempFile:
#     tempFile.write(fullXmlData)

# with open('temp.txt', 'r') as tempFile:
#     for line in reversed(list(tempFile)):
#         if(line == '<?xml version="1.0" encoding="UTF-8"?>\n'): 
#             WeatherDataArrReversed.append(line)
#             break
#         else:
#             WeatherDataArrReversed.append(line)
#         index = index + 1

# WeatherDataArrReversed = WeatherDataArrReversed[::-1]

# for i in range(len(WeatherDataArrReversed)):
#     WeatherLatestXml = WeatherLatestXml + WeatherDataArrReversed[i]

jsons = []
k = 0
length = len(fullJsonData)

# seperates each JSON data structure for each minute into a list
for i in range(length-1):
    j = i+1
    if fullJsonData[i] == '}' and fullJsonData[j] == '{':
        jsons.append(fullJsonData[k:i])
        k = j

jsons.reverse()
print(jsons[0])
wxDate = re.search('(observation_time_rfc822":".*)(\d+\s\w\w\w\s\d\d\d\d\s\d\d:\d\d:\d\d)', jsons[0]).group(2)
if not wxDate[2].isdigit():
    wxDate = '0' + wxDate # puts a zero in front if it is before the 10th of the month
wxTemp = re.search('(temp_c":")(\d+.\d)', jsons[0]).group(2)
wxRelativeHumidity = re.search('(relative_humidity":")(\d+)', jsons[0]).group(2)
wxWindHeading = re.search('(wind_degrees":")(\d+)', jsons[0]).group(2)
wxPressure = re.search('(pressure_mb":")(\d+\.\d+)', jsons[0]).group(2)
wxDewpoint = re.search('(dewpoint_c":")(\d+\.\d+)', jsons[0]).group(2)
wxWindspeed = re.search('(wind_mph":")(\d+\.\d+)', jsons[0]).group(2)

# Original adds a minute for some reason
wxSecondString = wxDate[18:20]
wxSecondInteger = int(wxSecondString)
wxMinuteString = wxDate[15:17]    
wxMinuteInteger = int(wxMinuteString)
wxHourString = wxDate[12:14]
wxHourInteger = int(wxHourString)
wxDayString = wxDate[0:2]
wxDayInteger = int(wxDayString)
wxMonthString = wxDate[3:6]
wxYearString = wxDate[7:11]
wxYearInteger = int(wxYearString)
months = [['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec','new'],
          [31,28,31,30,31,30,31,31,30,31,30,31,0]]
if wxSecondInteger >= 30: # Rounds up minute if past 30 seconds    
    if(wxMinuteInteger == 59):
        wxMinuteInteger = 00
        wxHourInteger = wxHourInteger + 1
        if wxHourInteger == 24: #Rounds up hour,day, etc if necessary
            wxHourInteger = 00
            wxDayInteger = wxDayInteger + 1
            for i in range(12):
                if months[0][i] == wxMonthString:
                    break
            if wxYearInteger % 4 != 0:
                leapYear = False
            elif wxYearInteger % 100 != 0:
                leapYear = True
            elif wxYearInteger % 400 != 0:
                leapYear = False
            else:
                leapYear = True
            if leapYear and wxMonthString == months[0][1] and wxDayInteger == months[1][1]:
                wxNewDayInteger = 30
            elif wxDayInteger >= (months[1][i] + 1):
                wxDayInteger = 1
                wxMonthString = months[0][i+1]
                if wxMonthString == months[0][12]:
                    wxYearInteger = wxYearInteger + 1
                    wxMonthString = months[0][0]
    else:
        wxMinuteInteger = wxMinuteInteger + 1
    if wxMinuteInteger == 0:
        newMinute = '00'
    else:
        newMinute = str(wxMinuteInteger)
    if wxHourInteger == 0:
        newHour = '00'
    else:
        newHour = str(wxHourInteger)
    if wxDayInteger < 10:
        newDay = '0' + str(wxDayInteger)
    else:
        newDay = str(wxDayInteger)
    newYear = str(wxYearInteger)
    wxDate = newDay + ' ' + wxMonthString + ' ' + newYear + ' ' + newHour + ':' + newMinute

wxDateNoSeconds = wxDate[0:18]
wxConvertedTimestamp = datetime.datetime.strptime(wxDateNoSeconds, '%d %b %Y %H:%M')

print(wxConvertedTimestamp)

