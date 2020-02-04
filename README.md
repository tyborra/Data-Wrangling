## Wrangle Open Street Map Data
### File Descriptions:
>- __main.py:__ runs all from raw osm to cleaned SQL db. Run once then use sql_query.py
>to run queries
>- __sql_query.py:__ is a scratchpad of sql queries used in the investigation. All sql queries
>used in the investigation are in this file but not all of the queries were used in the
>report
>- __audit_f.py__ is the primary audit file it can be used as a stand alone audit with a 
>cleaned osm as output or run from main.py to create a clean db.
>- __prep_for_db.py:__ converts the osm output from audit_f.py to csv format using the
>schema in schema.py. 
>- __schema.py:__ is the schema to create csv files from the coursework
>- __sql_db.py:__ creates and populates the SQL database
>- __Report.pdf:__ the final report
