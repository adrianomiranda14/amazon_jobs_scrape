# -*- coding: utf-8 -*-

"""
1. Need to create a function to pull the last page through, find the number, and input in the range for page_urls to pull through the agreement urls for all the agreements.
2. 3. Can I calc whether the advert is live or not absed on the dates?
4. Compile the data into one dataframe
5. Store df on shared drive"""


import pandas as pd
from bs4 import BeautifulSoup
import requests
import itertools
import numpy as np

def get_dg_marketplace_links(url):
  """This function goes to a marketplace page and extracts the individual urls for each specialist opportunity"""  
  rsp = requests.get(url)
  content = rsp.content
  soup = BeautifulSoup(content)
  fw = soup.find_all("a",class_="govuk-link")
  links = [link.get('href') for link in fw]
  cl_links = [l for l in links if l.startswith('/digital-outcomes-and-specialists/opportunities/')]
  df = pd.DataFrame([cl_links])
  return cl_links

#This makes a request to work out the total amount of marketplace pages there will be, and then creates a url 
rsp = requests.get('https://www.digitalmarketplace.service.gov.uk/digital-outcomes-and-specialists/opportunities?lot=digital-specialists')
content = rsp.content
soup = BeautifulSoup(content)
keys = soup.find_all('span', class_='dm-pagination__link-label')
pages = [x.text.strip() for x in keys]
numbers = [int(s) for s in pages[0].split() if s.isdigit()]

page_urls=[]
for x in range(1,numbers[1]+1):
  url="https://www.digitalmarketplace.service.gov.uk/digital-outcomes-and-specialists/opportunities?page="+str(x)+"&lot=digital-specialists"
  page_urls.append(url)

#This creates a list of lists of all the specialist urls by passing through the page urls
spec_urls = []
for x in page_urls:
  y = get_dg_marketplace_links(x)
  spec_urls.append(y)

#spec_urls is a list of lists, this coverts into one list
#x = spec_urls
merge_urls = (list(itertools.chain.from_iterable(spec_urls)))
print(merge_urls)

#This adds the inital part of the url to all the merge_urls to complete them
all_urls = []
for x in merge_urls:
  url="https://www.digitalmarketplace.service.gov.uk"+ str(x)
  all_urls.append(url)

len(all_urls)

filt_col = ['Title',
 'URL',
 'Published',
 'Closing date for applications',
 'Specialist role',
 'Summary of the work',
 'Latest start date',
 'Expected contract length',
 'Location',
 'Organisation the work is for',
 'Maximum day rate',
 'Who the specialist will work with',
 'What the specialist will work on',
 'Additional terms and conditions',
 'Working arrangements',
 'Security clearance',
 'Additional terms and conditions',
 'Essential skills and experience',
 'Nice-to-have skills and experience',
 'How many specialists to evaluate']

#This function gets the information from the inidividual specialist page urls, the title, headings and info and puts together into a df
# At the moment some pages seem to have slightly different data structures and titles, more analysis required plus a normalisation of this data to concat the df properly
def get_info(indi_urls):
  rsp = requests.get(indi_urls)
  content = rsp.content
  soup = BeautifulSoup(content)
  keys = soup.find_all("dt", class_="govuk-summary-list__key")
  Headings = [x.text.strip() for x in keys]
  values = soup.find_all("dd", class_="govuk-summary-list__value")
  title = soup.find("title")
  descr = [x.text.strip() for x in values]
  new_d = [title.text.strip()] + descr
  new_d = np.array(new_d).reshape(1,len(new_d))
  Columns = ["Title"] + Headings 
  df =pd.DataFrame(new_d, columns = Columns)
  filt_df = df.filter(filt_col, axis=1)
  return filt_df

# The iterative function that compiles all of the df together into one list
df2 = []
for x in all_urls:
  y = get_info(x)
  df2.append(y)

df2

#The merging function for the dfs
final_df = pd.concat(df2)

final_df.shape

#My test function, only performs the above function on one page

rsp = requests.get('https://www.digitalmarketplace.service.gov.uk/digital-outcomes-and-specialists/opportunities/15219')
content = rsp.content
soup = BeautifulSoup(content)
keys = soup.find_all("dt", class_="govuk-summary-list__key")
Headings = [x.text.strip() for x in keys]
values = soup.find_all("dd", class_="govuk-summary-list__value")
title = soup.find("title")
descr = [x.text.strip() for x in values]
new_d = [title.text.strip()] + descr
new_d = np.array(new_d).reshape(1,len(new_d))
Columns = ["Title"] + Headings 
df =pd.DataFrame(new_d, columns = Columns)
descr

filt_ind = [0,1,2,4,5,7,8,9,10,11,12,14,15,19,17,18,19,20,21,22]
filt_col = []
for x in filt_ind:
  y = Columns[x]
  filt_col.append(y)

filt_col
filt_col = ['Title',
 'URL',
 'Published',
 'Closing date for applications',
 'Specialist role',
 'Summary of the work',
 'Latest start date',
 'Expected contract length',
 'Location',
 'Organisation the work is for',
 'Maximum day rate',
 'Who the specialist will work with',
 'What the specialist will work on',
 'Additional terms and conditions',
 'Working arrangements',
 'Security clearance',
 'Additional terms and conditions',
 'Essential skills and experience',
 'Nice-to-have skills and experience',
 'How many specialists to evaluate']

rsp = requests.get('https://www.digitalmarketplace.service.gov.uk/digital-outcomes-and-specialists/opportunities/7923')
content = rsp.content
soup = BeautifulSoup(content)
keys = soup.find_all("dt", class_="govuk-summary-list__key")
Headings = [x.text.strip() for x in keys]
values = soup.find_all("dd", class_="govuk-summary-list__value")
descr = [x.text.strip() for x in values]
title = soup.find("title")
new_d = [title.text.strip()] + ['https://www.digitalmarketplace.service.gov.uk/digital-outcomes-and-specialists/opportunities/7923'] + descr
columns = ["Title"] + ['https://www.digitalmarketplace.service.gov.uk/digital-outcomes-and-specialists/opportunities/7923'] + Headings
thing = dict(zip(columns, new_d))
thing

rows = [thing for i in range(0,10)]
pd.DataFrame(rows)

#'Make this function adaptive to today's date
final_df.to_csv('/content/drive/MyDrive/Digital Marketplace Scrape/2021_08_16 Digital Marketplace.csv')

