import pandas as pd
from bs4 import BeautifulSoup
import requests
import itertools
import numpy as np



rsp = requests.get('https://www.amazon.jobs/en/jobs/1726325/aws-application-security-engineer')
content = rsp.content
soup = BeautifulSoup(content)
title = soup.find("job")
description = soup.find_all("div", class_="section description")
print(title)


'''
keys = soup.find_all("dt", class_="govuk-summary-list__key")
Headings = [x.text.strip() for x in keys]
values = soup.find_all("dd", class_="govuk-summary-list__value")
title = soup.find("title")
descr = [x.text.strip() for x in values]
new_d = [title.text.strip()] + descr
new_d = np.array(new_d).reshape(1,len(new_d))
Columns = ["Title"] + Headings
df =pd.DataFrame(new_d, columns = Columns)
filt_df = df.filter(filt_col, axis=1)'''


