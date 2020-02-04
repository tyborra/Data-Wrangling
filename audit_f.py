"""
Audits and corrects raw osm. If confirm changes is True it reruns the audit on the output file to confirm changes. If save_file is True file will be saved if False
the audit will be run but changes will not be saved
"""

import xml.etree.cElementTree as ET
from collections import defaultdict
import re


OSMFILE = "data\poway_sample.osm"
file_OUT = "audit_output.osm"

confirm_changes = True # boolean to confirm changes by auditing output file
save_file = True  #boolean to determine if changes are saved to file

output_counter = 0 #global variable to ensure the confirmation audit does not have any output

# ================================================== #
#               Audit Street                         #
# ================================================== #
#Adapted from example in Case Study

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
state_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons", "Highway 78", "Peak", "Way" ]

mapping = { "St": "Street",
            "St.": "Street",
            "Ave": "Avenue",
            "Av": "Avenue",
            "Sr-78": "Highway 78",
            "Rd.": "Road",
            "Rd":  "Road",
            "Blvd": "Boulevard",
            "Blvd.": "Boulevard",
            "Bl": "Boulevard",
            "DRIVE": "Drive",
            "Dr": "Drive",
            "Ct": "Court",
            "Ct.": "Court",
            "Pl": "Place",
            "Pe": "Peak",
            "Sq": "Square",
            "La": "Lane",
            "Ln": "Lane",
            "Tr": "Trail",
            "Pk": "Parkway",
            "Py": "Parkway",
            "Pkwy.": "Parkway",
            "Cmns": "Commons",
            "Wa": "Way"     
           }


def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)
            

def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit_street(osmfile):
    osm_file = open(osmfile, "r")      
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close() 
    return street_types


def update_name(name, mapping):
    m = street_type_re.search(name)
    if m:
        street_type = m.group()        
        if street_type not in expected:
            name = re.sub(street_type_re, mapping[street_type], name)            
    return name
   
    
def fix_street_name(osmfile):
    street_problems = 0
    street_types = audit_street(osmfile)
    for types, elem in street_types.iteritems():
        for name in elem:
            if types in mapping:
                update_name(name, mapping)
                street_problems += 1    
    print('\nStreets Audited: {} problems found\n'.format(street_problems))
    return street_types 
def most_common_street_type(street_list): 
    new_street_list = []
    for st in street_list:
        if st not in expected:
            new_street_list.append(st)
    return sorted(set(new_street_list), key=street_list.count)[-10:]
                
                
# ================================================== #
#               Audit State                          #
# ================================================== #
    
def is_state(elem):
    return (elem.attrib.get('k') == "addr:state")
                
def audit_state(osmfile):
    problem_counter = 0
    for event, elem in ET.iterparse(osmfile, events=('start', 'end')):
        if event == 'end':
            if is_state(elem):
                state = elem.attrib.get('v')
                if state != 'CA':
                    problem_counter += 1
    print('State Audited: {} problems found\n'.format(problem_counter))


# ================================================== #
#               Audit Country                        #
# ================================================== #    

def is_country(elem):    
    return (elem.attrib.get('k') == "is_in:country")       
                
def audit_country(filename):
    problem_counter = 0
    for event, elem in ET.iterparse(filename, events=('start', 'end')):
        if event == 'end':
            if is_country(elem):
                country = elem.attrib.get('v')
                if country != 'United States of America':
                    problem_counter += 1
    print('Country Audited: {} problems found\n'.format(problem_counter))
    

# ================================================== #
#               Print and Write to File              #
# ================================================== #

def print_write_to_file(osmfile, street_types):
    print('\nPrinting results and correcting information...')
    street_changes = defaultdict(list)
    state_changes = defaultdict(list)
    country_changes = defaultdict(list)
    
    osm_file = ET.parse(osmfile)
    root = osm_file.getroot()
    street_type_list = []
    
    for elem in root.iter():
        for tag in elem.iter("tag"):
            
            #Change Streets
            if is_street_name(tag):                    
                m = street_type_re.search(tag.attrib['v'])
                name = tag.attrib['v']                       
                if m:
                    street_type = m.group()     
                    street_type_list.append(street_type)
                    if street_type  not in expected:                        
                        if street_type in mapping.keys():
                            old_street = tag.attrib['v']
                            tag.attrib['v']  = re.sub(street_type_re, mapping[street_type], name)  
                            new_street = tag.attrib['v']  
                            street_changes[old_street].append(new_street)
                            
            #Change States
            if is_state(tag):                    
                state_name = tag.attrib['v']                   
                if state_name != 'CA':
                    old_state = tag.attrib['v'] 
                    tag.attrib['v']  = 'CA'  
                    new_state = tag.attrib['v']
                    state_changes[old_state].append(new_state)
                    
            #Change Country
            if is_country(tag): 
                country_name = tag.attrib['v']
                if country_name != 'United States of America':
                    old_country = tag.attrib['v'] 
                    tag.attrib['v']  = 'United States of America'  
                    new_country = tag.attrib['v']
                    country_changes[old_country].append(new_country)        
                                 
    #Print Results
    changes = 0 
    street_type_set = set(street_type_list)
    most_common = most_common_street_type(street_type_list)
    
    print('\nStreet Changes:')    
    for key, value in street_changes.iteritems():
        changes += len(value)
        print('{:<22}  ==>  {:>27} x {:>2}'.format(key, value[0], len(value)))    
            
    print('\nState Changes:')    
    for key, value in state_changes.iteritems():
        changes += len(value)
        print('{:<12}  ==>  {:>2} x {:>2}'.format(key, value[0], len(value)))
    
    print('\nCountry Changes:')    
    for key, value in country_changes.iteritems():
        changes += len(value)
        print('{:<5}  ==>  {:>24} x {:>2}'.format(key, value[0], len(value)))
        
    
    #Save File
    global output_counter  
    
    if save_file:
        if confirm_changes:
            if output_counter == 0:
                output_counter +=1
                print('\nA total of {} street types were found...'.format(len(street_type_set)))
                print('The most common street types not in expected are:\n {}'.format(most_common))
                print('\n{} changes were made'.format(changes))
                print('\n\nSaving to file...')
                osm_file.write( open(file_OUT, 'a+'), encoding = 'UTF-8')                
                print('\nFile saved as: {}'.format(file_OUT))
                
            else:
                print('\n{} problems were found in the output file'.format(changes))
                 
        elif not confirm_changes:
            print('\n{} changes were made'.format(changes))
            print('\n\nSaving to file...')
            osm_file.write( open(file_OUT, 'a+'), encoding = 'UTF-8')            
            print('\nFile saved as: {}'.format(file_OUT))            
    
    
# ================================================== #
#               Main                                 #
# ================================================== #
                
def run_all(osm):    
    street_types = fix_street_name(osm)
    audit_state(osm)
    audit_country(osm)    
    print_write_to_file(osm, street_types)

if __name__ == '__main__':
    
    run_all(OSMFILE)
    
    if confirm_changes == True:
        print('\nConfirming Changes to output file...\n')
        run_all(file_OUT)   
