import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
from IPython.display import HTML
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

def scrape():
    #Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    #Visit redplanetscience.com
    url="https://redplanetscience.com/"
    browser.visit(url)
    html=browser.html
    webpage=BeautifulSoup(html,'html.parser')

    #Get Title
    titles=webpage.find_all('div',class_='content_title')
    most_recent_title=titles[0].text

    #Get body
    paragraphs=webpage.find_all('div',class_='article_teaser_body')
    most_recent_paragraph=paragraphs[0].text
    
    #Visit spaceimage-mars.com
    url_2 = "https://spaceimages-mars.com/"
    browser.visit(url_2)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    relative_image_path = soup.find_all('img')[1]["src"]
    featured_image_url = url_2 + relative_image_path

    #Visit galaxyfacts-mars.com
    url_3="https://galaxyfacts-mars.com"
    table=pd.read_html(url_3)
    mars_earth_comparison=table[0]

    #Convert from Pandas to html
    mars_earth_compare_string=mars_earth_comparison.to_html()
    mars_earth_facts=mars_earth_compare_string.replace('\n','')

    url_4="https://marshemispheres.com/"
    browser.visit(url_4)
    html=browser.html
    mars_hemispheres_soup=BeautifulSoup(html,'html.parser')

    # Mars hemispheres products data
    all_mars_hemispheres = mars_hemispheres_soup.find('div', class_='collapsible results')
    mars_hemispheres = all_mars_hemispheres.find_all('div', class_='item')

    hemisphere_image_urls = []
    
    # Iterate through each hemisphere data
    for i in mars_hemispheres:
        # Collect Title
        hemisphere = i.find('div', class_="description")
        title = hemisphere.h3.text
        
        # Collect image link by browsing to hemisphere page
        hemisphere_link = hemisphere.a["href"]    
        browser.visit(url_4 + hemisphere_link)
        
        image_html = browser.html
        image_soup = BeautifulSoup(image_html, 'html.parser')
        
        image_link = image_soup.find('div', class_='downloads')
        image_url = image_link.find('li').a['href']

        # Create Dictionary to store title and url info
        image_dict = {}
        image_dict['title'] = title
        image_dict['img_url'] = url_4 + image_url
        
        hemisphere_image_urls.append(image_dict)

    print(hemisphere_image_urls)

    

    mars_data = {
        "latest_mars_article": most_recent_title,
        "latest_article_par" : most_recent_paragraph,
        "mars_feat_img" : featured_image_url,
        "mars_earth_table": mars_earth_facts,
        "hems_titles_imgs" : hemisphere_image_urls

    }

    browser.quit()

    return(mars_data)


