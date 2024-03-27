# Scraper for PSA OpenStat Crop Prices using html5lib
import os

import mechanicalsoup
import requests
from bs4 import BeautifulSoup


def get_csv(url, filename):
    browser = mechanicalsoup.StatefulBrowser(soup_config={"features": "html5lib"})
    browser.open(url)
    page = browser.page
    form = browser.select_form('form[method="post"]')
    print(page.prettify())

    # Get VARS and OPTIONS, 1:1 mapped
    varnames = [
        var.string
        for var in page.css.select("#VariableSelection")[0].find_all(
            class_="variableselector_valuesselect_variabletitle"
        )
    ]
    varnames.append("OutputFormats")
    options = []
    selects = page.css.select("#VariableSelection")[0].find_all("select")
    for e in selects:
        options.append([opt["value"] for opt in e.find_all("option")])

    options[2] = options[2][
        :5
    ]  # hotfix to "Number of selected cells exceeds the maximum allowed 100,000"

    # print(*varnames, sep="\n")
    # print(*options, sep="\n")

    # Set OPTIONS for each VAR
    for i in range(0, len(selects) - 1):
        browser[selects[i]["name"]] = options[i]
    browser[selects[-1]["name"]] = "FileTypeCsvWithHeadingAndComma"

    # browser.form.print_summary()

    # Submit request
    response = browser.submit_selected()

    # Download CSV
    if not os.path.isdir("../datasets/prices"):
        os.mkdir("../datasets/prices")
    with open("../datasets/prices/%s.csv" % filename, "w+") as text_file:
        text_file.write(
            response.text.split("\n", 2)[2]
        )  # Remove first 2 lines from string


# Prepare URLs to be scraped
# https://openstat.psa.gov.ph/PXWeb/pxweb/en/DB/DB__2M__NFG/?tablelist=true
url = "https://openstat.psa.gov.ph/PXWeb/pxweb/en/DB/DB__2M__NFG/?tablelist=true"
base_url = "https://openstat.psa.gov.ph"
page = requests.get(url)

soup = BeautifulSoup(page.content, "html5lib")

# Collect hyperlinks from which to extract CSV files
for child in soup.ol.children:
    if child != "\n" and child.a is not None:
        table_url = base_url + child.a["href"].split("?")[0][:-1]
        if table_url[-5] == "A":
            continue  # avoid appendices
        filename = str(child.a.string.split(":")[0])
        filename = f"farmgate_{filename.lower().replace(' ', '')}"
        # print(filename, table_url)
        get_csv(table_url, filename)
