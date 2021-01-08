from splinter import Browser
from bs4 import BeautifulSoup
import time
import requests
import pandas as pd
import pymongo
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver


def init_browser():
    executable_path = {"executable_path" : "C:/Users/thmye/.wdm/drivers/chromedriver/win32/87.0.4280.88/chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape1():
    browser = init_browser()

    # visit NASA Mars News website
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)
    time.sleep(1)

    # Scrape page into BeautifulSoup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Get the latest news and paragraph text
    results = soup.find('div', class_='article_teaser_body').text
    
    title_one = soup.find_all('div', class_='content_title')[1].find('a').text

    mars_data = (
        title_one,
        results
    )

    browser.quit()

    return mars_data
    
    # Close the browser after scraping
    

def scrape2():
    browser = init_browser()
    
    # visit JPL Mars Space Images web splinter
    url1 = "https://www.jpl.nasa.gov"
    url2 = "https://www.jpl.nasa.gov/spaceimages/?search=featured+&category=Mars#submit"
    browser.visit(url2)
    time.sleep(1)

    # Locate the featured space images
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()

    more_info_elem = browser.links.find_by_partial_text('more info')
    more_info_elem.click()

    # Scrape page into BeautifulSoup
    for x in range(1):
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')

        featured = soup.find('figure', class_="lede").find_all('a')[0]['href']
        featured_image_url = url1 + featured 

    browser.quit()
    return  featured_image_url  
    
    # Close the broswer after scraping
    

def scrape3():
    browser = init_browser()

    # Visit Mars Facts website
    url3 = 'https://space-facts.com/mars/'
    time.sleep(1)

    # Get the tables from the Mars Facts website
    mars_table = pd.read_html(url3)

    # Manipulate the table from the webpage
    df_1 = mars_table[0]
    df_1 = df_1.rename(columns={0: "Mars Attribute", 1 : "Measurement"})
    df_1 = df_1.set_index("Mars Attribute")

    # Code to transform and save pandas dataframe as html
    html_table = df_1.to_html()
    df_1.to_html('table.html')
    #print(html_table) 

    browser.quit()

    return html_table 

    # Close the broswer after scraping

  
def scrape4():
    browser = init_browser()

    # Visit the USGS Astrogeology website
    url4 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url4)
    time.sleep(1)

    # Scrape page into BeautifulSoup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Get the title links for the hemisphere images
    mars_hemispheres = []
    
    for x in range(0, 4):
        links = browser.find_by_css("a.product-item h3")[x].text
        #print(links)
        mars_hemispheres.append(links)

    # Get the image urls for the hemisphere images and the titles
    hemisphere_image_urls = []

    for i in range(0, 4):
        hemispheres = {}
    
    
        # We have to find the elements on each loop to avoid a stale element exception
        browser.find_by_css("a.product-item h3")[i].click()
        
        # Next, we find the Sample image anchor tag and extract the href
        sample_elem = browser.links.find_by_text('Sample')
        #print(sample_elem)
        hemispheres['img_url'] = sample_elem['href']
        
        # Get Hemisphere title
    
        #hemispheres['title_enhanced'] = browser.find_by_css("h2.title").text
        hemispheres_title = browser.find_by_css("h2.title").text
        title = hemispheres_title.split("E")
        #print(hemispheres['img_url'])
        #print(title[0])
    
        hemisphere_image_urls.append([{"title" : title[0], "img_url" : hemispheres['img_url']}])
        #browser.links.find_by_text('Sample')[i].click()
    
        browser.back()      
    
    
        # Close the browser after scraping is completed
        #print(hemisphere_image_urls["title", "img_url"])

    browser.quit()
        
    # Store all Mars info data in a dictionary
    return hemisphere_image_urls
    
        

    

