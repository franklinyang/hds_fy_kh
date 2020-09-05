from urllib import request
import csv
import os

from bs4 import BeautifulSoup

page_ids = [i for i in range(98, 100)]
base_url = "https://sundown.tougaloo.edu/sundowntownsshow.php?id={}"


# TODO (9/4): DRY up with ./grab_sunset_town_data.py... copy+pasta for now
def get_city_state(soup):
    parent_table = soup.find("table")
    tbodys = parent_table.find_all("tbody")

    city_tbody = tbodys[3]
    city_tbody_str = str(city_tbody.contents[1]).split("i>")
    city = city_tbody_str[1][:-2]
    state = city_tbody_str[2][4:6]
    return [city, state]


# save page contents to ../data/html_dump
if __name__ == "__main__":
    html_dir = "../data/html_dump"
    # page_ids = [i for i in range(1, 2708)]
    page_ids = [i for i in range(98, 105)]

    for i in page_ids:
        web_url = request.urlopen(base_url.format(i))
        html_doc = web_url.read()
        soup = BeautifulSoup(html_doc, "html.parser")
        location = get_city_state(soup)
        if len(location[0]) == 0:
            continue

        output_filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), html_dir)
        output_file = open("{}/{}.html".format(output_filepath, i), "w")
        output_file.write(str(html_doc))
        output_file.close()
