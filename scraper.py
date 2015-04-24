# -*- coding: utf-8 -*-

import scraperwiki
import urllib2
import urllib
import urlparse
from datetime import datetime
from bs4 import BeautifulSoup

# Set up variables
entity_id = "E1920_HCC_gov"
url = "http://www.hertsdirect.org/your-council/work/opendata/money/supplierpymtsmr250/"

# Set up functions
def convert_mth_strings ( mth_string ):
	month_numbers = {'JAN': '01', 'FEB': '02', 'MAR':'03', 'APR':'04', 'MAY':'05', 'JUN':'06', 'JUL':'07', 'AUG':'08', 'SEP':'09','OCT':'10','NOV':'11','DEC':'12' }
	#loop through the months in our dictionary
	for k, v in month_numbers.items():
		#then replace the word with the number
		mth_string = mth_string.replace(k, v)
	return mth_string

# pull down the content from the webpage
html = urllib2.urlopen(url)
soup = BeautifulSoup(html)

# find all entries with the required class
block = soup.find('ul',{'id':'lNav'})
pageLinks = block.findAll('li')

for pageLink in pageLinks:
	pageTitle = pageLink.text
	url = 'http://www.hertsdirect.org' + pageLink.a['href']
	if 'CSV' in pageTitle:
		html2 = urllib2.urlopen(url)
		soup2 = BeautifulSoup(html2)
		block = soup2.find('ul',{'class':'level1'})
		fileLinks = block.findAll('li')
  		for fileLink in fileLinks:
  			title = fileLink.text.strip()
	  		url = 'http://www.hertsdirect.org' + fileLink.a['href']
			parsed_link = urlparse.urlsplit(url.encode('utf8'))
			parsed_link = parsed_link._replace(path=urllib.quote(parsed_link.path))
			encoded_link = parsed_link.geturl()
			# create the right strings for the new filename
			csvYr = title.split(' ')[-4]
			csvMth = title.split(' ')[-5][:3]
			csvMth = csvMth.upper()
			csvMth = convert_mth_strings(csvMth);
			filename = entity_id + "_" + csvYr + "_" + csvMth + ".csv"
			todays_date = str(datetime.now())
			scraperwiki.sqlite.save(unique_keys=['l'], data={"l": url, "f": filename, "d": todays_date })
			print filename
	  
