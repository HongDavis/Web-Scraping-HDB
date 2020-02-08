# Last run in April 2019
import pandas as pd
import requests
from lxml import html, etree

# Function to scrap and return web data
def scrapedata(url):
    d=requests.get(url)
    rootdata=html.fromstring(d.content)
    return rootdata

hdblist = [] # Create a list to store scraped data

# Web pages of iProperty hosting 4 room HDBs 
url = 'https://www.iproperty.com.sg/sale/hdb/?bedroom=3&maxPrice=400000&sortBy=price-asc'

for i in range(1,20): # Assuming HDB flats listing is more than a page but less than 20.
    if i > 1:
        rootdata = scrapedata(url + '&page=' + str(i))
    else:
        rootdata = scrapedata(url)
        
    for rrd in rootdata.xpath('//ul[@class="listing-list sc-jCHZzo fOyaAy"]/li[contains(@class, "sale")]/div/div[@class="sc-mrBlX dsRzxL"]'):
        recordlist={} # Create a dictionary to hold data temporary
        for rrd1 in rrd.xpath('div[@class="sc-dyKSPo jcIdSe"]'):
            #print(rrd1.xpath('div/h2/text()')) # Property agent name and property agent
            #print(rrd1.xpath('div/div/p/text()')) # Ad 'posted on' date
            agent = rrd1.xpath('div/h2/text()') # Property agent name and property agent
            postondate = rrd1.xpath('div/div/p/text()') # Ad 'posted on' date
            recordlist['agent'] = agent[0][0:]
            recordlist['postondate'] = postondate[0][0:]
        for rrd1 in rrd.xpath('div[@class="sc-gXPbch icSkIZ"]'):
            for rrd2 in rrd1.xpath('div[@class="sc-inlrYM bmRfcO"]'):
                #print(rrd2.xpath('div/div/a/@href')) # Sales ad reference number
                #print(rrd2.xpath('div/div/a/ul/li/text()')) # Price
                #print(rrd2.xpath('div/p/a/text()')) # Price PSF
                ref = rrd2.xpath('div/div/a/@href') # Sales ad reference number
                price = rrd2.xpath('div/div/a/ul/li/text()') # Price
                psf = rrd2.xpath('div/p/a/text()') # Price PSF
                recordlist['ref'] = ref[0][9:]
                recordlist['price S$'] = int(price[0][4:].replace(',',''))
                if len(psf) != 0:
                # Remove text 'Price PSF SGD' and convert numerical value to float.
                    recordlist['psf S$'] = float(psf[0][14:-1])
            for rrd2 in rrd1.xpath('div[@class="sc-bRbqnn ciWdWU"]'):
                #print(rrd2.xpath('div/p/a/text()')) # Address 1
                #print(rrd2.xpath('div/a/text()')) # Address 2
                add1 = rrd2.xpath('div/p/a/text()') # Address 1
                add2 = rrd2.xpath('div/a/text()') # Address 2
                recordlist['add1'] = add1[0][0:]
                recordlist['add2'] = add2[0][0:]
                recordlist['neigbourhood'] = recordlist['add1'].split(',')[0]
                recordlist['postal'] = add2[0][-6:]
            for rrd2 in rrd1.xpath('div[@class="sc-kVyEtE cqMWQp"]'):
                #print(rrd2.xpath('a/text()')) # Description of the flat eg, 4 Room HDB Flat
                des = rrd2.xpath('a/text()') # Description of the flat eg, 4 Room HDB Flat 
                recordlist['des'] = des[0][0:]
            for rrd2 in rrd1.xpath('div[@class="sc-lewbHj djZatJ"]'):
                #print(rrd2.xpath('div/ul/li/a[@class="attrs-price-per-unit-desktop"]/text()')) # Built up area
                #print(rrd2.xpath('div/ul/li[contains(@class,"bedroom-facility")]/a/text()')) # Number of bed rooms
                #print(rrd2.xpath('div/ul/li[contains(@class,"bathroom-facility")]/a/text()')) # Number of toilets
                try:
                    builtuparea = rrd2.xpath('div/ul/li/a[@class="attrs-price-per-unit-desktop"]/text()')
                    noofrooms = rrd2.xpath('div/ul/li[contains(@class,"bedroom-facility")]/a/text()')
                    nooftoilets = rrd2.xpath('div/ul/li[contains(@class,"bathroom-facility")]/a/text()')
                    recordlist['builtuparea'] = int([int(s) for s in builtuparea[0].split() if s.isdigit()][0])
                    recordlist['noofrooms'] = noofrooms[0]
                    recordlist['nooftoilets'] = nooftoilets[0]
                except IndexError:
                    break
        hdblist.append(recordlist)
# import data into a pandas dataframe
resalehdb = pd.DataFrame(hdblist)

cols = ['neigbourhood','add1','add2','postal','des','builtuparea','noofrooms','nooftoilets','price S$','psf S$','agent','ref']
resalehdb = resalehdb[cols]
resalehdb.sort_values(['neigbourhood','builtuparea'], axis=0, ascending=[True,False], inplace=True, kind='quicksort')
resalehdb['psf S$'].fillna(recordlist['price S$']/recordlist['builtuparea'],inplace = True)

resalehdb.to_csv("iProperty.csv", sep = ',', index = False)
print('Data saved')