import pickle
from requirementtuple import Requirement
from bs4 import BeautifulSoup
from test_data import TestData

# Config
TEST_MODE = False
data = None


def findDeps(requirement_name, level=None, depth=0, breadcrumb=""):
    found_requirements = data.get(requirement_name)
    print(
        " " * (depth),
        ">" * depth,
        requirement_name,
        f'{"(" + str(level) +")" if level else ""}',
    )
    # Create the  first node in the breadcrumb if there is none
    if not breadcrumb:
        breadcrumb = requirement_name

    # If there are no child nodes, return what we have thus far.
    if not found_requirements:
        return (depth, breadcrumb)

    # If there are child node iterate through them depth first
    else:
        for requirement in found_requirements:
            req_name = requirement.name
            req_level = requirement.level
            findDeps(
                req_name,
                level=req_level,
                depth=depth + 1,
                breadcrumb=breadcrumb + f" -> {req_name}({req_level})",
            )

# Load test data if debugging:
if TEST_MODE:
   data = TestData
# Otherwise load data from the pickled scraped web data:
else:
    with open("all_weapons_data.pickle", "rb") as f:
        data = pickle.load(f)

# Allow for search by substring if we only want a subset of the data renderd:
inp = input("Attachment Name: ")
for item_name, req_list in data.items():
    try:
        if not inp or inp in item_name:
            findDeps(item_name, depth=0)
            print(f"_________________")
    except Exception as e:
        print(f"ERROR WITH REQS FOR: {item_name}:{req_list} - {e}")
