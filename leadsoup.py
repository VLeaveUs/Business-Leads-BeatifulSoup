
# coding: utf-8

# In[1]:


import requests
import xlwt
from bs4 import BeautifulSoup


# In[2]:


# Requesting the HTML script of the website
baseURL = 'https://www.science-park.co.uk'
URL = 'https://www.science-park.co.uk/about-the-park/business-directory' # add here target website
page = requests.get(URL)

# Creating Soup Object
soup = BeautifulSoup(page.content, 'html.parser')

# print(soup.prettify()) # -- print interpretably if needed


# In[3]:


# adjusting soup to include container with business info
targclass = soup.find_all('div', class_='l-container c-business__list')

# idenitfying bussinesses' web links
targlinks = []  # links stored here
for class1 in targclass:
    targattr = class1.find_all('a')
for attr in targattr:
    targlinks.append(attr['href'])
targlinks


# In[4]:


# creating workbook to export data to
scrapDB = xlwt.Workbook()

# create sheet and format
sheet1 = scrapDB.add_sheet('Science Park', cell_overwrite_ok=True)
style = xlwt.easyxf('font: bold 1') 

# column titles
sheet1.write(0, 0, 'NAME', style)
sheet1.write(0, 1, 'WEBSITE', style) 
sheet1.write(0, 2, 'LOCATION', style) 
sheet1.write(0, 3, 'EMAIL', style)
sheet1.write(0, 4, 'TEL', style) 


# In[ ]:


# Exporting target bussiness data to workbook - name, website, location, tel.number, email
print('Filling workbook and noting incosistent insertions:\n')

for num, link in enumerate(targlinks, 1):
    name = link.split('/')
    name = name[-1] # name 
    sheet1.write(num, 0, name)

    compURL = baseURL + link
    nextpage = requests.get(compURL) # switching to bussiness' websites for the data
    soup2 = BeautifulSoup(nextpage.content, 'html.parser')
    buzzclass = soup2.find_all('div', class_='o-info')
    for class2 in buzzclass:
        buzzdets = class2.find_all('a')
        #print(buzzdets)
    col_num = 1  # workbook col count
    for detail in buzzdets:
        
        if col_num == 1:  # post-data-cleaning
            strweb = detail['href']
            if (('www' not in strweb) or ('maps' in strweb)):
                col_num = col_num + 1
                print(strweb)
            else:
                pass
        elif col_num == 2:
            strloc = detail['href']
            if 'maps' not in strloc:
                col_num = col_num + 1
                print(strloc)
            else:
                pass
        elif col_num == 3:
            strmail = detail['href']
            if '@' not in strmail:
                col_num = col_num + 1
                print(strmail)
            else:
                pass
        else:
            pass
        
        sheet1.write(num, col_num, detail['href'])
        col_num = col_num + 1

scrapDB.save('sciencepark_soup.xls') # saving workbook on local dir
    


# In[ ]:


get_ipython().system('jupyter nbconvert --to script leadsoup.ipynb # exporting to script -- comment out if running it')

