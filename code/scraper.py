'''Scraper for PSA OpenStat Crop Prices using html.parser. Parallelized version.
Tested on New Series or 2018-based datasets from PSA.
Tested on Farmgate, Wholesale, Retail, and Dealers prices.
Would likely work for other PSA datasets, as long as they have a Year variable.
Still bugged for CPI. Dataset too big even when downloaded per year,
must also be downloaded per month (breaks if bycg or byregion).
'''
# NOTE: Must be run with cwd at repo root
import os

import mechanicalsoup
import re
import bs4
import multiprocessing as mp
import time

# GLOBAL PARAMETERS
debug = False
base_url = "https://openstat.psa.gov.ph"
url_file = "code/get_crop-value-prod.txt"
writepath = "datasets/new"
parallel_mode = True
# Plop all URLs to be scraped in url_file.
# NOTE: URL pages must have the same format as https://openstat.psa.gov.ph/PXWeb/pxweb/en/DB/DB__2M__NFG/?tablelist=true
# Files will be output onto writepath

#######################

def get_csv(args):
    url, filename = args
    print(url)
    print(filename)
    
    browser = mechanicalsoup.StatefulBrowser(soup_config={"features": "html.parser"})
    status = browser.open(url).status_code
    if status != 200:
        print("Breaking operation: Failed to establish connection.")
        return
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
    if "year" not in [var.lower() for var in varnames]:
        print("Breaking operation: No year variable in dataset.")
        print("=============\n")
        return
    
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
    year_opts = page.find_all(name="option", string=re.compile("(19|20)[0-9]{2}"))
    year_var_name = year_opts[0].parent["name"]
    year_var_tag = page.find(attrs={"name": year_var_name})
    for e in year_opts:
        e: bs4.Tag
        value_year[e["value"]] = e.string
    # print(value_year)   # {'14': '2024', '13': '2023', '12': '2022', '11': '2021',...}
        
    # print(*varnames, sep="\n")
    # print(*options, sep="\n")

    # # Set OPTIONS for each VAR (including year var, but reset later)
    for i in range(len(select_tags)-1):
        browser[select_tags[i]["name"]] = options[i]
    browser[select_tags[-1]["name"]] = "FileTypeCsvWithHeadingAndComma"
    
    # Attempt to download the entire thing already
    failed = False
    with open(f"{filename}.csv", "w+", encoding="utf-8") as f:
        response = browser.submit_selected(update_state=False)
        # response:: header content-type is "text/html; charset=utf-8" for failed fetch,
        # and application/octet-stream for successful fetch
        if response.headers["content-type"] == "text/html; charset=utf-8":
            failed = True
            print(f"Failed to download entire thing: {filename}")
        if not failed:
            print(f"{filename}.csv")
            # Remove first 2 lines from string
            f.write(response.text.split("\n", 2)[2])
            return

    # Delete selected tag from selected year options
    def clear(tag: bs4.Tag, attrib: str):       
        for opt in tag.children:
            if opt != "\n":
                del opt[attrib]

    # Submit request for each year, download each csv
    # <option selected="selected" value="13">2023</option>
    # <option value="12">2022</option>
    failed = False
    for key in value_year:
        clear(year_var_tag, "selected")
        browser[year_var_name] = key
        year = value_year[key]
        response = browser.submit_selected(update_state=False)
        # response:: header content-type is "text/html; charset=utf-8" for failed fetch,
        # and application/octet-stream for successful fetch
        if response.headers["content-type"] == "text/html; charset=utf-8":
            failed = True
            break

        ## Download CSV
        with open(f"{filename}_{year}.csv", "w+", encoding="utf-8") as f:
            print(f"{filename}_{year}.csv")
            # Remove first 2 lines from string
            f.write(response.text.split("\n", 2)[2])
                
    if not failed:
        print("=============\n")
        return
    
    # Reattempt with per year, per month (period) this time
    # NOTE: period is month (I assume)
    if "period" not in [var.lower() for var in varnames]:
        print("Breaking operation: No month variable in dataset.")
        print("=============\n")
        return
    
    value_month = {}
    temp: bs4.Tag = page.find(name="span", string=re.compile("Period|Month", re.IGNORECASE))
    month_opts = list(temp.parents)[2].find_all(name="option")
    month_var_name = month_opts[0].parent["name"]
    month_var_tag = page.find(attrs={"name": month_var_name})
    # e is an <option> tag
    for e in month_opts:
        e: bs4.Tag
        value_month[e["value"]] = e.string
    # print(value_month)   # {'12': 'Ave', '11': 'Dec', '10': 'Nov', '9': 'Oct',...}
    
    failed = False
    for key1 in value_year:
        clear(year_var_tag, "selected")
        browser[year_var_name] = key1
        year = value_year[key1]
        
        for key2 in value_month:
            clear(month_var_tag, "selected")
            browser[month_var_name] = key2
            month = value_month[key2]
            response = browser.submit_selected(update_state=False)
            if response.status_code != 200:
                # BUG: Not ours, but PSA's, gateway timeout on certain datasets
                print(f"Bad response ({response.status_code}) (Year: {year})")
                print("Attempting something drastic...\n")
                failed = True
                continue
            # browser.form.print_summary()

            ## Download CSV
            with open(f"{filename}_{year}_{month}.csv", "w+", encoding="utf-8") as f:
                print(f"{filename}_{year}_{month}.csv")
                # Remove first 2 lines from string
                f.write(response.text.split("\n", 2)[2])
        else:
            continue
        break
    
    if not failed:
        print("=============\n")
        return
    
    # Reattempt with per year, per geolocation this time
    if "geolocation" not in [var.lower() for var in varnames]:
        print("Breaking operation: No geolocation variable in dataset.")
        print("=============\n")
        return
    
    value_geol = {}
    temp: bs4.Tag = page.find(name="span", string=re.compile("Geolocation", re.IGNORECASE))
    geol_opts = list(temp.parents)[2].find_all(name="option")
    geol_var_name = geol_opts[0].parent["name"]
    geol_var_tag = page.find(attrs={"name": geol_var_name})
    # e is an <option> tag
    for e in geol_opts:
        e: bs4.Tag
        value_geol[e["value"]] = e.string
    # print(value_geol)   # {'12': 'Ave', '11': 'Dec', '10': 'Nov', '9': 'Oct',...}
    
    # Reselect all months (assumes Period is the penultimate variable)
    browser[month_var_name] = options[-2]
    
    for key1 in value_year:
        clear(year_var_tag, "selected")
        browser[year_var_name] = key1
        year = value_year[key1]
        
        for key2 in value_geol:
            clear(geol_var_tag, "selected")
            browser[geol_var_name] = key2
            geol = value_geol[key2].strip(".")
            response = browser.submit_selected(update_state=False)
            if response.status_code != 200:
                # BUG: Not ours, but PSA's, gateway timeout on certain datasets
                print(f"Bad response ({response.status_code}) (Geolocation: {geol})\n")
                continue
            # browser.form.print_summary()

            ## Download CSV
            with open(f"{filename}_{year}_{geol}.csv", "w+", encoding="utf-8") as f:
                # Remove first 2 lines from string
                print(f"{filename}_{year}_{geol}.csv")
                f.write(response.text.split("\n", 2)[2])    
                
    print("=============\n")


