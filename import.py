'''
Brian Kane

CS 348 Database Systems

ABCD football database import functions

Creates functions to import player statistics into the offensive_performances,
	defensive_performances, and kicker_performances tables
	
Although database users shouldn't be altering data, administrators who are
	authorized to import data will be almost always importing player
	performance data. Once a particular NFL season is underway, there is little
	change regarding players, teams, coaches, or schedules. The only tables that
	will be frequently altered are the player performance tables, which need to be
	updated every week after games have taken place.
'''

import MySQLdb
import json
import collections
import getpass
import sys

# Authorization: Get username from command line
username = raw_input("Username: ")

# Authorization: Get password from command line and mask input
password = getpass.getpass("Password: ")

# Get the table name from which we will be extracting data
table_name = raw_input("Enter the table from which you wish to import data: ")

# Connect to database using MySQLdb
db = MySQLdb.connect(host="csdb", user=username, passwd=password, db="ab")
cursor = db.cursor()

# Take the JSON file and load it into a dictionary
json_data = open(filename)
data = json.load(json_data)
json_data.close()

'''
Function to import a row into the offensive_performances table

Preconditions:
	- connection to database has been established
	- table_name = offensive_performances
	- offensive_performances table has > 0 rows
	- JSON file to be imported has been loaded into data dictionary

Postconditions:
	- insertstmt string contains the MySQL INSERT query to be executed
'''
def importoffensive(table_name):
		
	# Setup variables for use in query
	for row in data:
		team_name = row['team_name']
		player_number = row['player_number']
		game_date = row['game_date']
		passing_yards = row['passing_yards']
		rushing_yards = row['rushing_yards']
		receiving_yards = row['receiving_yards']
		touchdowns = row['touchdowns']
		interceptions = row['interceptions']
		fumbles = row['fumbles']
		quarterback_rating = row['quarterback_rating']
		yards_per_carry = row['yards_per_carry']
		yards_per_reception = row['yards_per_reception']
	
	# Setup MySQL insert query
	insertstmt = ("INSERT INTO " + table_name + " VALUES ('%s', '%d', '%s', '%d', '%d', '%d', '%d', '%d', '%d', '%d', '%d', '%d');"
		% (team_name, player_number, game_date, passing_yards, rushing_yards, receiving_yards, touchdowns, interceptions,
		fumbles, quarterback_rating, yards_per_carry, yards_per_reception))
	
	return insertstmt

'''
Function to import a row into the defensive_performances table

Preconditions:
	- connection to database has been established
	- table_name = defensive_performances
	- defensive_performances table has > 0 rows
	- JSON file to be imported has been loaded into data dictionary

Postconditions:
	- insertstmt string contains the MySQL INSERT query to be executed
'''
# Function to import defensive player statistics
def importdefensive(table_name):
		
	# Setup variables for use in query
	for row in data:
		team_name = row['team_name']
		player_number = row['player_number']
		game_date = row['game_date']
		tackles = row['tackles']
		sacks = row['sacks']
		forced_fumbles = row['forced_fumbles']
		interceptions = row['interceptions']
		passes_defended = row['passes_defended']
		tackle_assists = row['tackle_assists']
	
	# Setup MySQL insert query
	insertstmt = ("INSERT INTO " + table_name + " VALUES ('%s', '%d', '%s', '%d', '%d', '%d', '%d', '%d', '%d');"
		% (team_name, player_number, game_date, tackles, sacks, forced_fumbles, interceptions, passes_defended, tackle_assists))
	
	return insertstmt

'''
Function to import a row into the kicker_performances table

Preconditions:
	- connection to database has been established
	- table_name = kicker_performances
	- kicker_performances table has > 0 rows
	- JSON file to be imported has been loaded into data dictionary

Postconditions:
	- insertstmt string contains the MySQL INSERT query to be executed
'''
# Function to import kicker player statistics
def importkicker(table_name):
	
	# Setup variables for use in query
	for row in data:
		team_name = row['team_name']
		player_number = row['player_number']
		game_date = row['game_date']
		field_goals_attempted = row['field_goals_attempted']
		field_goals_made = row['field_goals_made']
		field_goal_long = row['field_goal_long']
		punts = row['punts']
		punts_inside_20 = row['punts_inside_20']
		punt_avg_distance = row['punt_avg_distance']
	
	# Setup MySQL insert query
	insertstmt = ("INSERT INTO " + table_name + " VALUES ('%s', '%d', '%s', '%d', '%d', '%d', '%d', '%d', '%d');"
		% (team_name, player_number, game_date, field_goals_attempted, field_goals_made, 
		field_goal_long, punts, punts_inside_20, punt_avg_distance))
	
	return insertstmt


# Choose the appropriate import function and store the result in an empty query string for execution
query = ""
if table_name == "offensive_performances":
    query = importoffensive(table_name)
elif table_name == "defensive_performances":
    query = importdefensive(table_name)
elif table_name == "kicker_performances":
    query = importkicker(table_name)
else:
    print "Error: The entered table name is invalid."
    
    
# Try to execute the MySQL INSERT query
try:
    cursor.execute(query)
except MySQLdb.ProgrammingError:
    print "The following query failed:"
    print insertstmt


# Complete the transaction and close the database connection
con.commit()
print "The transaction was completed successfully."
con.close()
