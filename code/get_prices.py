'''Scraper for PSA OpenStat Crop Prices using html.parser.
Tested on New Series or 2018-based datasets from PSA.
Tested on Farmgate, Wholesale, Retail, and Dealers prices.
Still bugged for CPI.
'''
# NOTE: Must be run with cwd at repo root
import os

import mechanicalsoup
import requests
import re
import bs4
from bs4 import BeautifulSoup

# GLOBAL PARAMETERS
debug = False
base_url = "https://openstat.psa.gov.ph"
url_file = "code/get_prices_urls.txt"
writepath = "datasets/prices"
# Plop all URLs to be scraped in url_file.
# URL pages must have the same format as https://openstat.psa.gov.ph/PXWeb/pxweb/en/DB/DB__2M__NFG/?tablelist=true
# Files will be output onto writepath

#######################

def del_attrib_from_children_of_tag(tag: bs4.Tag, attrib: str, parent=True):
    """BUG: tag.next_sibling can be a newline '\\n'"""
    if parent and isinstance(tag, bs4.Tag):
        del_attrib_from_children_of_tag(tag.contents[0], attrib, False)
    elif isinstance(tag, bs4.Tag):
        del tag[attrib]
        del_attrib_from_children_of_tag(tag.next_sibling, attrib, False)
    else:
        del_attrib_from_children_of_tag(tag.next_sibling, attrib, False)

def get_csv(url, filename):
    browser = mechanicalsoup.StatefulBrowser(soup_config={"features": "html.parser"})
    browser.open(url)
    page: bs4.BeautifulSoup = browser.page
    browser.select_form('form[method="post"]')
    # Important attributes: browser.page (a soup object) and browser.form
    # print(page.prettify())

    # Get VARS list and OPTIONS list, 1:1 mapped
    # NOTE: varnames only used for debugging
    varnames = [
        var.string
        for var in page.select_one("#VariableSelection").find_all(
            class_ = "variableselector_valuesselect_variabletitle"
        )
    ]
    varnames.append("OutputFormats")
    
    options = []
    select_tags = page.select_one("#VariableSelection").find_all("select")
    # print(*selects, sep="\n")
    for e in select_tags:
        e: bs4.Tag
        options.append([opt["value"] for opt in e.find_all("option")])

    # hotfix to "Number of selected cells exceeds the maximum allowed 100,000"
    # Download per year, then join the tables
    # <option selected="selected" value="14">2024</option>
    value_year = {}
    year_opts = page.find_all(name="option", string=re.compile("[1-3][0-9]{3}"))
    year_var_name = year_opts[0].parent["name"]
    year_var_tag = page.find(attrs={"name": year_var_name})
    for e in year_opts:
        e: bs4.Tag
        value_year[e["value"]] = e.string
    print(value_year)   # {'14': '2024', '13': '2023', '12': '2022', '11': '2021',...}
        
    print(*varnames, sep="\n")
    print(*options, sep="\n")

    # # Set OPTIONS for each VAR (including year var, but reset later)
    for i in range(len(select_tags)-1):
        browser[select_tags[i]["name"]] = options[i]
    browser[select_tags[-1]["name"]] = "FileTypeCsvWithHeadingAndComma"

    # Delete selected tag from selected year options
    def clear(tag: bs4.Tag, attrib: str):       
        for opt in tag.children:
            if opt != "\n":
                del opt[attrib]

    # Submit request for each year, download each csv
    # <option selected="selected" value="13">2023</option>
    # <option value="12">2022</option>
    for key in value_year:
        clear(year_var_tag, "selected")
        browser[year_var_name] = key
        year = value_year[key]
        response = browser.submit_selected(update_state=False)
        # browser.form.print_summary()

        ## Download CSV
        with open(f"{filename}_{year}.csv", "w+", encoding="utf-8") as f:
            # Remove first 2 lines from string
            f.write(response.text.split("\n", 2)[2])


# Prepare output directory
if not os.path.exists(writepath):
    os.makedirs(writepath)

# Scrape URLs
with open(url_file) as f:
    for line in f:
        url = line.strip()
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")

        # Collect hyperlinks from which to extract CSV files
        # <a class="tablelist_linkHeading" href="/PXWeb/pxweb/en/DB/DB__2M__NFG/0032M4AFN01.px/?rxid=be2fff00-cee9-476f-9893-bdbf5199d519" id="ctl00_ContentPlaceHolderMain_TableList1_TableList1_LinkItemList_ctl01_lnkTableListItemText">Cereals: Farmgate Prices by Geolocation, Commodity, Year and Period</a>
        # https://openstat.psa.gov.ph/PXWeb/pxweb/en/DB/DB__2M__NFG/0032M4AFN01.px
        # cereals
        # farmgate
        # datasets/prices/farmgate_cereals
        for child in soup.ol.children:
            if child != "\n" and child.a is not None:
                table_url = base_url + child.a["href"].split("?")[0][:-1]
                if table_url[-5] == "A":
                    continue  # avoid appendices
                print(table_url)
                text = str(child.a.string)
                if "CPI" in table_url:
                    text = text.replace("Consumer Price Index", "cpi")
                    text = text.replace("Commodity Group", "cg")
                    text = text.replace("Year-on-Year", "yoy")
                    print(text)
                    text = re.sub("\(.*\)", "", text)
                    product = text.lower().replace(' ', '')
                    price_type = "cpi"
                elif ":" in text:
                    product = text.split(':')[0].lower().replace(' ', '')
                    price_type = text.split(':')[1].lower().split()[0]
                else:
                    product = text.lower().replace('\'', '').split()[-1]
                    price_type = text.lower().replace('\'', '').split()[0]
                filename = f"{writepath}/{price_type}_{product}"
                print(filename)
                get_csv(table_url, filename)
                break
