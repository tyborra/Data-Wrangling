"""

Main function runs all. This will take a raw osm, audit and correct it, convert to csv, then convert to sql db
 
""" 
import audit_f as af
import prep_for_db as pdb
import sql_db as sqd

OSMFILE = "data\poway_sample.osm"
OSM_PATH = "audit_output.osm"


if __name__ == '__main__':    
    
    # Run All from audit_f                  
    print('\nAuditing data ...\n')
    af.run_all(OSMFILE) #audit and save data    
    
    #  prep_for_db    
    print('\n\nWriting audited osm to csv...\n')
    pdb.process_map(OSM_PATH, validate=True)   #create csv files 
   
    # Create SQL Database     
    print('\nCreating SQL Database...\n')
    sqd.create_db()