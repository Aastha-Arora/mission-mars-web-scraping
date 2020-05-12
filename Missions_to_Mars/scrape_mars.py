
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt
import re
import time


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=True)


def scrape():
	browser = init_browser()

	news_date, news_title, news_p = mars_news(browser)
	
	mars_info = {
				"news_date": news_date,
				"news_title": news_title,
				"news_paragraph": news_p,
				"featured_image": featured_image(browser),
				"weather": mars_weather(browser),
				"facts": mars_facts(browser),
				"four_hemispheres": mars_hemispheres(browser),
				"last_modified": dt.datetime.now()
	}

	browser.quit()
	return mars_info


def mars_news(browser):
	"""
	NASA Mars News
	Scraping the NASA Mars News Site to collect the latest news title and paragraph text
	"""
	url = 'https://mars.nasa.gov/news/'
	browser.visit(url)
	time.sleep(3)
	
	soup = BeautifulSoup(browser.html, 'html.parser')
	news = soup.find('li', class_="slide")
	news_date = news.find('div', class_='list_date').text
	news_title = news.find('div', class_="content_title").text
	news_p = news.find('div', class_="article_teaser_body").text

	return news_date, news_title, news_p

	

def featured_image(browser):
	"""
	JPL Mars Space Images - Featured Image
	Using splinter to navigate the site and finding the full size '.jpg' image url for the current Featured Mars Image
	"""
	url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
	browser.visit(url)
	time.sleep(2)
	
	soup = BeautifulSoup(browser.html, 'html.parser')
	# time.sleep(1)
	browser.links.find_by_partial_text('FULL IMAGE').click()
	# time.sleep(1)
	browser.links.find_by_partial_text('more info').click()
	
	soup = BeautifulSoup(browser.html, 'html.parser')
	partial_url = soup.figure.img['src']
	featured_image_url = 'https://www.jpl.nasa.gov' + partial_url
	
	return featured_image_url



def mars_weather(browser):
	"""
	Mars Weather
	Scraping the latest Mars weather tweet from from the Mars Weather twitter account
	"""
	url = 'https://twitter.com/marswxreport?lang=en'
	browser.visit(url)
	time.sleep(5)
	
	soup = BeautifulSoup(browser.html, 'html.parser')
	pattern = re.compile(r'InSight sol')
	mars_weather = soup.find('span', text=pattern).text
	
	return mars_weather

	

def mars_facts(browser):
	"""
	Mars Facts
	Scraping Mars Facts webpage to get the table containing the Mars planet profile
	"""
	url = 'https://space-facts.com/mars/'
	browser.visit(url)
	time.sleep(2)

	soup = BeautifulSoup(browser.html, 'html.parser')
	tables = pd.read_html(url)
	mars_facts = tables[0]
	mars_facts_html_table = mars_facts.to_html(index=False, header=False)
	
	return mars_facts_html_table	



def mars_hemispheres(browser):
	"""
	Mars Hemispheres
	Scraping the USGS Astrogeology site to obtain high resolution images for each of Mar's hemispheres
	"""
	url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
	browser.visit(url)
	time.sleep(5)

	soup = BeautifulSoup(browser.html, 'html.parser')
	# Find all the four hemispheres of Mars
	hemispheres = soup.find_all('div', class_='item')
	# Declare variable to store result
	hemisphere_image_urls = []
	# Iterate over each hemisphere
	for hemisphere in hemispheres:
	    
	    # Declare variable to store result
	    hemisphere_url = {}
	    
	    # Find the title
	    title = hemisphere.find('div', class_='description').h3.text
	    hemisphere_url['title'] = title
	    
	    # Click on the title to navigate to page
	    # time.sleep(1)
	    browser.find_by_text(title).click()
	    
	    # On the new page, get the html
	    hemi_soup = BeautifulSoup(browser.html, 'html.parser')
	    
	    # Find the url to the full resolution '.jpg' image
	    download = hemi_soup.find('div', class_="downloads")
	    download_link = download.find('a')
	    if download_link.text == 'Sample':
	        img_url = download_link['href']
	        hemisphere_url['img_url'] = img_url
	    
	    # Append hemisphere_url dict to a list of all hemisphere_image_urls
	    hemisphere_image_urls.append(hemisphere_url) 
	    # time.sleep(1)
	    browser.back()

	return hemisphere_image_urls


	



