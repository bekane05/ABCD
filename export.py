'''
Brian Kane

CS 348 Database Systems

ABCD football database export functions

Creates functions to export player statistics into the offensive_performances,
	defensive_performances, and kicker_performances tables
	
Users interacting with the database will most often be seeking either individual
	player statistics or how players rank against each other in certain
	statistical categories, which are both easily done by our performance tables.
	By the design of our database, users are able to query these performance tables
	to gather information about any player who has ever had some kind of performance
	in a game.
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
table_name = raw_input("Enter the table from which you wish to extract data: ")

# Connect to database using MySQLdb
db = MySQLdb.connect(host="csdb", user=username, passwd=password, db="ab")
cursor = db.cursor()

'''
Function to export rows from the offensive_performances table

Preconditions:
	- connection to database has been established
	- table_name = offensive_performances
	- offensive_performances table has > 0 rows

Postconditions:
	- objects contains a list of dictionaries, with each set of key-value pairs
		representing a row in the table
'''
def exportoffensive(table_name):

	# Setup MySQL query
	selectstmt = ("""
		SELECT team_name, player_number, game_date, passing_yards, 
		rushing_yards, receiving_yards, touchdowns, interceptions, fumbles, 
		quarterback_rating, yards_per_carry, yards_per_reception
		FROM 
		"""
		+ table_name)
	
	# Try to execute the MySQL SELECT query
	try:
		cursor.execute(selectstmt)
	except MySQLdb.ProgrammingError:
		print "The following query failed:"
		print selectstmt
	
	# Get the result of MySQL query
	rows = cursor.fetchall()
	
	# Convert query result to a list of key-value pairs
	objects = []
	for row in rows:
		d = collections.defaultdict()
		d['team_name'] = row[0]
		d['player_number'] = row[1]
		d['game_date'] = str(row[2])
		d['passing_yards'] = row[3]
		d['rushing_yards'] = row[4]
		d['receiving_yards'] = row[5]
		d['touchdowns'] = row[6]
		d['interceptions'] = row[7]
		d['fumbles'] = row[8]
		d['quarterback_rating'] = row[9]
		d['yards_per_carry'] = row[10]
		d['yards_per_reception'] = row[11]
		objects.append(d)
		
	return objects

'''
Function to export rows from the defensive_performances table

Preconditions:
	- connection to database has been established
	- table_name = defensive_performances
	- defensive_performances table has > 0 rows

Postconditions:
	- objects contains a list of dictionaries, with each set of key-value pairs
		representing a row in the table
'''
def exportdefensive(table_name):

	# Setup MySQL query
	selectstmt = ("""SELECT team_name, player_number, game_date, tackles, sacks, 
		forced_fumbles, interceptions, passes_defended, tackle_assists FROM 
		""" + table_name)
	
	# Try to execute the MySQL SELECT query
	try:
		cursor.execute(selectstmt)
	except MySQLdb.ProgrammingError:
		print "The following query failed:"
		print selectstmt
	
	# Get the result of MySQL query
	rows = cursor.fetchall()
	
	# Convert query result to a list of key-value pairs
	objects = []
	for row in rows:
		d = collections.defaultdict()
		d['team_name'] = row[0]
		d['player_number'] = row[1]
		d['game_date'] = str(row[2])
		d['tackles'] = row[3]
		d['sacks'] = row[4]
		d['forced_fumbles'] = row[5]
		d['interceptions'] = row[6]
		d['passes_defended'] = row[7]
		d['tackle_assists'] = row[8]
		objects.append(d)
		
	return objects

'''
Function to export rows from the kicker_performances table

Preconditions:
	- connection to database has been established
	- table_name = kicker_performances
	- kicker_performances table has > 0 rows

Postconditions:
	- objects contains a list of dictionaries, with each set of key-value pairs
		representing a row in the table
'''
def exportkicker(table_name):

	# Setup MySQL query
	selectstmt = ("""
		SELECT team_name, player_number, game_date, field_goals_attempted, 
		field_goals_made, field_goal_long, punts, punts_inside_20, punt_avg_distance 
		FROM 
		"""
		+ table_name)
	
	# Try to execute the MySQL SELECT query
	try:
		cursor.execute(selectstmt)
	except MySQLdb.ProgrammingError:
		print "The following query failed:"
		print selectstmt
	
	# Get the result of MySQL query
	rows = cursor.fetchall()
	
	# Convert query result to a list of key-value pairs
	objects = []
	for row in rows:
		d = collections.defaultdict()
		d['team_name'] = row[0]
		d['player_number'] = row[1]
		d['game_date'] = str(row[2])
		d['field_goals_attempted'] = row[3]
		d['field_goals_made'] = row[4]
		d['field_goal_long'] = row[5]
		d['punts'] = row[6]
		d['punts_insider_20'] = row[7]
		d['punt_avg_distance'] = row[8]
		objects.append(d)
		
	return objects


# Choose the appropriate export function and store the result in a list
data = []

if table_name == "offensive_performances":
    data = exportoffensive(table_name)
elif table_name == "defensive_performances":
    data = exportdefensive(table_name)
elif table_name == "kicker_performances":
    data = exportkicker(table_name)
else:
    print "Error: The entered table name is invalid."


# Convert to JSON file format and output nicely
j = json.dumps(data, indent=4, separators=(',', ': '))
stats = 'player_statistics.json'
f = open(stats, 'w')
print >> f, j
