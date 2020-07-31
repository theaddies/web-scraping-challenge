#!/usr/bin/env python
# coding: utf-8

# <h1>NASA Mars News</h1>

# In[148]:


# Dependencies
from bs4 import BeautifulSoup
from splinter import Browser
import requests
import re
import pandas as pd


# In[28]:


executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)


# In[29]:


url = 'http://mars.nasa.gov/news/'
browser.visit(url)


# In[30]:


html = browser.html
soup = BeautifulSoup(html, 'html.parser')


# In[31]:


print(soup.prettify())


# In[32]:


results = soup.find_all("div", class_= "image_and_description_container")
results


# In[33]:


news_title = []
news_p = []
for result in results:
    print("______")
    #print(result)
    try:
        news_title.append(result.find("div", class_='content_title').text)
        print(result.find("div", class_='content_title').text)
    except:
        print("")
    try:
        news_p.append(result.find("div", class_='article_teaser_body').text)
        print(result.find("div", class_='article_teaser_body').text)
    except:
        print("")


# In[34]:


news_title


# In[35]:


news_p


# <h1>JPL Mars Space Images - Featured Image</h1>

# In[320]:


url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)


# In[321]:


html = browser.html
soup = BeautifulSoup(html, 'html.parser')


# In[322]:


browser.find_by_id("full_image").click()


# In[323]:


browser.find_by_text("more info")


# In[324]:


browser.find_by_css('div[class="addthis_toolbox addthis_default_style"]')


# In[325]:


url = browser.find_by_css('div[class="addthis_toolbox addthis_default_style"]').find_by_css('a').last['href']


# In[326]:


browser.find_by_css('div[class="addthis_toolbox addthis_default_style"]').find_by_css('a').last.click()


# In[327]:


print(url)


# In[328]:


browser.visit(url)


# In[329]:


html = browser.html
soup = BeautifulSoup(html, 'html.parser')


# In[330]:


p_tag = soup.find_all('aside')[0].find_all('p')


# In[331]:


soup.find_all('aside')[0].find_all('p')[6].text


# In[333]:


for p in p_tag:
    print(p)
    if 'Full-Res JPG:' in p.text:
        featured_image_url = 'https:'+p.a['href']


# In[334]:


featured_image_url


# <h1>Mars Weather</h1>

# In[341]:


url = 'https://twitter.com/marswxreport?lang=en'
browser.visit(url)


# In[342]:


html = browser.html
soup = BeautifulSoup(html, 'html.parser')


# In[343]:


results = soup.find_all('span')


# In[344]:


i=0
found = False
for result in results:
    i=i+1
    if (('low' in result.text) & ('C' in result.text) &  (not found)):
        print(result)
        print(i)
        mars_weather = result.text
        found = True


# In[345]:


mars_weather


# <h1>Mars Facts</h1>

# In[159]:


mars_facts_url = 'https://space-facts.com/mars/'


# In[160]:


facts_list = pd.read_html(mars_facts_url)


# In[161]:


facts_df = facts_list[0]


# In[165]:


facts_df.columns = ["measure", "value"]
facts_df


# In[166]:


facts_df.set_index('measure', inplace = True)


# In[167]:


facts_df


# In[168]:


facts_df.to_html('mars_fact_table.html')


# <h1>Mars Hemispheres</h1>

# In[287]:


url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)


# In[288]:


html = browser.html
soup = BeautifulSoup(html, 'html.parser')


# In[289]:


results = soup.find_all('div', class_ = "item")


# In[279]:


results[0]


# In[290]:


for result in results:
    print(result)


# In[307]:


hemisphere_link = []
enhanced_hemisphere_link = []
hemisphere_name = []
i = 0
for result in results:
    i=i+1
    if result.find('a', class_ = "itemLink product-item"):
        print("---------------------")
        print(i)
        print(result)
        hemisphere_label = result.find_all('a', class_ = "itemLink product-item")[0].find('img')['alt']
        split_name = hemisphere_label.split()
        remove_words = ['Enhanced', 'thumbnail']
        print(split_name)
        result_words  = [word for word in split_name if word not in remove_words]
        hemisphere_name.append(" ".join(result_words))
        print(hemisphere_name)
        print(result.find_all('a', class_ = "itemLink product-item")[0]['href'])
        #print(result.find_by_css('a[class="itemLink product-item"]').find_by_css('h3').text)
        hemisphere_link.append(result.find_all('a', class_ = "itemLink product-item")[0]['href'])


# In[276]:


results[0].find_by_css('a[class="itemLink product-item"]')


# In[308]:


hemisphere_link


# In[309]:


hemisphere_name


# In[312]:


for i in range(0,4):
    browser.visit('https://astrogeology.usgs.gov/'+hemisphere_link[i])
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    enhanced_hemisphere_link.append(soup.find_all('ul')[0].find_all('li')[1].find('a')['href'])


# In[313]:


enhanced_hemisphere_link


# In[350]:


mars_data = {'news_title' : news_title, 'news_p' : news_p, 'featured_image_url' : featured_image_url,             'mars_weather' : mars_weather, 'hemisphere_name' : hemisphere_name, 'enhanced_hemisphere_link' :            enhanced_hemisphere_link}


# In[351]:


mars_data

