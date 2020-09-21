from urllib import request
import csv

from bs4 import BeautifulSoup

page_ids = [i for i in range(98, 100)]
base_url = "https://sundown.tougaloo.edu/sundowntownsshow.php?id={}"


# get_city_state took a bunch of patient trial and error
def get_city_state(soup):
    parent_table = soup.find("table")
    tbodys = parent_table.find_all("tbody")

    sundown_town_status_arr = str(tbodys[8]).split("Confirmed Sundown Town?")
    sundown_status = (
        sundown_town_status_arr[1]
        .split("</td>")[2]
        .split('<font size="-1">')[1]
        .split("</font>")[0]
    )

    city_tbody = tbodys[3]
    city_tbody_str = str(city_tbody.contents[1]).split("i>")
    city = city_tbody_str[1][:-2]
    state = city_tbody_str[2][4:6]
    return [city, state, sundown_status]


def get_page_content(page_ids, output_writer=None):
    for i in page_ids:
        if i % 500 == 0:
            print("Now parsing page at index " + str(i))
        web_url = request.urlopen(base_url.format(i))
        html_doc = web_url.read()
        soup = BeautifulSoup(html_doc, "html.parser")
        location = get_city_state(soup)
        if len(location[0]) == 0:
            continue
        # insert ID
        location.insert(0, i)
        output_writer.writerow(location)


if __name__ == "__main__":
    page_ids = [i for i in range(1, 2708)]
    # page_ids = [i for i in range(98, 105)]

    output_file = open("sundown_states.csv", "w")
    output_writer = csv.writer(output_file)

    get_page_content(page_ids, output_writer)

    output_file.close()
