#! /usr/bin/env python

import sqlite3
from pprint import pprint

sqlite_file = 'osm_san_diego.db'

# Connect to the database
conn = sqlite3.connect(sqlite_file)
conn.text_factory = str

# Create a cursor object
cur = conn.cursor()

# Count the number of nodes in the database
cur.execute("SELECT COUNT(*) FROM nodes COUNT")
num_nodes = cur.fetchall()
print('Number of nodes are: ', num_nodes)

# Count the number of ways in the database
cur.execute("SELECT COUNT(*) FROM ways")
num_ways = cur.fetchall()
print('Number of ways are: ', num_ways)

# Count the number of unique users
cur.execute('SELECT COUNT(DISTINCT(u.uid)) FROM (SELECT uid FROM nodes UNION ALL SELECT uid FROM ways) u')
num_unique_users = cur.fetchall()
print('Number of unique contributing users so far: ', num_unique_users)

# List of top users
cur.execute('SELECT u.user, COUNT(*) as num FROM (SELECT user FROM nodes UNION ALL SELECT user FROM ways) u \
             GROUP BY u.user ORDER BY num DESC LIMIT 10')
top_users = cur.fetchall()
print 'Top 10 users so far: ', top_users

# Top 10 amenities
cur.execute('SELECT value, COUNT(*) as num FROM nodes_tags WHERE key="amenity" \
             GROUP BY value ORDER BY num DESC LIMIT 10')
top_amenities = cur.fetchall()
print("Top 10 amenities :", top_amenities)

# How many Chipotle do we have in San Diego?
cur.execute('SELECT COUNT(*) FROM nodes_tags WHERE UPPER(value) LIKE UPPER("%Chipotle%")')
num_chipotle = cur.fetchall()
print("Number of Chipotle restaurants in San Diego: ", num_chipotle)

# Number of inputs within the last month
cur.execute('SELECT COUNT(*) FROM (SELECT timestamp FROM nodes WHERE timestamp >= "2017-06-01" \
             UNION ALL SELECT timestamp FROM ways WHERE timestamp >= "2017-06-01")')
input_2017 = cur.fetchall()
print('Number of inputs in 2017: ', input_2017)
