#!/usr/bin/env python
# coding: utf-8

# <h1>NASA Mars News</h1>
# Dependencies
from bs4 import BeautifulSoup
from splinter import Browser
import requests
import re
import pandas as pd
import time


def scrape():
    executable_path = {'executable_path': 'c:\\Users\\thead\\anaconda3\\bin\\chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'http://mars.nasa.gov/news/'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    try:
        slide_elem = soup.select_one("ul.item_list li.slide")
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find("div", class_="content_title").get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find("div", class_="article_teaser_body").get_text()
    except AttributeError:
        return None, None

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    browser.find_by_id("full_image").click()

    new_url = browser.find_by_css('div[class="addthis_toolbox addthis_default_style"]').find_by_css('a').last['href']

    browser.find_by_css('div[class="addthis_toolbox addthis_default_style"]').find_by_css('a').last.click()

    browser.visit(new_url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    p_tag = soup.find_all('aside')[0].find_all('p')

    for p in p_tag:
        if 'Full-Res JPG:' in p.text:
            featured_image_url = 'https:'+p.a['href']

    featured_image_url

    mars_weather = ''
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    time.sleep(5)
    browser.reload()
    time.sleep(5)
    html = browser.html
    time.sleep(5)
    soup = BeautifulSoup(html, 'html.parser')
    time.sleep(5)
    results = soup.find('div', class_= 'css-1dbjc4n').find_all('span', class_ ="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0")
    found = False
    for result in results:
        if (bool(result.find(string=re.compile("InSight"))) & (not found)):
            mars_weather = result.find(string=re.compile("InSight"))
            print(mars_weather)
            found = True
    print(mars_weather)



    mars_facts_url = 'https://space-facts.com/mars/'

    facts_list = pd.read_html(mars_facts_url)

    facts_df = facts_list[0]

    facts_df.columns = ["measure", "value"]
    facts_df

    facts_df.set_index('measure', inplace = True)

    facts_df

    facts_df_html = facts_df.to_html(classes = "table")

    facts_df.to_html('mars_fact_table.html')

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
            hemisphere_label = result.find_all('a', class_ = "itemLink product-item")[0].find('img')['alt']
            split_name = hemisphere_label.split()
            remove_words = ['Enhanced', 'thumbnail']
            result_words  = [word for word in split_name if word not in remove_words]
            hemisphere_name.append(" ".join(result_words))
            hemisphere_link.append(result.find_all('a', class_ = "itemLink product-item")[0]['href'])

    hemisphere_link

    hemisphere_name

    for i in range(0,4):
        browser.visit('https://astrogeology.usgs.gov/'+hemisphere_link[i])
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        enhanced_hemisphere_link.append(soup.find_all('ul')[0].find_all('li')[1].find('a')['href'])

    enhanced_hemisphere_link

    mars_data = {'news_title' : news_title, 'news_p' : news_p, 'featured_image_url' : featured_image_url,  'mars_weather' : mars_weather, 'mars_facts' : facts_df_html, 'hemisphere_name' : hemisphere_name, 'enhanced_hemisphere_link' : enhanced_hemisphere_link}
    print(mars_data)
    return mars_data
mars_data = scrape()
print(mars_data)