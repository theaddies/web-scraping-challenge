from flask import Flask, render_template
import pymongo
from bs4 import BeautifulSoup
from splinter import Browser
import requests
import re
import pandas as pd

executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)

url = 'http://mars.nasa.gov/news/'
browser.visit(url)

html = browser.html
soup = BeautifulSoup(html, 'html.parser')

results = soup.find_all("div", class_= "image_and_description_container")

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

# <h1>JPL Mars Space Images - Featured Image</h1>

url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)

html = browser.html
soup = BeautifulSoup(html, 'html.parser')

url = browser.find_by_css('div[class="addthis_toolbox addthis_default_style"]').find_by_css('a').last['href']

browser.find_by_css('div[class="addthis_toolbox addthis_default_style"]').find_by_css('a').last.click()

browser.visit(url)

html = browser.html
soup = BeautifulSoup(html, 'html.parser')

p_tag = soup.find_all('aside')[0].find_all('p')

soup.find_all('aside')[0].find_all('p')[6].text

for p in p_tag:
    print(p)
    if 'Full-Res JPG:' in p.text:
        featured_image_url = 'https:'+p.a['href']

# <h1>Mars Weather</h1>

url = 'https://twitter.com/marswxreport?lang=en'
browser.visit(url)

html = browser.html
soup = BeautifulSoup(html, 'html.parser')

results = soup.find_all('span')

i=0
found = False
for result in results:
    i=i+1
    if (('low' in result.text) & ('C' in result.text) &  (not found)):
        print(result)
        print(i)
        mars_weather = result.text
        found = True

mars_weather

# <h1>Mars Facts</h1>

mars_facts_url = 'https://space-facts.com/mars/'

facts_list = pd.read_html(mars_facts_url)

facts_df = facts_list[0]

facts_df.columns = ["measure", "value"]
facts_df

facts_df.set_index('measure', inplace = True)

facts_df.to_html('mars_fact_table.html')

# <h1>Mars Hemispheres</h1>

url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)

html = browser.html
soup = BeautifulSoup(html, 'html.parser')

results = soup.find_all('div', class_ = "item")

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

for i in range(0,4):
    browser.visit('https://astrogeology.usgs.gov/'+hemisphere_link[i])
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    enhanced_hemisphere_link.append(soup.find_all('ul')[0].find_all('li')[1].find('a')['href'])

mars_data = {'news_title' : news_title, 'news_p' : news_p, 'featured_image_url' : featured_image_url,             'mars_weather' : mars_weather, 'hemisphere_name' : hemisphere_name, 'enhanced_hemisphere_link' :            enhanced_hemisphere_link}

mars_data


