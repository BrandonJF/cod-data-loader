import pickle
from requirementtuple import Requirement
from bs4 import BeautifulSoup
from test_data import TestData

# Config
TEST_MODE = False
data = None



def findDeps(requirement_name, level = None, depth = 0, breadcrumb = ""):
    found_requirements = data.get(requirement_name)
    print(" " * depth, ">" * depth, requirement_name, f'{"(" + str(level) +")" if level else ""}')
    # Create the  first node in the breadcrumb if there is none
    if not breadcrumb:
        breadcrumb = requirement_name
        
    # If there are no child nodes, return what we have thus far. 
    if not found_requirements:
        return (depth, breadcrumb)
    
    # If there are child node iterate through them depth first
    else:
        for requirement in found_requirements:
            # print(f'Navigating {requirement} subtree for {requirement_name}')
            name = requirement.name
            level = requirement.level
            findDeps(name, level= level, depth = depth + 1, breadcrumb = breadcrumb +f' -> {name}({level})')

if not TEST_MODE:    
    with open('all_weapons_data.pickle', 'rb') as f:
        data = pickle.load(f)
else:
    data = TestData

inp = input('Attachment Name: ')
for item_name, req_list in data.items():
    try:
        if not inp or inp in item_name:
            # depth, breadcrumb = findDeps(item_name)
            findDeps(item_name, depth= 0)
            print(f'_________________')
            # print(f'depth = {depth} //{item_name}{breadcrumb}' ,end="\n" * 2)
    except Exception as e:    
        print(f'ERROR WITH REQS FOR: {item_name}:{req_list} - {e}' )
       