from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd
import time

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=True)
    
def marsnews(browser):
    url = 'https://mars.nasa.gov/news/'

    browser.visit(url)
    html= browser.html
    time.sleep(1)

    soup = BeautifulSoup(html, 'html.parser')
    results = soup.find("ul" , class_="item_list")

    news_title = results.find("div", class_ = "content_title").text
    news_p = results.find("div", class_ = "article_teaser_body").text

    return(news_title, news_p)

def marsimage(browser):
    url_images = "https://www.jpl.nasa.gov/spaceimages/"

    browser.visit(url_images)
    browser.click_link_by_partial_text('FULL IMAGE')
    browser.click_link_by_partial_text('more info')
    time.sleep(1)


    html_images= browser.html
    
    soup = BeautifulSoup(html_images, 'html.parser')

    featured_image = soup.find("figure" , class_ ="lede").a["href"]
    featured_image_url= f"https://www.jpl.nasa.gov{featured_image}"

    return (featured_image_url)

def table():

    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    df = tables[0]
    df.columns = ['Description','Mars']
    df.set_index('Description', inplace=True)
    html_table = df.to_html(table_id="scrape_table")
    html_table.replace('\n', '') 

    return(html_table)


def marshemispheres():

    url_hemispheres = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars' 
    
    hemisphere_image_urls = []
    
    response = requests.get(url_hemispheres) 

    soup = BeautifulSoup(response.text, 'html.parser') 

    result_hemispheres = soup.find_all('div', class_ = 'item')

    for result in result_hemispheres:
        img_url = result.find('img',class_ = 'thumb')['src']
        title = result.find('img',class_ = 'thumb')['alt']
        img_dict = {"title":title,
                "img_url": img_url}
        hemisphere_image_urls.append(img_dict)
    
    return(hemisphere_image_urls)

def scrape():

    browser = init_browser()

    mars_data = {}
    news_title, news_p = marsnews(browser)
    featured_image_url = marsimage(browser)
    hemisphere_image_urls = marshemispheres()
    mars_table = table()

    mars_data["news_title"] = news_title
    mars_data["news_p"] = news_p
    mars_data["featured_image_url"] = featured_image_url
    mars_data["Table"] = mars_table
    mars_data["hemisphere_image_urls"] = hemisphere_image_urls

    return (mars_data)