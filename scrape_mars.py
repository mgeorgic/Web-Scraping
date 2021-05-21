# Dependencies: Import Splinter and BeautifulSoup
import time
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager

# Set the executable path and initialize the chrome browser in splinter
def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    #browser

# Using python to scrape website
def scrape():
    browser = init_browser()
    mars_data = {}

    # Open the Nasa Mars Webpage (must be open to code)
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # HTML object
    html = browser.html

    # Parse ('lxml') HTML with Beautiful Soup
    soup = bs(html, 'html.parser')

    # Retrieve the latest news title and paragraph 
    # Use 0 bc retrieval is a list and starts at 0, not one
    news_t = soup.find_all('div', class_='content_title')[0].text
    news_p = soup.find_all('div', class_='article_teaser_body')[0].text
    mars_data['news_t'] = news_t
    mars_data['news_p'] = news_p
