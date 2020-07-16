import requests
from bs4 import BeautifulSoup
import xlsxwriter
import pandas as pd


city = str(input('City:'))
state = str(input('State (Use the two character code ex: Texas -> Tx):'))

url = "https://www.trulia.com/" + state + "/" + city

req = requests.get(url, headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})

content = req.content

soup = BeautifulSoup(content, 'html.parser')

all_property_data = soup.find_all("div", {"class":"Box-sc-8ox7qa-0 jDcCbK"})

workbook = xlsxwriter.Workbook('property_data.xlsx')
worksheet = workbook.add_worksheet()

worksheet.write('A1', 'Price')
worksheet.write('B1', 'Beds')
worksheet.write('C1', 'Bath')
worksheet.write('D1', 'Address')
worksheet.write('E1', 'Region')


for i in range (0, len(all_property_data)):
    property_price = all_property_data[i].find_all("div", {"data-testid":"property-price"})
    property_beds = all_property_data[i].find_all("div", {"data-testid": "property-beds"})
    property_baths = all_property_data[i].find_all("div", {"data-testid": "property-baths"})
    property_address = all_property_data[i].find_all("div", {"data-testid":"property-street"})
    property_region = all_property_data[i].find_all("div", {"data-testid": "property-region"})
    if property_price:
        property_price = property_price[0].text
    else:
        property_price = "$0"
    if property_beds:
        property_beds = property_beds[0].text
    else:
        property_beds = "0bd"
    if property_baths:
        property_baths = property_baths[0].text
    else:
        property_baths = "0ba"
        
    if property_address:
        property_address = property_address[0].text
    else:
        property_address = ""
    if property_region:
        property_region = property_region[0].text
    else:
        property_region = ""
    
    row_a = ["A", str(i+2)]
    row_b = ["B", str(i+2)]
    row_c = ["C", str(i+2)]
    row_d = ["D", str(i+2)]
    row_e = ["E", str(i+2)]
    
    worksheet.write(''.join(row_a), property_price)
    worksheet.write(''.join(row_b), property_beds)
    worksheet.write(''.join(row_c), property_baths)
    worksheet.write(''.join(row_d), property_address)
    worksheet.write(''.join(row_e), property_region)
    

workbook.close()

df = pd.read_excel("hello.xlsx")
df.to_html("spreadsheet.html")