if __name__ == "__main__":
    # Prepare URLs that will be scraped
    table_urls = []
    filenames = []
    with open(url_file) as f:
        for line in f:
            url = line.strip()
            browser = mechanicalsoup.StatefulBrowser()
            print(browser.open(url).status_code)        # don't comment out this line
            soup = browser.page
            # soup = BeautifulSoup(page, "html.parser")
            print("OK:", url)
            time.sleep(5)
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
                    text = str(child.a.string)
                    if "CPI" in table_url:
                        text = text.replace("Consumer Price Index", "cpi")
                        text = text.replace("Commodity Group", "cg")
                        text = text.replace("Year-on-Year", "yoy")
                        text = text.replace("(2018=100)", "")
                        # print(text)
                        text = re.sub("\(Backcasted Values\)?", "", text).strip()
                        product = text.lower().replace(' ', '').split(":")[0]
                        price_type = "cpi"
                    elif ":" in text:
                        product = text.split(':')[0].lower().replace(' ', '')
                        price_type = text.split(':')[1].lower().split()[0]
                    else:
                        product = text.lower().replace('\'', '').split()[-1]
                        price_type = text.lower().replace('\'', '').split()[0]
                        
                    nestedpath = f"{writepath}/{price_type}"
                    if not os.path.exists(nestedpath):
                        os.makedirs(nestedpath)
                        
                    filename = f"{nestedpath}/{price_type}_{product}"
                    table_urls.append(table_url)
                    filenames.append(filename)

    # Scrape URLs, may be done in parallel
    args = [pair for pair in zip(table_urls, filenames)]
    if parallel_mode:
        pool_size = mp.cpu_count()
        with mp.Pool(pool_size) as pool:
            pool.map(get_csv, args)
    else:
        for pair in args:
            get_csv(pair)
