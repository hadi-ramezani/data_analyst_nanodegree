#! /usr/bin/env python

import sqlite3
import csv
from pprint import pprint

sqlite_file = 'osm_san_diego.db'

# Connect to the database
conn = sqlite3.connect(sqlite_file)
conn.text_factory = str

# Create a cursor object
cur = conn.cursor()

# Drop the tables if they exist
cur.execute('''DROP TABLE IF EXISTS nodes_tags''')
conn.commit()
cur.execute('''DROP TABLE IF EXISTS ways_tags''')
conn.commit()
cur.execute('''DROP TABLE IF EXISTS nodes''')
conn.commit()
cur.execute('''DROP TABLE IF EXISTS ways''')
conn.commit()
cur.execute('''DROP TABLE IF EXISTS ways_nodes''')
conn.commit()

# Create the tables, specifying the column names and data types:
cur.execute('''
    CREATE TABLE nodes_tags(id INTEGER, key TEXT, value TEXT,type TEXT)
''')
conn.commit()
cur.execute('''
    CREATE TABLE ways_tags(id INTEGER, key TEXT, value TEXT,type TEXT)
''')
conn.commit()
cur.execute('''
    CREATE TABLE nodes(id INTEGER, lat FLOAT, lon FLOAT, user TEXT, uid INTEGER, version INTEGER, changeset INTEGER, timestamp TIMESTAMP)
''')
conn.commit()
cur.execute('''
    CREATE TABLE ways(id INTEGER, user TEXT, uid INTEGER, version INTEGER, changeset INTEGER, timestamp TIMESTAMP)
''')
conn.commit()
cur.execute('''
    CREATE TABLE ways_nodes(id INTEGER, node_id INTEGER, position INTEGER)
''')
conn.commit()

# Read in the data
with open('nodes_tags.csv','rb') as node_tags_file, \
     open('ways_tags.csv','rb') as ways_tags_file, \
     open('nodes.csv','rb') as nodes_file, \
     open('ways.csv','rb') as ways_file, \
     open('ways_nodes.csv','rb') as ways_nodes_file:
    node_tags = csv.DictReader(node_tags_file)
    ways_tags = csv.DictReader(ways_tags_file)
    nodes = csv.DictReader(nodes_file) # comma is default delimiter
    ways = csv.DictReader(ways_file) # comma is default delimiter
    ways_nodes = csv.DictReader(ways_nodes_file) # comma is default delimiter
    db_node_tags = [(i['id'], i['key'],i['value'], i['type']) for i in node_tags]
    db_ways_tags = [(i['id'], i['key'],i['value'], i['type']) for i in ways_tags]
    db_nodes = [(i['id'], i['lat'],i['lon'], i['user'], i['uid'], i['version'], i['changeset'], i['timestamp']) for i in nodes]
    db_ways = [(i['id'], i['user'], i['uid'], i['version'], i['changeset'], i['timestamp']) for i in ways]
    db_ways_nodes = [(i['id'], i['node_id'], i['position']) for i in ways_nodes]

# insert the formatted data
cur.executemany("INSERT INTO nodes_tags(id, key, value,type) VALUES (?, ?, ?, ?);", db_node_tags)
conn.commit()
cur.executemany("INSERT INTO ways_tags(id, key, value,type) VALUES (?, ?, ?, ?);", db_ways_tags)
conn.commit()
cur.executemany("INSERT INTO nodes(id, lat, lon, user, uid, version, changeset, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, ?);", db_nodes)
conn.commit()
cur.executemany("INSERT INTO ways(id, user, uid, version, changeset, timestamp) VALUES (?, ?, ?, ?, ?, ?);", db_ways)
conn.commit()
cur.executemany("INSERT INTO ways_nodes(id, node_id, position) VALUES (?, ?, ?);", db_ways_nodes)
conn.commit()

# Close the connection
conn.close()

