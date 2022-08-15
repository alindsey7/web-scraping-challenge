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
    featured_image_url = url + relative_image_path

    #Visit galaxyfacts-mars.com
    url_3="https://galaxyfacts-mars.com"
    table=pd.read_html(url_3)
    mars_earth_comparison=table[0]

    #Convert from Pandas to html
    mars_earth_compare_string=mars_earth_comparison.to_html()
    mars_earth_facts=mars_earth_compare_string.replace('\n','')

    #Visit marshermispheres.com and go to each hemisphere
    url_4="https://marshemispheres.com/cerberus.html"
    browser.visit(url_4)

    html=browser.html
    mars_hemispheres=BeautifulSoup(html,'html.parser')

    mars_hemispheres_images=browser.links.find_by_partial_href('.jpg')
    cerebrus_img=mars_hemispheres_images['href']
    cerebrus_img

    url_5="https://marshemispheres.com/schiaparelli.html"
    browser.visit(url_5)

    html=browser.html
    mars_hemispheres=BeautifulSoup(html,'html.parser')

    mars_hemispheres_images=browser.links.find_by_partial_href('enhanced')
    schiap_img=mars_hemispheres_images['href']
    schiap_img

    url_6="https://marshemispheres.com/syrtis.html"
    browser.visit(url_6)

    html=browser.html
    mars_hemispheres=BeautifulSoup(html,'html.parser')


    mars_hemispheres_images=browser.links.find_by_partial_href('enhanced')
    syrtmaj_img=mars_hemispheres_images['href']
    syrtmaj_img

    url_7="https://marshemispheres.com/valles.html"
    browser.visit(url_7)

    html=browser.html
    mars_hemispheres=BeautifulSoup(html,'html.parser')

    mars_hemispheres_images=browser.links.find_by_partial_href('enhanced')
    valmar_img=mars_hemispheres_images['href']
    valmar_img

    #Combine into a list
    mars_hemispheres_list=[]
    mars_hems_dict={
        "title": 'Cerberus Hemisphere', 
        "img_url": cerebrus_img
        
    }
    mars_hemispheres_list.append(mars_hems_dict)
    mars_hems_dict={
        "title": 'Schiaparelli Hemisphere' , 
        "img_url": schiap_img
        
    }
    mars_hemispheres_list.append(mars_hems_dict)
    mars_hems_dict={
        "title": 'Syrtis Major Hemisphere' , 
        "img_url": syrtmaj_img
        
    }
    mars_hemispheres_list.append(mars_hems_dict)
    mars_hems_dict={
        "title": 'Valles_Marineris Hemisphere' , 
        "img_url": valmar_img
        
    }
    mars_hemispheres_list.append(mars_hems_dict)

    mars_data = {
        "latest_mars_article": most_recent_title,
        "latest_article_par" : most_recent_paragraph,
        "mars_feat_img" : featured_image_url,
        "mars_earth_table": mars_earth_facts,
        "hems_titles_imgs" : mars_hemispheres_list

    }

    browser.quit()

    return(mars_data)


