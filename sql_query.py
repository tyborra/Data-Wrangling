"""
This is a scratchpad for SQL queries. All of the SQL queries used in the report 
are here, but not all of the queries are in the report.
Some queries do not have results on the sample file

"""

import sqlite3 as sq
import pprint as pp

SQLFILE = 'data\Poway_DB.db'

conn = sq.connect(SQLFILE)
cur = conn.cursor()

print('\nNodes:')
cur.execute("""SELECT COUNT(*)
               FROM Node
            ;""")
print('There are {} nodes.'.format(cur.fetchall()))

print('\nWays:')
cur.execute("""SELECT COUNT(*)
               FROM ways
            ;""")
print('There are {} ways.\n'.format(cur.fetchall()))

#users
cur.execute("""SELECT DISTINCT user, COUNT(*) as num_users
               FROM Node UNION ALL 
               SELECT DISTINCT uid, COUNT(*) as more 
               FROM ways               
            ;""")
pp.pprint(cur.fetchall())

#top users
print('\ntop users')
cur.execute("""SELECT tu.user, COUNT(*) as num
                FROM (SELECT user FROM Node UNION ALL SELECT user FROM ways) tu
                GROUP BY tu.user
                ORDER BY num DESC
                LIMIT 10               
            ;""")
pp.pprint(cur.fetchall())

#leisure
print('\nLeisure::')
cur.execute("""SELECT value, COUNT(*) as num
                FROM nodes_tags
                WHERE key='leisure'
                GROUP BY value
                ORDER BY num DESC
                LIMIT 10              
            ;""")
pp.pprint(cur.fetchall())

#Number of unique users
print('\nUnique users:')
cur.execute("""SELECT COUNT(DISTINCT(u.uid))          
                FROM (SELECT uid FROM Node UNION ALL SELECT uid FROM ways) u          
            ;""")
pp.pprint(cur.fetchall())

#Amenities
print('\namentities:')
cur.execute("""SELECT value, COUNT(*) as num
                FROM nodes_tags
                WHERE key='amenity'
                GROUP BY value
                ORDER BY num DESC
                LIMIT 10              
            ;""")
pp.pprint(cur.fetchall())

#Tourism in the area
print('\nTourism:')
cur.execute("""SELECT value, COUNT(*) as num
                FROM nodes_tags
                WHERE key='tourism'
                GROUP BY value
                ORDER BY num DESC
                LIMIT 10              
            ;""")
print('The 10 most common tourist attractions are:')
pp.pprint(cur.fetchall())

#query for different types of artwork from tourism query
print('\nArtwork:')
cur.execute("""SELECT nodes_tags.value, COUNT(*) as num
                FROM nodes_tags
                JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value = 'artwork')ar
                ON nodes_tags.id = ar.id
                WHERE nodes_tags.key = 'artwork_type'
                GROUP BY value
                ORDER BY num DESC
                LIMIT 10              
            ;""")
print('The most common artwork types:')
pp.pprint(cur.fetchall())

#There are no entries for landuse on the sample osm
print('\nland use::')
cur.execute("""SELECT value, COUNT(*) as num
                FROM nodes_tags
                WHERE key='landuse'
                GROUP BY value
                ORDER BY num DESC
                LIMIT 10              
            ;""")
pp.pprint(cur.fetchall())

#Find the name of the vineyard from landuse. There are no entries for landuse on the sample osm
print('\nVineyard Name:') 
cur.execute("""SELECT nodes_tags.value
                FROM nodes_tags
                JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE key = 'landuse')lu
                ON nodes_tags.id = lu.id
                JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value = 'vineyard')v
                ON lu.id = v.id
                WHERE nodes_tags.key = 'name'                 
            ;""")
name = cur.fetchone()
if name:       #Added because this entry does not exist in the sample file
    for n in name:
        name = n
print('The name of the vineyard is {}.'.format(name))
