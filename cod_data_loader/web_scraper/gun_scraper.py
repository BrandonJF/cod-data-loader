import requests
import re
import collections
import pickle
from bs4 import BeautifulSoup

gun_name_to_url_dict = {}
name_to_requirement = {}
BASE_URL = "https://www.wzranked.com"
URL = "https://www.wzranked.com/wz2/meta/guns"
Requirement = collections.namedtuple('Requirement', ['name', 'level'])

def extract_level_numbers_from_text(string):
    return [int(item) for item in re.findall(r'\b\d+\b', string)]

def unlock_info_to_requirement(unlock_info_div: str):
    text = unlock_info_div # 'EBR-14 / 4 LVL
    name, level = text.split("/")
    name = name.strip()
    level = extract_level_numbers_from_text(level)[0]
    return Requirement(name= name, level= level)
    

# Get all the guns from the top-level page and store in a dict 
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")
results = soup.find(id="__next")
potential_gun_tables = results.find_all("section", class_="col-span-2 md:col-span-1")
desired_gun_table = potential_gun_tables[0]
gun_elements_results = desired_gun_table.find_all("div", class_="mt-1 truncate text-center text-xs text-custom-text-primary") #55 elements
for gun_element in gun_elements_results:
    link = gun_element.find("a")
    gun_name = link.text
    gun_url = link["href"]
    # print(gun_name, end="\n")
    # print(gun_url, end="\n"*2)
    gun_name_to_url_dict[gun_name] = gun_url
# print(gun_name_to_url_dict)

# Iterate through all of the gun pages and load the attachments and required levels. 

NUM_GUNS_TO_LOAD = 100
guns_loaded = 0
for idx, (gun_name, url) in enumerate(gun_name_to_url_dict.items()):
    if (idx >= NUM_GUNS_TO_LOAD):
        break
    target_url = BASE_URL + url
    page = requests.get(target_url)
    gun_page_soup = BeautifulSoup(page.content, "html.parser")
    
    # Base case - at minimum store the weapon in the list:
    name_to_requirement[gun_name] = None
    
    # Further, if there are requirements to unlock this gun/weapon let's store them:
    gun_unlock_req = gun_page_soup.select('#__next > div > main > div.grid.grid-cols-2.gap-4 > section.col-span-2.sm\\:px-2.lg\\:mx-auto.lg\\:w-1\\/2 > div > div > header > p')
    if (len(gun_unlock_req) > 0):        
        gun_unlock_spans = gun_unlock_req[0].find_all("span")
        gun_unlock_req_name = gun_unlock_spans[0].text
        gun_unlock_extracted_levels = extract_level_numbers_from_text(gun_unlock_spans[1].text)
        # Sometimes the level below would be something like 'DMZ' - might be good to handle this
        gun_unlock_req_lvl = gun_unlock_extracted_levels[0] if gun_unlock_extracted_levels else 0
        # We store in list format for compatability with multi requirement attachments
        name_to_requirement[gun_name] = [Requirement(name = gun_unlock_req_name, level = gun_unlock_req_lvl)]
        # print(f'Gun: {gun_name} // Requires unlocking: {gun_unlock_req_name} // Level: {gun_unlock_req_lvl}')
    
    # Now we'll handle related attachments for this specific weapon:
    results = gun_page_soup.find(id="__next")
    attachment_table = results.find("tbody", class_="divide-y divide-custom-background-primary")
    # Ensure that the attachement table is present, indicating there are attachments
    if attachment_table:
        attachement_rows = attachment_table.find_all("tr")
        for attachement_row in attachement_rows: 
            columns = attachement_row.find_all("td")
            attachment_name = columns[1].text
            attachment_type = columns[2].text # barrel/magazine/muzzle...
            attachment_req_unlock_info_divs = columns[3].find_all("div") #<div> VEL 46 / 3 LVL</div> or<div>PDSW 528 / 16 LVL</div>
            attachment_req_unlock_info_divs_text = list(map(lambda x: x.text, attachment_req_unlock_info_divs))
            try:
                requirements_list = list(map(unlock_info_to_requirement,attachment_req_unlock_info_divs_text))
                name_to_requirement[attachment_name] = requirements_list
            except:
                print(f'ERROR: Attachment: {attachment_name} with req: {columns[3].text} can not be parsed')
    # If there are no attachements, the weapon still needs to be inserted
   
            # print(f'Gun: {gun_name} // Attachement: {attachment_name} // Requires: {attachment_unlock_name}')

print(name_to_requirement)
with open('all_weapons_data.pickle', 'wb') as f:
        pickle.dump(name_to_requirement, f)

#__next > div > main > div.grid.grid-cols-2.gap-4 > section.col-span-2.space-y-4 > div.sm\:px-2 > div > div > table > tbody


