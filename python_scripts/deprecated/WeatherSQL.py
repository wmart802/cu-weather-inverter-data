# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 21:04:27 2019

@author: Chris
"""

#import mysql.connector
#
##cnx = mysql.connector.connect(user='historicalqueryuser', password='clarksonuser',
##                              host='128.153.12.113',
##                              database='inverter_and_weather_data')
##cnx.close()
#
##cnx = mysql.connector.connect(user='pythondev', password='WMDccp2018!',
##                              host='128.153.12.113',
##                              database='inverter_and_weather_data')
##cnx.close()
#
#cnx = mysql.connector.connect(user='historicalqueryuser', password='WMDccp2018!',
#                              host='128.153.12.113',
#                              database='inverter_and_weather_data')
#cnx.close()

#import mysql.connector
#from mysql.connector import errorcode
#
#try:
#  cnx = mysql.connector.connect(user='pythondev', host='128.153.12.113',
#                                password='WMDccp2018!',
#                                database='blackboard_gui')
#except mysql.connector.Error as err:
#  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
#    print("Something is wrong with your user name or password")
#  elif err.errno == errorcode.ER_BAD_DB_ERROR:
#    print("Database does not exist idiot")
#  else:
#    print(err)
#else:
#  cnx.close()

#temp_celsius, relative_humidity, wind_heading, pressure_mb, dewpoint_celsius, windspeed_mph  
  
import mysql.connector

mydb = mysql.connector.connect(
  host="128.153.12.113", user="pythondev", passwd="WMDccp2018!", database="blackboard_gui"
)

mycursor = mydb.cursor()

sql = (
       "INSERT INTO inverter_and_weather_data (timestamp, temp_celsius, relative_humidity, wind_heading, pressure_mb, dewpoint_celsius, windspeed_mph)"
       "VALUES ('00:00:04', %temp_celsius_xml, %relative_humidity_xml, %wind_heading_xml, %pressure_mb_xml, %dewpoint_celsius_xml, %windspeed_mph_xml)"
)

mycursor.execute(sql)

mydb.commit()

print(mycursor.rowcount, "record inserted.")
mydb.close()
#timestamp, MPPT,VDC1, IDC1, PDC1, VDC2, IDC2, PDC2, VAC, IAC, PAC, TINV, TINT, ENERGY, RISO, ILEAK, GENFREQ, temp_celsius, relative_humidity, wind_heading, pressure_mb, dewpoint_celsius, windspeed_mph
