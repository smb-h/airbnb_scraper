import requests
from bs4 import BeautifulSoup
import sqlite3
import json


url = "https://www.airbnb.com/s/Paris--France/homes?refinement_paths%5B%5D=%2Fhomes&current_tab_id=home_tab&selected_tab_id=home_tab&screen_size=large&hide_dates_and_guests_filters=false&place_id=ChIJD7fiBh9u5kcRYJSMaMOCCwQ&s_tag=qFBLGoQ9&search_type=pagination&section_offset=5&items_offset="
response = requests.get(url)
# print(response.status_code)
# print(response.content)
soup = BeautifulSoup(response.text, 'html.parser')
# print(soup.prettify())

def get_page(pg_num):
    url = "https://www.airbnb.com/s/Paris--France/homes?refinement_paths%5B%5D=%2Fhomes&current_tab_id=home_tab&selected_tab_id=home_tab&screen_size=large&hide_dates_and_guests_filters=false&place_id=ChIJD7fiBh9u5kcRYJSMaMOCCwQ&s_tag=qFBLGoQ9&search_type=pagination&section_offset=5&items_offset="
    if pg_num > 1:
        url += str(len(homes))
    response = requests.get(url)
    return BeautifulSoup(response.text, 'html.parser')


# Pagination
active_page_number = int(soup.findAll("div", {"class": "_e602arm"})[0].text.strip())
pages = [active_page_number]
deactive_page_numbers = soup.findAll("div", {"class": "_1bdke5s"})
for div in deactive_page_numbers:
    tmp = int(div.text.strip())
    if tmp not in pages:
        pages.append(tmp)
pages = max(pages)

# Main loop
homes = []
for page in range(1, pages+1):
    soup = get_page(page)
    find_homes = soup.findAll("div", {"class": "_6kiyebe"})
    for home in find_homes:
        children = home.findChildren(recursive=False)
        children_data = [child.text for child in children if child.text]
        # print(children_data)
        homes.append(children_data)



# DB stuff
conn = sqlite3.connect('paris.db')
cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS home_table")
cur.execute('CREATE TABLE home_table (name varchar(255), description varchar(255), rating varchar(255))')
for home in homes:
    print(home)
    # QUERY =
    cur.execute(
        f'INSERT INTO home_table (name, description, rating) VALUES ({home[1]}, {home[2]}, {home[0]})'
    )

conn.commit()


conn.close()


